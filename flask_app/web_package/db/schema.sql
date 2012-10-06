drop table if exists users;
create table users(
	username string primary key,
	hash string not null,
	salt string not null
);

drop table if exists posts;
create table posts(
	id integer primary key autoincrement,
	title string not null,
	text string not null
);