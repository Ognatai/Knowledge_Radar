"""Run the source agents: fetch arXiv and the curated feeds, keep what is new.

    python -m app.agents.monitoring.run_sources            # findings of the last 7 days
    python -m app.agents.monitoring.run_sources --days 14

A failing source is reported and skipped; the others still run. New findings go
to `.knowledge-radar/monitoring/runs/findings-<time>.jsonl` for the relevance
agent and are remembered in `seen.json`, so the next run skips them.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from app.agents.monitoring import feeds
from app.agents.monitoring.config import ConfigError, FeedConfig, SourcesConfig, load_sources_config
from app.agents.monitoring.findings import Finding, SeenStore, write_run


@dataclass(frozen=True)
class CollectResult:
    findings: list[Finding]
    errors: list[str]
    # Undated items of a source fetched for the first time: remembered as seen,
    # not handed on, so a feed without dates does not deliver its whole archive.
    baseline: list[Finding] = field(default_factory=list)
    fetched_sources: list[str] = field(default_factory=list)


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    """Whole words ("AI" does not match "maintain"); a trailing * matches a word start ("Daten*")."""
    if keyword.endswith("*"):
        return re.compile(rf"\b{re.escape(keyword[:-1])}", re.IGNORECASE)
    return re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)


def _matches_keywords(finding: Finding, keywords: list[str]) -> bool:
    if not keywords:
        return True
    text = f"{finding.title} {finding.summary}"
    return any(_keyword_pattern(keyword).search(text) for keyword in keywords)


def collect_findings(
    config: SourcesConfig,
    seen: SeenStore,
    *,
    since: date,
    fetch_arxiv: Callable[[feeds.ArxivQuery], list[Finding]] = feeds.fetch_arxiv,
    fetch_feed: Callable[[FeedConfig], list[Finding]] = feeds.fetch_feed,
) -> CollectResult:
    """New findings published since `since`. Items without a date count as new,
    except on the first fetch of their source (see `CollectResult.baseline`)."""
    batches: list[tuple[str, list[Finding], list[str]]] = []
    errors: list[str] = []
    for phrase in config.arxiv.queries:
        query = feeds.ArxivQuery(phrase, config.arxiv.categories, config.arxiv.max_results_per_query)
        try:
            batches.append(("arXiv", fetch_arxiv(query), []))
        except Exception as exc:  # network and parse errors of one source must not stop the run
            errors.append(f"arXiv ({phrase}): {exc}")
    for feed in config.rss:
        try:
            batches.append((feed.name, fetch_feed(feed), feed.include_keywords))
        except Exception as exc:
            errors.append(f"{feed.name}: {exc}")

    findings: dict[str, Finding] = {}
    baseline: dict[str, Finding] = {}
    for source, batch, keywords in batches:
        for finding in batch:
            if finding.id in findings or finding.id in baseline or seen.contains(finding.id):
                continue
            if finding.published is None and not seen.knows_source(source):
                baseline[finding.id] = finding
                continue
            if finding.published is not None and finding.published < since:
                continue
            if _matches_keywords(finding, keywords):
                findings[finding.id] = finding
    return CollectResult(
        findings=list(findings.values()),
        errors=errors,
        baseline=list(baseline.values()),
        fetched_sources=sorted({source for source, _, _ in batches}),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=7, help="look back this many days (default 7)")
    parser.add_argument("--dry-run", action="store_true", help="print counts only; write nothing")
    args = parser.parse_args()

    try:
        config = load_sources_config()
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        return 1
    now = datetime.now().astimezone()
    seen = SeenStore()
    result = collect_findings(config, seen, since=now.date() - timedelta(days=args.days))
    if not args.dry_run:
        path = write_run(result.findings, now)
        seen.add(result.findings + result.baseline, now)
        seen.add_sources(result.fetched_sources)
        seen.save()

    by_source: dict[str, int] = {}
    for finding in result.findings:
        by_source[finding.source] = by_source.get(finding.source, 0) + 1
    for source, count in sorted(by_source.items()):
        print(f"{count:4}  {source}")
    for error in result.errors:
        print(f"Error: {error}", file=sys.stderr)
    if result.baseline:
        print(f"{len(result.baseline)} undated items of newly added feeds remembered as seen")
    print(f"{len(result.findings)} new findings" + ("" if args.dry_run else f" -> {path}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
