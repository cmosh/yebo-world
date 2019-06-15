create database yebo collate SQL_Latin1_General_CP1_CI_AS
go

create table dbo.greetings
(
	greeting varchar(100),
	language varchar(100),
	id int identity
		constraint greetings_pk
			primary key nonclustered
)
go

create unique index greetings_id_uindex
	on dbo.greetings (id)
go

