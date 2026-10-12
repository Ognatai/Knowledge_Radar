---
title_en: Monitoring and Alerting
title_de: Monitoring und Alerting
entity_type: Concept
aliases:
- Monitoring
- Alerting
- Error logging
- Observability
- Four golden signals
sources:
- https://sre.google/sre-book/monitoring-distributed-systems/
- https://opentelemetry.io/docs/concepts/signals/
- https://prometheus.io/docs/alerting/latest/overview/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Monitoring collects, processes, aggregates and displays real-time quantitative data about a system, and alerting notifies a human when something needs attention (Google SRE Book). Systems emit signals, mainly traces, metrics and logs (OpenTelemetry docs: Signals); dashboards summarise them, and alerting rules turn them into notifications, as in Prometheus with its Alertmanager (Prometheus docs: Alerting). Good monitoring watches the four golden signals of latency, traffic, errors and saturation, separates symptoms from causes and pages people only when they can and must act (Google SRE Book).

### How it works

```text
service ─► signals (metrics, logs, traces) ─► storage ─► dashboards
                                              │
                                              └─► alerting rules ─► Alertmanager ─► email / on-call / chat
```

#### 1. Signals

OpenTelemetry collects, processes and exports signals, the outputs that describe a system's activity: traces record the path of a request through an application, metrics are measurements captured at runtime, logs are recordings of events, and baggage carries contextual information between signals; profiles, recordings of resource usage at code level, are in development (OpenTelemetry docs: Signals).

#### 2. What to measure: the four golden signals

For user-facing systems, the Google SRE book names four signals: latency, the time to serve a request, with failed requests tracked separately from successful ones; traffic, the demand on the system in a system-specific measure; errors, the rate of requests that fail explicitly (such as HTTP 500), implicitly or by policy; and saturation, how full the service is, noting that many systems degrade before they reach 100 % utilisation (Google SRE Book).

#### 3. Distributions, not averages

Averages hide slow requests. Collecting request counts in latency buckets, a histogram, separates a slow average from a very slow tail of requests (Google SRE Book).

#### 4. White-box and black-box monitoring

White-box monitoring uses metrics exposed by the system's internals and can detect imminent problems and failures hidden by retries; black-box monitoring tests externally visible behaviour as a user would see it and catches active problems (Google SRE Book).

#### 5. Symptoms and causes

A monitoring system should answer two questions: what is broken (the symptom) and why (the cause); the distinction is one of the most important in good monitoring (Google SRE Book).

#### 6. Alerting

An alert is a notification intended to be read by a human, as a ticket, an email or a page (Google SRE Book). In Prometheus, alerting rules in the Prometheus servers send alerts to an Alertmanager, which manages them, including silencing, inhibition and aggregation, and sends notifications by email, on-call systems or chat (Prometheus docs: Alerting). Every page should be actionable, require human intelligence rather than a robotic response, and be urgent, because people can react urgently only a few times a day before they tire (Google SRE Book).

#### 7. Origin and variants

The four golden signals and the paging rules come from Google's site reliability engineering practice (Google SRE Book); OpenTelemetry standardises the signal types (OpenTelemetry docs: Signals). For LLM applications, traces per request with prompts, tokens and costs are covered in [[llm-observability-and-tracing|LLM Observability and Tracing]], and conversation-level measures for chat and voice bots in [[conversation-analytics|Conversation Analytics]].

### When to use it

- For every service in production, from the first deployment ([[mlops-and-deployment|MLOps and Deployment]]).
- Alerting on symptoms users notice, such as errors and latency, and dashboards for diagnosing causes (Google SRE Book).
- Alerting on quality regressions of AI systems, for example a rising no-match or escalation rate in a [[voice-agents|voice bot]] ([[conversation-analytics|Conversation Analytics]]).

### Strengths and limitations

**Strengths**
- The four golden signals give a small, general starting set of metrics (Google SRE Book).
- One framework collects, processes and exports traces, metrics and logs (OpenTelemetry docs: Signals).
- Silencing, inhibition and aggregation in the Alertmanager reduce noise (Prometheus docs: Alerting).

**Limitations**
- Too many pages tire people; pages that need only a robotic response should not be pages (Google SRE Book).
- Averages hide tail latency unless distributions are recorded (Google SRE Book).
- What counts as an error can be implicit or a matter of policy, so error rates must be defined per service (Google SRE Book).

### Comparison

| Approach | What it shows | Source |
|----------|---------------|--------|
| Metrics and dashboards | Trends of latency, traffic, errors, saturation | Google SRE Book |
| Logs | Individual events, such as errors | OpenTelemetry docs: Signals |
| Traces | The path of a request through services | OpenTelemetry docs: Signals |
| Black-box probes | Behaviour as users see it | Google SRE Book |
| Alerts | A human must act now | Google SRE Book; Prometheus docs: Alerting |

### In practice

Alert rules are kept simple, predictable and reliable, because the rules that catch real incidents most often should be the simplest (Google SRE Book). Latency is recorded as histograms, failed and successful requests separately (Google SRE Book). Alertmanager routes notifications to email, on-call systems or chat (Prometheus docs: Alerting).

### Key takeaway

Monitor latency, traffic, errors and saturation from metrics, logs and traces, alert on symptoms users feel, and page a human only when the alert is actionable and urgent.

### Sources

- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (Eds.) (2016). *Monitoring Distributed Systems.* Site Reliability Engineering, Chapter 6. Google. [sre.google](https://sre.google/sre-book/monitoring-distributed-systems/)
- OpenTelemetry. *Signals.* OpenTelemetry documentation. [opentelemetry.io](https://opentelemetry.io/docs/concepts/signals/)
- Prometheus. *Alerting overview.* Prometheus documentation. [prometheus.io](https://prometheus.io/docs/alerting/latest/overview/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Monitoring sammelt, verarbeitet, aggregiert und zeigt quantitative Echtzeitdaten über ein System, und Alerting benachrichtigt einen Menschen, wenn etwas Aufmerksamkeit braucht (Google SRE Book). Systeme senden Signale, vor allem Traces, Metriken und Logs (OpenTelemetry docs: Signals); Dashboards fassen sie zusammen, und Alerting-Regeln machen daraus Benachrichtigungen, wie in Prometheus mit seinem Alertmanager (Prometheus docs: Alerting). Gutes Monitoring beobachtet die vier Golden Signals Latenz, Traffic, Fehler und Sättigung, trennt Symptome von Ursachen und alarmiert Menschen nur, wenn sie handeln können und müssen (Google SRE Book).

### Funktionsweise

```text
Dienst ─► Signale (Metriken, Logs, Traces) ─► Speicher ─► Dashboards
                                              │
                                              └─► Alerting-Regeln ─► Alertmanager ─► E-Mail / Bereitschaft / Chat
```

#### 1. Signale

OpenTelemetry sammelt, verarbeitet und exportiert Signale, die Ausgaben, die die Aktivität eines Systems beschreiben: Traces halten den Weg einer Anfrage durch eine Anwendung fest, Metriken sind zur Laufzeit erfasste Messwerte, Logs sind Aufzeichnungen von Ereignissen, und Baggage trägt Kontextinformationen zwischen Signalen; Profile, Aufzeichnungen des Ressourcenverbrauchs auf Code-Ebene, sind in Entwicklung (OpenTelemetry docs: Signals).

#### 2. Was messen: die vier Golden Signals

Für Systeme mit Nutzern nennt das Google-SRE-Buch vier Signale: Latenz, die Zeit, eine Anfrage zu bedienen, wobei fehlgeschlagene Anfragen getrennt von erfolgreichen erfasst werden; Traffic, die Last auf dem System in einem systemspezifischen Maß; Fehler, die Rate der Anfragen, die ausdrücklich (etwa HTTP 500), implizit oder per Richtlinie scheitern; und Sättigung, wie „voll“ der Dienst ist, wobei viele Systeme schon vor 100 % Auslastung schlechter werden (Google SRE Book).

#### 3. Verteilungen statt Durchschnitte

Durchschnitte verbergen langsame Anfragen. Anfragen in Latenz-Buckets zu zählen, also als Histogramm, trennt einen langsamen Durchschnitt von einem sehr langsamen Ende der Verteilung (Google SRE Book).

#### 4. White-Box- und Black-Box-Monitoring

White-Box-Monitoring nutzt Metriken, die das Innere des Systems bereitstellt, und kann drohende Probleme und durch Wiederholungen verdeckte Fehler erkennen; Black-Box-Monitoring testet das von außen sichtbare Verhalten so, wie Nutzer es sehen, und erkennt akute Probleme (Google SRE Book).

#### 5. Symptome und Ursachen

Ein Monitoring-System soll zwei Fragen beantworten: Was ist kaputt (das Symptom) und warum (die Ursache); diese Unterscheidung ist eine der wichtigsten für gutes Monitoring (Google SRE Book).

#### 6. Alerting

Ein Alert ist eine Benachrichtigung, die ein Mensch lesen soll, als Ticket, E-Mail oder Page (Google SRE Book). In Prometheus schicken Alerting-Regeln in den Prometheus-Servern Alerts an einen Alertmanager, der sie verwaltet, einschließlich Stummschalten, Unterdrücken und Zusammenfassen, und Benachrichtigungen per E-Mail, Bereitschaftssystem oder Chat verschickt (Prometheus docs: Alerting). Jede Page soll eine Handlung erfordern, menschliches Urteil statt einer mechanischen Reaktion verlangen und dringend sein, denn Menschen können nur wenige Male am Tag dringend reagieren, bevor sie ermüden (Google SRE Book).

#### 7. Herkunft und Varianten

Die vier Golden Signals und die Regeln für Pages stammen aus Googles Site-Reliability-Engineering-Praxis (Google SRE Book); OpenTelemetry vereinheitlicht die Signaltypen (OpenTelemetry docs: Signals). Für LLM-Anwendungen behandelt [[llm-observability-and-tracing|LLM Observability and Tracing]] Traces pro Anfrage mit Prompts, Tokens und Kosten, und [[conversation-analytics|Conversation Analytics]] Maße auf Gesprächsebene für Chat- und Voicebots.

### Wann einsetzen

- Für jeden Dienst im Betrieb, ab dem ersten Deployment ([[mlops-and-deployment|MLOps und Deployment]]).
- Alerts auf Symptome, die Nutzer bemerken, etwa Fehler und Latenz, und Dashboards zur Diagnose der Ursachen (Google SRE Book).
- Alerts auf Qualitätsrückgänge von KI-Systemen, etwa eine steigende No-Match- oder Eskalationsrate eines Voicebots ([[conversation-analytics|Conversation Analytics]]).

### Stärken und Grenzen

**Stärken**
- Die vier Golden Signals sind eine kleine, allgemeine Grundmenge an Metriken (Google SRE Book).
- Ein Framework sammelt, verarbeitet und exportiert Traces, Metriken und Logs (OpenTelemetry docs: Signals).
- Stummschalten, Unterdrücken und Zusammenfassen im Alertmanager verringern Rauschen (Prometheus docs: Alerting).

**Grenzen**
- Zu viele Pages ermüden; Pages, die nur eine mechanische Reaktion erfordern, sollten keine Pages sein (Google SRE Book).
- Durchschnitte verbergen die langsamen Anfragen am Ende der Verteilung, wenn keine Verteilungen erfasst werden (Google SRE Book).
- Was als Fehler zählt, kann implizit oder eine Frage der Richtlinie sein, daher müssen Fehlerraten pro Dienst definiert werden (Google SRE Book).

### Vergleich

| Ansatz | Was er zeigt | Quelle |
|--------|--------------|--------|
| Metriken und Dashboards | Verläufe von Latenz, Traffic, Fehlern, Sättigung | Google SRE Book |
| Logs | Einzelne Ereignisse, etwa Fehler | OpenTelemetry docs: Signals |
| Traces | Den Weg einer Anfrage durch Dienste | OpenTelemetry docs: Signals |
| Black-Box-Prüfungen | Verhalten, wie Nutzer es sehen | Google SRE Book |
| Alerts | Ein Mensch muss jetzt handeln | Google SRE Book; Prometheus docs: Alerting |

### In der Praxis

Alert-Regeln werden einfach, vorhersehbar und verlässlich gehalten, weil die Regeln, die am häufigsten echte Vorfälle erkennen, die einfachsten sein sollten (Google SRE Book). Latenz wird als Histogramm erfasst, fehlgeschlagene und erfolgreiche Anfragen getrennt (Google SRE Book). Der Alertmanager leitet Benachrichtigungen an E-Mail, Bereitschaftssysteme oder Chat weiter (Prometheus docs: Alerting).

### Merksatz

Latenz, Traffic, Fehler und Sättigung aus Metriken, Logs und Traces überwachen, auf Symptome alarmieren, die Nutzer spüren, und einen Menschen nur dann rufen, wenn der Alert eine Handlung erfordert und dringend ist.

### Quellen

- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (Eds.) (2016). *Monitoring Distributed Systems.* Site Reliability Engineering, Chapter 6. Google. [sre.google](https://sre.google/sre-book/monitoring-distributed-systems/)
- OpenTelemetry. *Signals.* OpenTelemetry documentation. [opentelemetry.io](https://opentelemetry.io/docs/concepts/signals/)
- Prometheus. *Alerting overview.* Prometheus documentation. [prometheus.io](https://prometheus.io/docs/alerting/latest/overview/)
