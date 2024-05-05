insert into "users" ("nickname","email","password") values ('est','Randy_Bins@hotmail.com','id');
insert into "users" ("nickname","email","password") values ('perspiciatis','Bo80@gmail.com','rerum');
insert into "users" ("nickname","email","password") values ('omnis','Antwan_Fahey98@hotmail.com','cumque');
insert into "users" ("nickname","email","password") values ('dolorem','Zion.Bauch@hotmail.com','enim');
insert into "users" ("nickname","email","password") values ('et','Orlo98@gmail.com','et');
insert into "users" ("nickname","email","password") values ('testers','test@test.com','test');


insert into "conversations" ("conversation_name", "personal") values ('personal', true);
insert into "conversations" ("conversation_name", "personal") values ('personal', true);
insert into "conversations" ("conversation_name", "personal") values ('personal', true);
insert into "conversations" ("conversation_name", "personal") values ('personal', true);


insert into "conversation_members" ("conversation_id", "user_id") values (1, 6);
insert into "conversation_members" ("conversation_id", "user_id") values (1, 5);
insert into "conversation_members" ("conversation_id", "user_id") values (2, 6);
insert into "conversation_members" ("conversation_id", "user_id") values (2, 4);


insert into "messages" ("from_id", "conversation_id", "content") values (5, 1, 'hello');
insert into "messages" ("from_id", "conversation_id", "content") values (6, 1, 'same hello');
insert into "messages" ("from_id", "conversation_id", "content") values (5, 1, 'hello');
insert into "messages" ("from_id", "conversation_id", "content") values (6, 1, 'same hello');
insert into "messages" ("from_id", "conversation_id", "content") values (5, 1, 'hello');
insert into "messages" ("from_id", "conversation_id", "content") values (6, 1, 'same hello');


insert into "messages" ("from_id", "conversation_id", "content") values (4, 2, 'hello');
insert into "messages" ("from_id", "conversation_id", "content") values (6, 2, 'same hello');
insert into "messages" ("from_id", "conversation_id", "content") values (4, 2, 'hello');
insert into "messages" ("from_id", "conversation_id", "content") values (6, 2, 'same hello');
insert into "messages" ("from_id", "conversation_id", "content") values (4, 2, 'hello');
insert into "messages" ("from_id", "conversation_id", "content") values (6, 2, 'same hello');
