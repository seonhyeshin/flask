drop table if exists searchlist;
create table searchlist (
	no integer PRIMARY KEY AUTOINCREMENT,
	code char(30) not null,
	time char(30) not null,
	price char(30) not null,
	change char(30) not null);
