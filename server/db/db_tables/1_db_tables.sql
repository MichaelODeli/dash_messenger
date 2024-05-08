-- create DATABASE messenger;

create table "users" (
  "id" serial primary key,
  "username" varchar(255) not null,
  "email" varchar(255) not null,
  "password" varchar(255) not null,
  "created_at" timestamp not null default NOW(),
  "updated_at" timestamp not null default NOW(),
  UNIQUE(username),
  UNIQUE(email)
);

create table "conversations" (
  "id" serial primary key,
  "conversation_name" varchar(255) null,
  "personal" boolean not null,
  "created_at" timestamp not null default NOW(),
  "updated_at" timestamp not null default NOW()
);

create table "messages" (
  "id" serial primary key,
  "from_id" INTEGER not null,
  "conversation_id" INTEGER not null,
  "content" varchar(4000) not null,
  "content_type" varchar(25) not null default 'text',
  "created_at" timestamp not null default NOW(),
  "updated_at" timestamp not null default NOW(),
  FOREIGN KEY (from_id) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
);

create table "conversation_members" (
  "conversation_id" integer not null,
  "user_id" integer not null,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
);

create table "tokens" (
  "id" serial primary key,
  "token" varchar(255) not null,
  "user_id" INTEGER not null,
  "status" varchar(25) not null,
  "created_at" timestamp not null default NOW(),
  "valid_until" timestamp not null,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  UNIQUE(token)
);