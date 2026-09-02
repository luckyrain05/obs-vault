- ==HTTP== (HyperText Transfer Protocol) is a text-based, request-response protocol for transferring data over the web.
- A client opens a TCP connection to a server, sends a request, and the server sends back a response.
- Runs on port 80 by default.
- HTTP is ==stateless== — the server does not remember previous requests. Each request is independent.
- HTTP is unencrypted. Anyone between the client and server can read and modify the traffic.

# HTTPS

- ==HTTPS== is HTTP with ==TLS== (Transport Layer Security) encryption layered underneath.
- Runs on port 443 instead of 80.
- Before any HTTP data is sent, the client and server perform a ==TLS handshake==:

```
+----------+                          +----------+
|  CLIENT  |                          |  SERVER  |
+----------+                          +----------+
|  ClientHello (supported ciphers) -->|          |
|          |<-- ServerHello + cert    |          |
|  verify cert against CA             |          |
|  generate session key        ------>|          |
|          |<---- encrypted OK        |          |
|  ======= encrypted HTTP begins ============== |
+----------+                          +----------+
```

- The server proves its identity with a ==TLS certificate==, signed by a trusted ==Certificate Authority== (CA).
- After the handshake, a shared symmetric key encrypts all traffic. This gives confidentiality (can't read), integrity (can't modify), and authentication (server is who it claims).
- No difference in how requests are written — just `https://` instead of `http://`.

# Methods

- The method tells the server what action to perform on the resource.

**GET**
- Retrieve a resource. No body. Safe and ==idempotent==.

**POST**
- Create a new resource. Includes a body with the data.

**PUT**
- Replace a resource entirely. Idempotent.

**PATCH**
- Partially update a resource. Only sends the fields that changed.

**DELETE**
- Remove a resource. Idempotent.

- ==Idempotent== means calling it multiple times produces the same result as calling it once. `GET`, `PUT`, `DELETE` are idempotent. `POST` is not — each call may create a new resource.
- ==Safe== means the method does not modify the resource. `GET` is safe. `POST`, `PUT`, `PATCH`, `DELETE` are not.

# URLs

- `https://api.example.com/v1/users/42/posts?sort=date&limit=10`

**Base URL**
- `https://api.example.com/v1` — the root. Usually includes a version.

**Path Parameters**
- `/users/42` — identifies a specific resource. `42` is the path parameter.

**Query Parameters**
- `?sort=date&limit=10` — optional filters, sorting, pagination. Appended after `?`, separated by `&`.

# Request / Response

```
+---------------------------+         +---------------------------+
|         REQUEST           |         |         RESPONSE          |
+---------------------------+         +---------------------------+
| POST /v1/users HTTP/1.1   | ------> | HTTP/1.1 201 Created      |
| Host: api.example.com     |         | Content-Type: app/json    |
| Authorization: Bearer ... |         |                           |
| Content-Type: app/json    |         | { "id": 1,               |
|                           |         |   "name": "alice" }       |
| { "name": "alice" }       |         |                           |
+---------------------------+         +---------------------------+
       CLIENT                                SERVER
```

- A request contains: method, URL, headers, and optionally a body.
- A response contains: status code, headers, and optionally a body.

# Status Codes

- The status code tells the client what happened.

**2xx — Success**
- `200 OK` — request succeeded, response has data.
- `201 Created` — resource was created.
- `204 No Content` — success, but nothing to return (common for `DELETE`).

**3xx — Redirection**
- `301 Moved Permanently` — resource has a new URL.
- `304 Not Modified` — cached version is still valid.

**4xx — Client Error**
- `400 Bad Request` — malformed request or invalid data.
- `401 Unauthorized` — missing or invalid authentication.
- `403 Forbidden` — authenticated but not allowed.
- `404 Not Found` — resource doesn't exist.
- `429 Too Many Requests` — rate limit exceeded.

**5xx — Server Error**
- `500 Internal Server Error` — generic server failure.
- `502 Bad Gateway` — server got an invalid response from upstream.
- `503 Service Unavailable` — server is overloaded or down for maintenance.

# Headers

- Headers are key-value metadata attached to requests and responses.

**Content-Type**
- Declares the format of the body. `application/json` for JSON, `text/html` for HTML.

**Authorization**
- Carries credentials. `Bearer <token>` or `Basic <base64>`.

**Accept**
- Tells the server what response format the client wants. `Accept: application/json`.
