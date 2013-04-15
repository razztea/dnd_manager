/*
    This will contain the sql that needs to be run
    to create the database and all tables
*/

create table users (
    username        varchar(100),
    password        varchar(40),
    master          bool,
    primary key (username)
);

create table dungeons (
    id              varchar(36),
    master_username varchar(100),
    name            varchar(40),
    primary key (id),
    constraint foreign key (master_username) references users (username)
);

create table character_attributes (
    id              varchar(36),
    dungeon_id      varchar(36),
    name            varchar(20),
    min             int,
    max             int,
    primary key (id),
    constraint foreign key (dungeon_id) references dungeons (id)
);

create table character_races (
    id              varchar(36),
    dungeon_id      varchar(36),
    name            varchar(20),
    class_limit     int,
    description     text,
    special         text,
    primary key (id),
    constraint foreign key (dungeon_id) references dungeons (id)
);

create table race_modifiers (
    id              varchar(36),
    race_id         varchar(36),
    attribute_id    varchar(36),
    primary key (id),
    constraint foreign key (race_id) references character_races (id),
    constraint foreign key (attribute_id) references character_attributes (id)
);

create table race_attribute_requirements (
    id              varchar(36),
    race_id         varchar(36),
    attribute_id    varchar(36),
    max             int,
    min             int,
    primary key (id),
    constraint foreign key (race_id) references character_races (id),
    constraint foreign key (attribute_id) references character_attributes (id)
);

create table character_classes (
    id              varchar(36),
    dungeon_id      varchar(36),
    name            varchar(20),
    description     text,
    primary key (id),
    constraint foreign key (dungeon_id) references dungeons (id)
);

create table class_attribute_requirements (
    id              varchar(36),
    class_id        varchar(36),
    attribute_id    varchar(36),
    max             int,
    min             int,
    primary key (id),
    constraint foreign key (class_id) references character_classes (id),
    constraint foreign key (attribute_id) references character_attributes (id)
);

create table race_class_requirements (
    id              varchar(36),
    race_id         varchar(36),
    class_id        varchar(36),
    max_level       int,
    primary key (id),
    constraint foreign key (race_id) references character_races (id),
    constraint foreign key (class_id) references character_classes (id)
);
