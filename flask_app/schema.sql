drop table if exists users;
create table users(
	username string primary key,
	hash string not null,
	salt string not null,
	latitude integer,
	longitude integer
)