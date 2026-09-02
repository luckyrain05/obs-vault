- ==Prisma== is a TypeScript ORM (Object-Relational Mapper) for Node.js. It replaces raw SQL with type-safe function calls.
- Three components: 
	- Prisma Schema (data model), 
	- Prisma Client  
		- [[api]]
	- Prisma Migrate

```
+------------------+       +------------------+       +------------------+
|  Your App Code   | ----> |  Prisma Client   | ----> |    Database      |
|  (TypeScript)    |       |  (Generated API) |       |  (Postgres, etc) |
+------------------+       +------------------+       +------------------+
                                    |
                           reads schema from
                                    |
                           +------------------+
                           | schema.prisma    |
                           +------------------+
```

- Prisma Client is ==auto-generated== from your schema. Every time you change the schema, you regenerate the client, and it reflects your exact data model with full type safety.

# Setup

- Install Prisma as a dev dependency and initialize the project.

```bash
npm install prisma --save-dev
npx prisma init
```

- This creates `prisma/schema.prisma` and a `.env` file with a placeholder `DATABASE_URL`.
- Set the database URL in `.env`:

```env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

- Install the Prisma Client library your app code imports:

```bash
npm install @prisma/client
```

# Schema

- The schema file (`prisma/schema.prisma`) defines your data source, generator, and models.
- Uses its own DSL, not TypeScript.

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

- `generator` tells Prisma what to output. `prisma-client-js` generates the TypeScript client.
- `datasource` points to your database. `provider` can be `postgresql`, `mysql`, `sqlite`, `mongodb`, `sqlserver`.

# Models

- A ==model== maps to a database table. Each field maps to a column.

```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  createdAt DateTime @default(now())
}
```

**Field structure**
- `fieldName  Type  Modifiers  Attributes`

**Scalar types**
- `String`, `Int`, `Float`, `Boolean`, `DateTime`, `BigInt`, `Decimal`, `Bytes`, `Json`.

**Type modifiers**
- `String?` — optional (nullable).
- `Post[]` — list (one-to-many relation).

**Attributes**
- `@id` — primary key.
- `@unique` — unique constraint.
- `@default(value)` — default value. Accepts `autoincrement()`, `now()`, `uuid()`, `cuid()`, or a literal.
- `@map("column_name")` — map field to a different column name in the database.
- `@updatedAt` — auto-updates to current timestamp on every update.
- `@@map("table_name")` — map model to a different table name (double `@@` = model-level).
- `@@unique([field1, field2])` — composite unique constraint.
- `@@index([field1, field2])` — composite index.

# Enums

- Define a fixed set of values.

```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}
```

- Reference it as a type in any model: `role Role @default(USER)`.

# Relations

- Relations connect models. Prisma uses a `@relation` attribute to define the foreign key.

**One-to-Many**

```prisma
model User {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id])
  authorId Int
}
```

- `Post` holds the foreign key (`authorId`). `User` holds the list (`posts`).
- `fields` = the FK column on this model. `references` = the PK on the other model.

**One-to-One**

```prisma
model User {
  id      Int      @id @default(autoincrement())
  profile Profile?
}

model Profile {
  id     Int  @id @default(autoincrement())
  user   User @relation(fields: [userId], references: [id])
  userId Int  @unique
}
```

- Same as one-to-many, but the FK field has `@unique` and the reverse side is singular (no `[]`).

**Many-to-Many**

```prisma
model Post {
  id         Int        @id @default(autoincrement())
  categories Category[]
}

model Category {
  id    Int    @id @default(autoincrement())
  posts Post[]
}
```

- ==Implicit== many-to-many: Prisma auto-creates the join table. Both sides hold a list.
- For ==explicit== many-to-many (when you need extra fields on the join), create the join model yourself:

```prisma
model Post {
  id         Int              @id @default(autoincrement())
  categories CategoriesOnPosts[]
}

model Category {
  id    Int              @id @default(autoincrement())
  posts CategoriesOnPosts[]
}

model CategoriesOnPosts {
  post       Post     @relation(fields: [postId], references: [id])
  postId     Int
  category   Category @relation(fields: [categoryId], references: [id])
  categoryId Int
  assignedAt DateTime @default(now())

  @@id([postId, categoryId])
}
```

**Self-Relation**

```prisma
model Employee {
  id        Int        @id @default(autoincrement())
  name      String
  manager   Employee?  @relation("Management", fields: [managerId], references: [id])
  managerId Int?
  reports   Employee[] @relation("Management")
}
```

- A model that references itself. The `@relation` name string disambiguates the two sides.

**Referential Actions**

```prisma
model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId Int
}
```

- `onDelete` / `onUpdate` control what happens when the referenced record is deleted or updated.
- Options: `Cascade`, `SetNull`, `Restrict`, `NoAction`, `SetDefault`.

# Migrations

- Migrations sync your schema changes to the database.

```bash
# create and apply a migration
npx prisma migrate dev --name init

# apply pending migrations in production
npx prisma migrate deploy

# reset database (drop + recreate + apply all migrations)
npx prisma migrate reset
```

- `migrate dev` compares your schema to the current database state, generates a SQL migration file in `prisma/migrations/`, and applies it.
- Every migration is a timestamped folder containing a `migration.sql` file. These are committed to version control.
- After running a migration, Prisma automatically regenerates the client.

```bash
# manually regenerate client without migrating
npx prisma generate
```

- `prisma db push` syncs schema to database without creating a migration file. Use for prototyping only, not production.

# Prisma Client

- Import and instantiate the client.

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
```

- Instantiate once and reuse. In a web server, create it at startup, not per-request.

# Create

```typescript
// create one
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
  },
});

// create with nested relation
const user = await prisma.user.create({
  data: {
    email: "bob@example.com",
    posts: {
      create: [
        { title: "First Post" },
        { title: "Second Post" },
      ],
    },
  },
});

// create many
const count = await prisma.user.createMany({
  data: [
    { email: "a@example.com" },
    { email: "b@example.com" },
  ],
  skipDuplicates: true,
});
```

- `create` returns the created record. `createMany` returns a count.

# Read

```typescript
// find by unique field
const user = await prisma.user.findUnique({
  where: { email: "alice@example.com" },
});

// find first match
const user = await prisma.user.findFirst({
  where: { role: "ADMIN" },
});

// find many
const users = await prisma.user.findMany({
  where: { role: "USER" },
});
```

- `findUnique` returns `null` if not found. Only works on `@id` or `@unique` fields.
- `findFirst` returns `null` if not found. Works with any filter.
- `findMany` returns `[]` if nothing matches.
- `findUniqueOrThrow` and `findFirstOrThrow` throw instead of returning `null`.

# Update

```typescript
// update one
const user = await prisma.user.update({
  where: { email: "alice@example.com" },
  data: { name: "Alice Updated" },
});

// update many
const count = await prisma.user.updateMany({
  where: { role: "USER" },
  data: { role: "ADMIN" },
});

// upsert (update if exists, create if not)
const user = await prisma.user.upsert({
  where: { email: "alice@example.com" },
  update: { name: "Alice" },
  create: { email: "alice@example.com", name: "Alice" },
});
```

- `update` requires a unique `where`. Throws if not found.
- `updateMany` returns a count.

# Delete

```typescript
// delete one
const user = await prisma.user.delete({
  where: { email: "alice@example.com" },
});

// delete many
const count = await prisma.user.deleteMany({
  where: { role: "USER" },
});

// delete all records in a table
await prisma.user.deleteMany();
```

# Filtering

- The `where` clause supports operators beyond equality.

```typescript
const users = await prisma.user.findMany({
  where: {
    email: { contains: "example.com" },
    name: { startsWith: "A" },
    createdAt: { gte: new Date("2025-01-01") },
    role: { in: ["ADMIN", "MODERATOR"] },
  },
});
```

**Comparison operators**
- `equals`, `not`, `gt`, `gte`, `lt`, `lte`.

**String operators**
- `contains`, `startsWith`, `endsWith`. Add `mode: "insensitive"` for case-insensitive.

**List operators**
- `in`, `notIn`. Match against an array of values.

**Logical operators**
- `AND`, `OR`, `NOT`. Combine multiple conditions.

```typescript
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: { contains: "admin" } },
      { role: "ADMIN" },
    ],
  },
});
```

**Relation filters**
- `some`, `every`, `none`. Filter based on related records.

```typescript
// users who have at least one published post
const users = await prisma.user.findMany({
  where: {
    posts: { some: { published: true } },
  },
});
```

# Sorting and Pagination

```typescript
const users = await prisma.user.findMany({
  orderBy: { createdAt: "desc" },
  skip: 20,
  take: 10,
});
```

- `orderBy` accepts `"asc"` or `"desc"`. Pass an array for multi-field sorting.
- `skip` offsets by N records. `take` limits to N records. Together they implement offset pagination.

**Cursor-based pagination**

```typescript
const users = await prisma.user.findMany({
  take: 10,
  cursor: { id: 42 },
  skip: 1, // skip the cursor record itself
  orderBy: { id: "asc" },
});
```

- More performant than offset pagination on large datasets.

# Select and Include

- By default, queries return all scalar fields but no relations.

```typescript
// select specific fields only
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: {
    email: true,
    name: true,
  },
});

// include related records
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: true,
  },
});

// nested select inside include
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: {
      select: { title: true },
      where: { published: true },
      orderBy: { createdAt: "desc" },
      take: 5,
    },
  },
});
```

- `select` and `include` are mutually exclusive at the same level. Use one or the other.
- `select` returns only specified fields. `include` returns all scalar fields plus the specified relations.

# Aggregations

```typescript
// count
const count = await prisma.user.count({
  where: { role: "ADMIN" },
});

// aggregate
const result = await prisma.post.aggregate({
  _avg: { views: true },
  _sum: { views: true },
  _min: { views: true },
  _max: { views: true },
  _count: true,
});

// group by
const grouped = await prisma.post.groupBy({
  by: ["published"],
  _count: true,
  _avg: { views: true },
  having: {
    views: { _avg: { gt: 100 } },
  },
});
```

# Transactions

- Prisma guarantees that all operations inside a transaction either all succeed or all fail.

**Sequential transaction**

```typescript
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: "a@b.com" } }),
  prisma.post.create({ data: { title: "Hello", authorId: 1 } }),
]);
```

- Pass an array of Prisma operations. They execute sequentially in a single database transaction.

**Interactive transaction**

```typescript
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id: 1 } });
  if (!user) throw new Error("User not found");

  const updated = await tx.user.update({
    where: { id: 1 },
    data: { balance: { decrement: 100 } },
  });

  return updated;
});
```

- Pass an async function. `tx` is a transactional Prisma Client. If the function throws, the entire transaction rolls back.
- Use interactive transactions when later operations depend on the results of earlier ones.

# Nested Writes

- Create, update, or connect related records inside a single operation.

```typescript
// connect to existing relation
const post = await prisma.post.create({
  data: {
    title: "New Post",
    author: { connect: { id: 1 } },
  },
});

// disconnect a relation
await prisma.post.update({
  where: { id: 1 },
  data: {
    author: { disconnect: true },
  },
});

// create or connect
const post = await prisma.post.create({
  data: {
    title: "New Post",
    author: {
      connectOrCreate: {
        where: { email: "alice@example.com" },
        create: { email: "alice@example.com", name: "Alice" },
      },
    },
  },
});
```

**Nested write keywords**
- `create` — create a new related record.
- `connect` — link to an existing record by unique field.
- `connectOrCreate` — connect if exists, otherwise create.
- `disconnect` — remove the link (sets FK to null).
- `set` — replace the entire list of relations (many-to-many).
- `delete` — delete the related record.
- `update` — update the related record.
- `upsert` — update the related record if it exists, create if not.

# Raw Queries

- Escape hatch for queries Prisma Client cannot express.

```typescript
// raw SELECT
const users = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE email = ${email}
`;

// raw INSERT/UPDATE/DELETE
const count = await prisma.$executeRaw`
  UPDATE "User" SET name = ${name} WHERE id = ${id}
`;
```

- Uses tagged template literals. Variables are automatically parameterized (SQL injection safe).
- `$queryRaw` returns rows. `$executeRaw` returns the number of affected rows.

# Middleware

- ==Middleware== intercepts every query before or after execution.

```typescript
prisma.$use(async (params, next) => {
  const before = Date.now();
  const result = await next(params);
  const after = Date.now();
  console.log(`${params.model}.${params.action} took ${after - before}ms`);
  return result;
});
```

- `params` contains `model`, `action`, `args`. Modify `params.args` to alter the query before it runs.
- Common uses: soft deletes, logging, automatic timestamps.

**Soft delete example**

```typescript
prisma.$use(async (params, next) => {
  if (params.model === "Post") {
    if (params.action === "delete") {
      params.action = "update";
      params.args.data = { deleted: true };
    }
    if (params.action === "findMany") {
      params.args.where = { ...params.args.where, deleted: false };
    }
  }
  return next(params);
});
```

# Prisma Studio

- A GUI to browse and edit your database.

```bash
npx prisma studio
```

- Opens a web UI on `localhost:5555`. View, create, update, delete records directly.

# CLI Reference

```bash
npx prisma init              # scaffold schema + .env
npx prisma generate          # regenerate client from schema
npx prisma migrate dev       # create + apply migration (dev)
npx prisma migrate deploy    # apply pending migrations (prod)
npx prisma migrate reset     # drop db + reapply all migrations
npx prisma db push           # push schema without migration file
npx prisma db pull           # introspect existing db into schema
npx prisma db seed           # run seed script
npx prisma studio            # open GUI
npx prisma format            # format schema file
npx prisma validate          # validate schema syntax
```

# Seeding

- Populate the database with initial data.
- Add a seed script to `package.json`:

```json
{
  "prisma": {
    "seed": "ts-node prisma/seed.ts"
  }
}
```

```typescript
// prisma/seed.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  await prisma.user.createMany({
    data: [
      { email: "alice@example.com", name: "Alice", role: "ADMIN" },
      { email: "bob@example.com", name: "Bob", role: "USER" },
    ],
  });
}

main()
  .then(() => prisma.$disconnect())
  .catch((e) => {
    console.error(e);
    prisma.$disconnect();
    process.exit(1);
  });
```

```bash
npx prisma db seed
```

- `prisma migrate reset` automatically runs the seed script after resetting.