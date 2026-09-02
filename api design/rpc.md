- ==RPC== (Remote Procedure Call) is an [[api]] style where the client calls a function on the server as if it were local.
- REST models nouns (resources): `GET /users/42`. RPC models verbs (actions): `POST /getUser`.
- Every operation is a `POST` to a function-named endpoint. The body contains the arguments.

```
+-----------------------------+       +-----------------------------+
|          REST               |       |          RPC                |
+-----------------------------+       +-----------------------------+
| GET    /users/42            |       | POST /getUser  {id: 42}    |
| DELETE /users/42            |       | POST /deleteUser {id: 42}  |
| POST   /users               |       | POST /createUser {name: …} |
| PATCH  /users/42            |       | POST /updateUser {id: 42}  |
+-----------------------------+       +-----------------------------+
```

- REST uses [[http]] methods to express intent. RPC ignores them — everything is `POST`, and the endpoint name carries the intent.

# gRPC

- A modern RPC framework from Google.
- Uses ==Protocol Buffers== (protobuf) instead of [[json]] — a binary format that is smaller and faster to parse, but not human-readable.
- Services and messages are defined in `.proto` files. Code is generated from them.

```protobuf
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc CreateUser (CreateUserRequest) returns (User);
}

message GetUserRequest {
  int32 id = 1;
}

message User {
  int32 id = 1;
  string name = 2;
}
```

- The `.proto` file is compiled into client and server stubs in any supported language (Python, Go, Java, etc.).
- Supports bidirectional ==streaming== — client and server can send multiple messages over a single connection.
- Uses HTTP/2 under the hood, enabling multiplexed requests over one connection.
- Common in microservice-to-microservice communication where performance matters more than readability.

# When to Use What

```
+---------------+-------------------+--------------------+
|               | REST              | RPC (gRPC)         |
+---------------+-------------------+--------------------+
| Format        | JSON (text)       | Protobuf (binary)  |
| Transport     | HTTP/1.1 or 2     | HTTP/2             |
| Contract      | OpenAPI / ad hoc  | .proto (strict)    |
| Streaming     | No (workarounds)  | Native             |
| Browser       | Native            | Needs grpc-web     |
| Best for      | Public APIs       | Internal services  |
+---------------+-------------------+--------------------+
```
