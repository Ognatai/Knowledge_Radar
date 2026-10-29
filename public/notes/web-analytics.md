---
title_en: Web Analytics
title_de: Web-Analytics
entity_type: Method
aliases:
- Web analytics
- Digital analytics
- Google Analytics 4
- GA4
- Marketing attribution
- Attribution modelling
- Consent mode
- Web-Analytics
sources:
- https://support.google.com/analytics/answer/9322688
- https://support.google.com/analytics/answer/9358801
- https://support.google.com/analytics/answer/10596866
- https://developers.google.com/tag-platform/security/concepts/consent-mode
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Web analytics measures how people use websites and apps, page views, clicks, sign-ups, purchases, in order to improve products, marketing and customer journeys. In Google Analytics 4 (GA4), a widely used tool, everything is recorded as events with parameters; important events are marked as key events, raw events can be exported to the BigQuery [[data-warehouse|data warehouse]] for SQL analysis, and attribution models distribute credit for a key event across the marketing touchpoints that preceded it (Google Analytics, Events; Google Analytics, BigQuery Export; Google Analytics, Attribution). In the EU, cookies and identifiers for analytics require consent, which GA4 handles through consent mode (Google Tag Platform, Consent mode; [[tdddg|TDDDG]]).

### How it works

```text
user interaction on website or app
 ▼
tag / SDK sends events with parameters (batched), respecting consent state
 ▼
GA4 property: processing, sessions, key events, reports, attribution
 ▼
BigQuery export: raw events per day (+ streaming intraday)
 ▼
data modelling and analysis: funnels, customer journeys, cohorts, ML features
```

#### 1. The event model

In GA4, "an event allows you to measure a specific interaction or occurrence on your website or app", including system events such as an app crash (Google Analytics, Events). There are four kinds: automatically collected events, enhanced measurement events collected when that option is enabled, recommended events with predefined names and parameters that unlock reports, and custom events, which should only be created when no other event fits. Each event carries parameters that describe it. Events that matter most for the business, such as a purchase or sign-up, are marked as key events (Google Analytics, Events). Most events are sent in batches of up to 20, with a 16 KB limit per request, and offline events arriving more than two calendar days late are ignored (Google Analytics, Events).

#### 2. Export to BigQuery

Reports in the GA4 interface are processed and aggregated. For full analysis, all raw events can be exported to BigQuery, where they belong to the organisation and are controlled by BigQuery access rights (Google Analytics, BigQuery Export). A daily export writes the complete, unsampled events of the previous day into a table `events_YYYYMMDD`; a streaming export makes current-day data available within minutes in `events_intraday_YYYYMMDD`, a staging table that is deleted once the daily table is complete. Standard properties may export up to one million events per day, and data cannot be re-exported later (Google Analytics, BigQuery Export). In the warehouse, events are joined with CRM, sales or campaign data and modelled into fact and dimension tables ([[data-modelling|data modelling]], [[sql|SQL]]).

```sql
-- illustrative: daily purchases per traffic medium from the GA4 export
SELECT event_date, traffic_source.medium, COUNT(*) AS purchases
FROM `project.analytics_123456.events_*`
WHERE event_name = 'purchase'
  AND _TABLE_SUFFIX BETWEEN '20260901' AND '20260930'
GROUP BY event_date, traffic_source.medium
ORDER BY event_date;
```

#### 3. Attribution and customer journeys

"Attribution is the act of assigning credit for important user actions to different ads, clicks, and factors" (Google Analytics, Attribution). Customers often search several times and click several ads before buying, so the question is how much each touchpoint contributed. GA4's data-driven attribution uses machine learning on converting and non-converting paths and estimates each touchpoint's contribution by comparing outcomes with and without that interaction; models are specific to each advertiser and key event. Paid and organic last click gives all credit to the last channel clicked and ignores direct traffic. The rule-based first click, linear, time decay and position-based models have not been available since November 2023 (Google Analytics, Attribution). Estimating the causal effect of a campaign with experiments or observational methods is covered in [[causal-inference|causal inference]].

#### 4. Consent

"Consent mode allows web and app developers to adjust tag and app SDK behavior based on user consent choices" (Google Tag Platform, Consent mode). Consent types include `analytics_storage` for analytics cookies and identifiers, `ad_storage`, `ad_user_data` for sending user data to Google for advertising and `ad_personalization`. In basic consent mode, Google tags do not load until the user responds to the consent banner and no data, not even the consent status, is sent before; in advanced mode, tags load with consent denied by default and send cookieless pings until consent is granted. Google uses these pings to model conversions and key events for users who decline, once a data threshold is reached (Google Tag Platform, Consent mode). In Germany, § 25 [[tdddg|TDDDG]] requires consent before information is stored on or read from a device unless strictly necessary, and the processing of personal data falls under the [[gdpr|GDPR]].

#### Origin and variants

GA4 is built around events for websites and apps alike (Google Analytics, Events). Its rule-based attribution models were removed in November 2023, leaving data-driven and last-click models (Google Analytics, Attribution), and consent mode with basic and advanced implementations reflects consent requirements for cookies and identifiers (Google Tag Platform, Consent mode).

### When to use it

- Measuring conversion funnels and drop-offs on websites and apps (Google Analytics, Events).
- Evaluating marketing channels and campaigns across multi-step customer journeys (Google Analytics, Attribution).
- Combining behavioural data with internal data in a warehouse for segmentation, forecasting or personalisation (Google Analytics, BigQuery Export).

### Strengths and limitations

**Strengths**
- A uniform event model covers websites and apps (Google Analytics, Events).
- Raw data export enables any analysis in SQL and joins with internal data (Google Analytics, BigQuery Export).
- Data-driven attribution uses observed paths instead of fixed rules (Google Analytics, Attribution).

**Limitations**
- Users who decline consent are only modelled, not measured, which makes figures estimates (Google Tag Platform, Consent mode).
- Export limits and the impossibility of re-exporting require planning from the start (Google Analytics, BigQuery Export).
- Attribution distributes credit among touchpoints; whether a campaign caused a purchase is a causal question ([[causal-inference|causal inference]]).

### Comparison

| Attribution model | Credit | Status in GA4 |
|---|---|---|
| Data-driven | distributed by a learned model per key event | available |
| Paid and organic last click | 100% to the last clicked channel (direct ignored) | available |
| Google paid channels last click | 100% to the last Google Ads channel | available |
| First click, linear, time decay, position-based | fixed rules | removed in November 2023 |

Source: Google Analytics, Attribution.

### In practice

A tracking plan lists events, parameters and key events before implementation, preferring recommended events over custom ones (Google Analytics, Events). Dashboards on top of the warehouse follow the principles in [[data-visualisation|data visualisation]]; ownership and definitions of metrics belong to [[data-governance|data governance]].

### Regulatory context

Analytics cookies and identifiers require consent under § 25 [[tdddg|TDDDG]], which implements the [[eprivacy-directive|ePrivacy Directive]]; personal data in analytics is subject to the [[gdpr|GDPR]], including rules on transfers to third countries.

### Key takeaway

Web analytics records user interactions as events, exports them as raw data for analysis and attributes outcomes to marketing touchpoints; consent requirements mean that part of the data is modelled rather than measured.

### Sources

- Google Analytics, Events. *[GA4] About events.* Analytics Help. [support.google.com](https://support.google.com/analytics/answer/9322688)
- Google Analytics, BigQuery Export. *[GA4] BigQuery Export.* Analytics Help. [support.google.com](https://support.google.com/analytics/answer/9358801)
- Google Analytics, Attribution. *[GA4] Get started with attribution.* Analytics Help. [support.google.com](https://support.google.com/analytics/answer/10596866)
- Google Tag Platform, Consent mode. *Consent mode overview.* Google for Developers. [developers.google.com](https://developers.google.com/tag-platform/security/concepts/consent-mode)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Web-Analytics misst, wie Menschen Websites und Apps nutzen, Seitenaufrufe, Klicks, Registrierungen, Käufe, um Produkte, Marketing und Customer Journeys zu verbessern. Google Analytics 4 (GA4), ein verbreitetes Werkzeug, erfasst alles als Events mit Parametern; wichtige Events werden als Key Events markiert, Roh-Events lassen sich in das [[data-lakehouse|Data Warehouse]] BigQuery exportieren und dort mit SQL auswerten, und Attributionsmodelle verteilen den Erfolg eines Key Events auf die Marketing-Kontaktpunkte davor (Google Analytics, Events; Google Analytics, BigQuery Export; Google Analytics, Attribution). In der EU brauchen Cookies und Kennungen für Analysen eine Einwilligung, die GA4 über den Consent Mode berücksichtigt (Google Tag Platform, Consent mode; [[tdddg|TDDDG]]).

### Funktionsweise

```text
Interaktion auf Website oder App
 ▼
Tag / SDK sendet Events mit Parametern (gebündelt), abhängig vom Einwilligungsstatus
 ▼
GA4-Property: Verarbeitung, Sitzungen, Key Events, Berichte, Attribution
 ▼
BigQuery-Export: Roh-Events je Tag (+ Streaming für den laufenden Tag)
 ▼
Datenmodellierung und Analyse: Funnels, Customer Journeys, Kohorten, ML-Features
```

#### 1. Das Event-Modell

In GA4 gilt: „an event allows you to measure a specific interaction or occurrence on your website or app“, auch Systemereignisse wie ein App-Absturz (Google Analytics, Events). Es gibt vier Arten: automatisch erfasste Events, Events der erweiterten Messung, wenn diese Option aktiv ist, empfohlene Events mit vorgegebenen Namen und Parametern, die Berichte freischalten, und eigene Events, die nur angelegt werden sollten, wenn kein anderes Event passt. Jedes Event trägt Parameter, die es beschreiben. Events, die für das Geschäft besonders wichtig sind, etwa ein Kauf oder eine Registrierung, werden als Key Events markiert (Google Analytics, Events). Die meisten Events werden in Bündeln von bis zu 20 gesendet, mit 16 KB je Anfrage, und Offline-Events, die mehr als zwei Kalendertage zu spät eintreffen, werden ignoriert (Google Analytics, Events).

#### 2. Export nach BigQuery

Berichte in der GA4-Oberfläche sind verarbeitet und aggregiert. Für vollständige Analysen lassen sich alle Roh-Events nach BigQuery exportieren, wo sie der Organisation gehören und über die Zugriffsrechte von BigQuery geschützt sind (Google Analytics, BigQuery Export). Ein täglicher Export schreibt die vollständigen, nicht gesampelten Events des Vortags in eine Tabelle `events_YYYYMMDD`; ein Streaming-Export macht Daten des laufenden Tages innerhalb von Minuten in `events_intraday_YYYYMMDD` verfügbar, einer Zwischentabelle, die gelöscht wird, sobald die Tagestabelle vollständig ist. Standard-Properties dürfen bis zu eine Million Events pro Tag exportieren, und Daten lassen sich später nicht erneut exportieren (Google Analytics, BigQuery Export). Im Warehouse werden Events mit CRM-, Vertriebs- oder Kampagnendaten verknüpft und in Fakten- und Dimensionstabellen modelliert ([[data-modelling|Datenmodellierung]], [[sql|SQL]]).

```sql
-- zur Veranschaulichung: tägliche Käufe je Traffic-Medium aus dem GA4-Export
SELECT event_date, traffic_source.medium, COUNT(*) AS purchases
FROM `project.analytics_123456.events_*`
WHERE event_name = 'purchase'
  AND _TABLE_SUFFIX BETWEEN '20260901' AND '20260930'
GROUP BY event_date, traffic_source.medium
ORDER BY event_date;
```

#### 3. Attribution und Customer Journeys

„Attribution is the act of assigning credit for important user actions to different ads, clicks, and factors“ (Google Analytics, Attribution). Kundinnen und Kunden suchen oft mehrmals und klicken mehrere Anzeigen, bevor sie kaufen, daher stellt sich die Frage, wie viel jeder Kontaktpunkt beigetragen hat. Die datengetriebene Attribution von GA4 nutzt Machine Learning auf Pfaden mit und ohne Conversion und schätzt den Beitrag jedes Kontaktpunkts, indem sie Ergebnisse mit und ohne diese Interaktion vergleicht; die Modelle gelten je Werbetreibendem und Key Event. Paid and Organic Last Click schreibt den gesamten Erfolg dem zuletzt angeklickten Kanal zu und ignoriert direkte Zugriffe. Die regelbasierten Modelle First Click, linear, zeitlicher Verfall und positionsbasiert sind seit November 2023 nicht mehr verfügbar (Google Analytics, Attribution). Die Schätzung der kausalen Wirkung einer Kampagne mit Experimenten oder Beobachtungsmethoden behandelt [[causal-inference|Kausale Inferenz]].

#### 4. Einwilligung

„Consent mode allows web and app developers to adjust tag and app SDK behavior based on user consent choices“ (Google Tag Platform, Consent mode). Zu den Einwilligungstypen gehören `analytics_storage` für Analyse-Cookies und -Kennungen, `ad_storage`, `ad_user_data` für das Senden von Nutzerdaten an Google zu Werbezwecken und `ad_personalization`. Im Basic Consent Mode laden Google-Tags erst, wenn die Nutzenden auf das Einwilligungsbanner reagiert haben, und vorher werden keine Daten gesendet, nicht einmal der Einwilligungsstatus; im Advanced Mode laden Tags mit standardmäßig verweigerter Einwilligung und senden cookielose Pings, bis die Einwilligung erteilt ist. Google nutzt diese Pings, um Conversions und Key Events für Nutzende ohne Einwilligung zu modellieren, sobald eine Datenschwelle erreicht ist (Google Tag Platform, Consent mode). In Deutschland verlangt § 25 [[tdddg|TDDDG]] eine Einwilligung, bevor Informationen auf einem Endgerät gespeichert oder ausgelesen werden, sofern das nicht unbedingt erforderlich ist, und die Verarbeitung personenbezogener Daten unterliegt der [[gdpr|DSGVO]].

#### Herkunft und Varianten

GA4 ist für Websites und Apps gleichermaßen um Events herum aufgebaut (Google Analytics, Events). Seine regelbasierten Attributionsmodelle wurden im November 2023 entfernt, sodass datengetriebene und Last-Click-Modelle bleiben (Google Analytics, Attribution), und der Consent Mode mit Basic- und Advanced-Umsetzung trägt den Einwilligungspflichten für Cookies und Kennungen Rechnung (Google Tag Platform, Consent mode).

### Wann einsetzen

- Conversion-Funnels und Abbrüche auf Websites und in Apps messen (Google Analytics, Events).
- Marketingkanäle und Kampagnen über mehrstufige Customer Journeys hinweg bewerten (Google Analytics, Attribution).
- Verhaltensdaten im Warehouse mit internen Daten verbinden, für Segmentierung, Prognosen oder Personalisierung (Google Analytics, BigQuery Export).

### Stärken und Grenzen

**Stärken**
- Ein einheitliches Event-Modell deckt Websites und Apps ab (Google Analytics, Events).
- Der Export der Rohdaten erlaubt jede Analyse in SQL und Verknüpfungen mit internen Daten (Google Analytics, BigQuery Export).
- Datengetriebene Attribution nutzt beobachtete Pfade statt fester Regeln (Google Analytics, Attribution).

**Grenzen**
- Nutzende ohne Einwilligung werden nur modelliert, nicht gemessen, sodass Zahlen Schätzungen sind (Google Tag Platform, Consent mode).
- Exportgrenzen und die fehlende Möglichkeit zum erneuten Export erfordern Planung von Anfang an (Google Analytics, BigQuery Export).
- Attribution verteilt Erfolge auf Kontaktpunkte; ob eine Kampagne einen Kauf verursacht hat, ist eine kausale Frage ([[causal-inference|Kausale Inferenz]]).

### Vergleich

| Attributionsmodell | Zuordnung | Status in GA4 |
|---|---|---|
| Datengetrieben | von einem gelernten Modell je Key Event verteilt | verfügbar |
| Paid and Organic Last Click | 100 % an den zuletzt angeklickten Kanal (direkt ignoriert) | verfügbar |
| Google Paid Channels Last Click | 100 % an den letzten Google-Ads-Kanal | verfügbar |
| First Click, linear, zeitlicher Verfall, positionsbasiert | feste Regeln | im November 2023 entfernt |

Quelle: Google Analytics, Attribution.

### In der Praxis

Ein Tracking-Plan legt Events, Parameter und Key Events vor der Umsetzung fest und bevorzugt empfohlene vor eigenen Events (Google Analytics, Events). Dashboards auf dem Warehouse folgen den Grundsätzen der [[data-visualisation|Datenvisualisierung]]; Verantwortung und Definitionen von Kennzahlen gehören zur [[data-governance|Data Governance]].

### Regulatorischer Kontext

Analyse-Cookies und -Kennungen erfordern eine Einwilligung nach § 25 [[tdddg|TDDDG]], das die [[eprivacy-directive|ePrivacy-Richtlinie]] umsetzt; personenbezogene Daten in Analysen unterliegen der [[gdpr|DSGVO]], einschließlich der Regeln für Übermittlungen in Drittländer.

### Merksatz

Web-Analytics erfasst Interaktionen als Events, exportiert sie als Rohdaten zur Analyse und ordnet Ergebnisse Marketing-Kontaktpunkten zu; wegen der Einwilligungspflicht wird ein Teil der Daten modelliert statt gemessen.

### Quellen

- Google Analytics, Events. *[GA4] About events.* Analytics-Hilfe. [support.google.com](https://support.google.com/analytics/answer/9322688)
- Google Analytics, BigQuery Export. *[GA4] BigQuery Export.* Analytics-Hilfe. [support.google.com](https://support.google.com/analytics/answer/9358801)
- Google Analytics, Attribution. *[GA4] Get started with attribution.* Analytics-Hilfe. [support.google.com](https://support.google.com/analytics/answer/10596866)
- Google Tag Platform, Consent mode. *Consent mode overview.* Google for Developers. [developers.google.com](https://developers.google.com/tag-platform/security/concepts/consent-mode)
