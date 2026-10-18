---
title_en: API Authentication
title_de: API-Authentifizierung
entity_type: Concept
aliases:
- Authentication patterns
- API authentication patterns
sources:
- https://www.rfc-editor.org/rfc/rfc6749
- https://www.rfc-editor.org/rfc/rfc6750
- https://www.rfc-editor.org/rfc/rfc7519
- https://www.rfc-editor.org/rfc/rfc9700
- https://api-security.owasp.org/editions/2023/en/0xa2-broken-authentication
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

API authentication establishes who calls an API and on whose behalf. The dominant standard is OAuth 2.0: an authorisation server issues access tokens to a client, which presents them to the resource server, usually as bearer tokens in the Authorization header over TLS (RFC 6749; RFC 6750). Tokens are often JSON Web Tokens whose claims, such as issuer, audience and expiry, must be validated (RFC 7519). Current best practice drops the implicit and password grants, requires PKCE for public clients and restricts tokens to their audience (RFC 9700); broken authentication is the second-most critical API security risk in the [[owasp|OWASP]] API Top 10 2023 (OWASP API2:2023).

### How it works

```text
client ──(1) grant: authorization code + PKCE / client credentials──► authorization server
client ◄─(2) access token (+ refresh token) ──────────────────────────┘
client ──(3) GET /contracts  Authorization: Bearer <token> ─────────► resource server (API)
                                                     validate signature, iss, aud, exp
```

#### 1. Roles

OAuth 2.0 distinguishes four roles: the resource owner, who can grant access to a protected resource; the resource server, which hosts the protected resources; the client, an application that makes requests on behalf of the resource owner and with its authorisation; and the authorisation server, which issues access tokens to the client after authenticating the resource owner (RFC 6749).

#### 2. Grants

A grant is how the client obtains a token. The authorisation code grant uses the authorisation server as an intermediary between client and resource owner; the client credentials grant lets a client obtain access on its own behalf, for example for server-to-server calls; RFC 6749 also defined the implicit grant for browser clients and the resource owner password credentials grant (RFC 6749). The current Best Current Practice says clients should not use the implicit grant and must not use the password grant; public clients must use PKCE to protect the authorisation code, and PKCE is recommended for confidential clients (RFC 9700).

#### 3. Tokens

Access tokens are credentials used to access protected resources; refresh tokens are credentials used to obtain new access tokens (RFC 6749). A bearer token can be used by any party that possesses it, so it must be protected from disclosure in storage and in transport; clients send it in the header Authorization: Bearer and must always use TLS (RFC 6750). Refresh tokens of public clients must be sender-constrained or rotated (RFC 9700).

#### 4. JSON Web Tokens

A JWT is a compact, URL-safe representation of claims, encoded as JSON and signed (JWS), protected with a MAC or encrypted (JWE). Registered claims include iss (issuer), sub (subject), aud (intended recipients; a recipient not listed must reject the token), exp (expiry), nbf (not before), iat (issued at) and jti (a unique ID that helps prevent replay) (RFC 7519). Access tokens should be audience-restricted to a specific resource server and, where possible, sender-constrained, for example with mutual TLS or DPoP (RFC 9700).

#### 5. API keys

API keys identify a calling application. OWASP stresses that OAuth is not authentication and neither are API keys, and that API keys should not be used for user authentication (OWASP API2:2023).

#### 6. Origin and variants

OAuth 2.0 was published as RFC 6749 with bearer token usage in RFC 6750; JWT followed in RFC 7519; RFC 9700 consolidates the security lessons since then into a Best Current Practice (RFC 6749; RFC 6750; RFC 7519; RFC 9700).

### When to use it

- Client credentials when a client accesses resources on its own behalf, such as back-end services calling each other (RFC 6749).
- Authorisation code with PKCE when an application acts on behalf of a user (RFC 9700).
- JWT access tokens when resource servers should validate tokens themselves from their claims and signature (RFC 7519).

### Strengths and limitations

**Strengths**
- Standardised roles, grants and token formats (RFC 6749; RFC 7519).
- Access tokens and refresh tokens separate the credential for resources from the credential for obtaining new tokens (RFC 6749).
- Audience restriction and sender-constrained tokens make stolen tokens less useful (RFC 9700).

**Limitations**
- Anyone holding a bearer token can use it (RFC 6750).
- Many failures are implementation errors: unsigned or weakly signed JWTs accepted, expiry not validated, tokens or passwords sent in URLs (OWASP API2:2023).
- Authentication endpoints are exposed to everyone and attract credential stuffing and brute force (OWASP API2:2023).

### Comparison

| Mechanism | Identifies | Notes |
|-----------|------------|-------|
| API key | The calling application | Not for user authentication (OWASP API2:2023) |
| OAuth 2.0 client credentials | A client acting on its own behalf (RFC 6749) | Server-to-server |
| OAuth 2.0 authorisation code + PKCE | A client acting for a user (RFC 9700) | User-facing apps |
| JWT access token | Claims about a subject, signed (RFC 7519) | Validated by the resource server |

### In practice

OWASP recommends not reinventing authentication, token generation or password storage but using the standards; treating password-recovery endpoints like login endpoints for brute-force protection and rate limiting; requiring re-authentication for sensitive operations; multi-factor authentication where possible; account lockout and CAPTCHA against brute force; and rejecting weak passwords (OWASP API2:2023). On the resource server, every token is checked for signature, issuer, audience and expiry (RFC 7519; OWASP API2:2023). Authorisation per object and per user is a separate concern, covered in [[apis|APIs]].

### Key takeaway

APIs authenticate callers with standard OAuth 2.0 tokens sent as bearer tokens over TLS; validate every token's signature, audience and expiry, use PKCE and audience-restricted tokens, and never treat API keys as user authentication.

### Sources

- Hardt, D. (Ed.) (2012). *The OAuth 2.0 Authorization Framework.* RFC 6749. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc6749)
- Jones, M. & Hardt, D. (2012). *The OAuth 2.0 Authorization Framework: Bearer Token Usage.* RFC 6750. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc6750)
- Jones, M., Bradley, J. & Sakimura, N. (2015). *JSON Web Token (JWT).* RFC 7519. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc7519)
- Lodderstedt, T. et al. (2025). *Best Current Practice for OAuth 2.0 Security.* RFC 9700. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9700)
- OWASP (2023). *API2:2023 Broken Authentication.* OWASP API Security Top 10. [owasp.org](https://api-security.owasp.org/editions/2023/en/0xa2-broken-authentication)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

API-Authentifizierung stellt fest, wer eine API aufruft und in wessen Auftrag. Der vorherrschende Standard ist OAuth 2.0: Ein Authorization Server gibt einem Client Access Tokens aus, die dieser dem Resource Server vorlegt, meist als Bearer Tokens im Authorization-Header über TLS (RFC 6749; RFC 6750). Tokens sind oft JSON Web Tokens, deren Claims wie Aussteller, Zielgruppe und Ablauf geprüft werden müssen (RFC 7519). Die aktuelle Best Practice verzichtet auf Implicit- und Password-Grant, verlangt PKCE für öffentliche Clients und beschränkt Tokens auf ihre Zielgruppe (RFC 9700); fehlerhafte Authentifizierung ist das zweitgrößte API-Sicherheitsrisiko der [[owasp|OWASP]] API Top 10 2023 (OWASP API2:2023).

### Funktionsweise

```text
Client ──(1) Grant: Authorization Code + PKCE / Client Credentials──► Authorization Server
Client ◄─(2) Access Token (+ Refresh Token) ─────────────────────────┘
Client ──(3) GET /contracts  Authorization: Bearer <Token> ────────► Resource Server (API)
                                                    Signatur, iss, aud, exp prüfen
```

#### 1. Rollen

OAuth 2.0 unterscheidet vier Rollen: den Resource Owner, der Zugriff auf eine geschützte Ressource gewähren kann; den Resource Server, der die geschützten Ressourcen bereitstellt; den Client, eine Anwendung, die im Auftrag und mit Zustimmung des Resource Owners Anfragen stellt; und den Authorization Server, der dem Client nach Authentifizierung des Resource Owners Access Tokens ausstellt (RFC 6749).

#### 2. Grants

Ein Grant ist der Weg, auf dem der Client ein Token erhält. Der Authorization Code Grant nutzt den Authorization Server als Vermittler zwischen Client und Resource Owner; der Client Credentials Grant lässt einen Client Zugriff in eigenem Namen erhalten, etwa für Aufrufe zwischen Servern; RFC 6749 definierte außerdem den Implicit Grant für Browser-Clients und den Resource Owner Password Credentials Grant (RFC 6749). Die aktuelle Best Current Practice sagt, Clients sollen den Implicit Grant nicht verwenden und dürfen den Password Grant nicht verwenden; öffentliche Clients müssen PKCE einsetzen, um den Authorization Code zu schützen, und für vertrauliche Clients wird PKCE empfohlen (RFC 9700).

#### 3. Tokens

Access Tokens sind Zugangsdaten für geschützte Ressourcen; Refresh Tokens sind Zugangsdaten, mit denen neue Access Tokens geholt werden (RFC 6749). Ein Bearer Token kann von jedem genutzt werden, der es besitzt, und muss daher bei Speicherung und Übertragung vor Offenlegung geschützt werden; Clients senden es im Header Authorization: Bearer und müssen immer TLS verwenden (RFC 6750). Refresh Tokens öffentlicher Clients müssen an den Absender gebunden oder rotiert werden (RFC 9700).

#### 4. JSON Web Tokens

Ein JWT ist eine kompakte, URL-sichere Darstellung von Claims, als JSON kodiert und signiert (JWS), mit einem MAC geschützt oder verschlüsselt (JWE). Registrierte Claims sind unter anderem iss (Aussteller), sub (Subjekt), aud (vorgesehene Empfänger; ein nicht genannter Empfänger muss das Token ablehnen), exp (Ablauf), nbf (nicht vor), iat (ausgestellt am) und jti (eine eindeutige ID, die gegen Replay hilft) (RFC 7519). Access Tokens sollen auf einen bestimmten Resource Server beschränkt und, wo möglich, an den Absender gebunden sein, etwa mit Mutual TLS oder DPoP (RFC 9700).

#### 5. API-Schlüssel

API-Schlüssel identifizieren eine aufrufende Anwendung. OWASP betont, dass weder OAuth noch API-Schlüssel eine Authentifizierung sind und API-Schlüssel nicht zur Authentifizierung von Nutzern verwendet werden sollen (OWASP API2:2023).

#### 6. Herkunft und Varianten

OAuth 2.0 erschien als RFC 6749, die Nutzung von Bearer Tokens in RFC 6750; JWT folgte in RFC 7519; RFC 9700 fasst die Sicherheitserfahrungen seither als Best Current Practice zusammen (RFC 6749; RFC 6750; RFC 7519; RFC 9700).

### Wann einsetzen

- Client Credentials, wenn ein Client in eigenem Namen auf Ressourcen zugreift, etwa Backend-Dienste, die einander aufrufen (RFC 6749).
- Authorization Code mit PKCE, wenn eine Anwendung im Auftrag eines Nutzers handelt (RFC 9700).
- JWT-Access-Tokens, wenn Resource Server Tokens selbst anhand ihrer Claims und Signatur prüfen sollen (RFC 7519).

### Stärken und Grenzen

**Stärken**
- Standardisierte Rollen, Grants und Tokenformate (RFC 6749; RFC 7519).
- Access Tokens und Refresh Tokens trennen die Zugangsdaten für Ressourcen von denen für neue Tokens (RFC 6749).
- Zielgruppenbeschränkung und an den Absender gebundene Tokens machen gestohlene Tokens weniger nützlich (RFC 9700).

**Grenzen**
- Wer ein Bearer Token besitzt, kann es nutzen (RFC 6750).
- Viele Fehler liegen in der Umsetzung: unsignierte oder schwach signierte JWTs werden akzeptiert, der Ablauf wird nicht geprüft, Tokens oder Passwörter landen in URLs (OWASP API2:2023).
- Authentifizierungs-Endpunkte sind für alle erreichbar und ziehen Credential Stuffing und Brute Force an (OWASP API2:2023).

### Vergleich

| Mechanismus | Identifiziert | Anmerkung |
|-------------|---------------|-----------|
| API-Schlüssel | Die aufrufende Anwendung | Nicht für Nutzer-Authentifizierung (OWASP API2:2023) |
| OAuth 2.0 Client Credentials | Einen Client in eigenem Namen (RFC 6749) | Zwischen Servern |
| OAuth 2.0 Authorization Code + PKCE | Einen Client im Auftrag eines Nutzers (RFC 9700) | Anwendungen mit Nutzern |
| JWT-Access-Token | Signierte Claims über ein Subjekt (RFC 7519) | Vom Resource Server geprüft |

### In der Praxis

OWASP empfiehlt, Authentifizierung, Tokenerzeugung und Passwortspeicherung nicht neu zu erfinden, sondern Standards zu nutzen; Endpunkte zur Passwort-Wiederherstellung beim Schutz gegen Brute Force und beim Rate Limiting wie Login-Endpunkte zu behandeln; für sensible Operationen erneute Authentifizierung zu verlangen; wo möglich Multi-Faktor-Authentifizierung einzusetzen; Kontosperren und CAPTCHA gegen Brute Force zu nutzen und schwache Passwörter abzulehnen (OWASP API2:2023). Auf dem Resource Server wird jedes Token auf Signatur, Aussteller, Zielgruppe und Ablauf geprüft (RFC 7519; OWASP API2:2023). Die Autorisierung pro Objekt und pro Nutzer ist ein eigenes Thema, behandelt in [[apis|APIs]].

### Merksatz

APIs authentifizieren Aufrufer mit standardisierten OAuth-2.0-Tokens, gesendet als Bearer Tokens über TLS; Signatur, Zielgruppe und Ablauf jedes Tokens werden geprüft, PKCE und zielgruppenbeschränkte Tokens eingesetzt, und API-Schlüssel gelten nie als Nutzer-Authentifizierung.

### Quellen

- Hardt, D. (Ed.) (2012). *The OAuth 2.0 Authorization Framework.* RFC 6749. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc6749)
- Jones, M. & Hardt, D. (2012). *The OAuth 2.0 Authorization Framework: Bearer Token Usage.* RFC 6750. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc6750)
- Jones, M., Bradley, J. & Sakimura, N. (2015). *JSON Web Token (JWT).* RFC 7519. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc7519)
- Lodderstedt, T. et al. (2025). *Best Current Practice for OAuth 2.0 Security.* RFC 9700. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9700)
- OWASP (2023). *API2:2023 Broken Authentication.* OWASP API Security Top 10. [owasp.org](https://api-security.owasp.org/editions/2023/en/0xa2-broken-authentication)
