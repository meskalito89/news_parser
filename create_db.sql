drop table if exists items;
create table items (
    id integer primary key autoincrement,
    res_id integer not null,
    link varchar(255) not null,
    title text not null,
    content text not null,
    nd_date integer not null,
    s_date timestamp default current_timestamp not null,
    not_date date not null,
    foreign key(res_id) references resource(resource_id)
);

--drop table if exists resource;
--create table resource (
--    RESOURCE_ID integer primary key autoincrement,
--    RESOURCE_NAME varchar(255),
--    RESOURCE_URL varchar(255),
--    top_tag varchar(255) not null,
--    bottom_tag varchar(255) not null,
--    title_cut varchar(255) not null,
--    date_cut varchar(255) not null
--);

