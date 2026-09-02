- API is an acronym for ===Application Programming Interface==.
	- It is simply defined as interface that allows one piece of software to communicate with another.
	- This definition is purposely broad. The point is that caller doesn't need to know how the other side is implemented, only what requests it accepts and what responses it returns.

# Web APIs

- Web APIs expose functionality over [[http]]. A client sends a request, the server processes it, and sends back a response.

# REST

- ==REST== (Representational State Transfer) is an architectural style for designing web APIs.
- Resources are identified by URLs. Each URL represents a thing (user, post, order).
- Requests are ==stateless==, the server does not remember previous requests. Every request must carry all the information the server needs.
- A REST API that follows all constraints is called ==RESTful==.

# GraphQL

- ==GraphQL== is an alternative to REST where the client specifies exactly what data it wants.
- A single endpoint (typically `/graphql`) handles all requests instead of many resource-specific URLs.
- The client sends a query describing the shape of the response it needs.

```
+-----------------------------+       +-----------------------------+
|          REST               |       |         GraphQL             |
+-----------------------------+       +-----------------------------+
| GET /users/1                |       | POST /graphql               |
| GET /users/1/posts          |       | { query {                   |
| GET /users/1/posts/comments |       |     user(id: 1) {           |
| (3 requests)                |       |       name                  |
|                             |       |       posts { title }       |
|                             |       |     }                       |
|                             |       |   }                         |
|                             |       | }                           |
|                             |       | (1 request)                 |
+-----------------------------+       +-----------------------------+
```

- REST can ==over-fetch== (return fields you don't need) or ==under-fetch== (require multiple requests to assemble related data). GraphQL solves both.
- Trade-off: GraphQL is more complex to set up and harder to cache since every query is unique.

# JSON

- [[json]] is the standard data format for APIs.
- Key-value pairs. Keys are strings, values can be strings, numbers, booleans, arrays, objects, or `null`.

```json
{
  "id": 1,
  "name": "alice",
  "active": true,
  "tags": ["admin", "staff"],
  "address": {
    "city": "Seattle"
  }
}
```

# Authentication

**API Keys**
- A single token passed as a header or query parameter. Simple but no user context.
- `X-API-Key: abc123` or `?api_key=abc123`.

**Bearer Tokens**
- A token (often a JWT) passed in the `Authorization` header.
- `Authorization: Bearer eyJhbGci...`
- The server validates the token to identify the user and their permissions.

**OAuth**
- A protocol that lets a user grant a third-party app limited access without sharing their password.
- The app redirects the user to the provider (Google, GitHub), the user approves, and the app receives an ==access token==.
- Used when an app needs to act on behalf of a user.

# Rate Limiting

- APIs enforce ==rate limits== to prevent abuse and protect server resources.
- Limits are typically expressed as requests per time window (e.g., 100 requests per minute).
- Exceeding the limit returns `429 Too Many Requests`.
- Response headers often indicate the limit status: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
