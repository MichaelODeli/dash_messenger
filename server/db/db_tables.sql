-- create DATABASE messenger;

create table "users" (
  "id" serial primary key,
  "nickname" varchar(255) not null,
  "email" varchar(255) not null,
  "password" varchar(255) not null,
  "created_at" timestamp not null default NOW(),
  "updated_at" timestamp not null default NOW(),
  UNIQUE(nickname),
  UNIQUE(email)
);

create table "conversations" (
  "id" serial primary key,
  "conversation_name" varchar(255) null,
  "created_at" timestamp not null default NOW(),
  "updated_at" timestamp not null default NOW()
);

create table "messages" (
  "id" serial primary key,
  "from_id" INTEGER not null,
  "to_id" INTEGER null,
  "to_conversation_id" INTEGER null,
  "content" varchar(4000) not null,
  "content_type" varchar(255) not null default 'text',
  "created_at" timestamp not null default NOW(),
  "updated_at" timestamp not null default NOW(),
  FOREIGN KEY (from_id) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (to_id) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (to_conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
);

create table "conversation_members" (
  "conversation_id" serial primary key,
  "user_id" integer not null,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
);

