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

create table worlds (
    id              varchar(36),
    master_username varchar(100),
    name            varchar(40),
    description     text,
    primary key (id),
    constraint foreign key (master_username) references users (username) on delete cascade
);

create table races (
    id              varchar(36),
    world_id        varchar(36),
    name            varchar(20),
    class_limit     int,
    description     text,
    special         text,
    primary key (id),
    constraint foreign key (world_id) references worlds (id) on delete cascade
);

create table characters (
    id              varchar(36),
    player_username varchar(100),
    world_id        varchar(36),
    race_id         varchar(36),
    name            varchar(40),
    primary key (id),
    constraint foreign key (player_username) references users (username) on delete cascade,
    constraint foreign key (world_id) references worlds (id),
    constraint foreign key (race_id) references races (id)
);

create table attributes (
    id              varchar(36),
    world_id      varchar(36),
    name            varchar(20),
    min             int,
    max             int,
    primary key (id),
    constraint foreign key (world_id) references worlds (id) on delete cascade
);

create table race_attribute_requirements (
    id              varchar(36),
    race_id         varchar(36),
    attribute_id    varchar(36),
    max             int,
    min             int,
    modifier        int,
    primary key (id),
    constraint foreign key (race_id) references races (id) on delete cascade,
    constraint foreign key (attribute_id) references attributes (id) on delete cascade
);

create table classes (
    id              varchar(36),
    world_id      varchar(36),
    name            varchar(20),
    description     text,
    primary key (id),
    constraint foreign key (world_id) references worlds (id) on delete cascade
);

create table class_attribute_requirements (
    id              varchar(36),
    class_id        varchar(36),
    attribute_id    varchar(36),
    max             int,
    min             int,
    primary key (id),
    constraint foreign key (class_id) references classes (id) on delete cascade,
    constraint foreign key (attribute_id) references attributes (id) on delete cascade
);

create table race_class_requirements (
    id              varchar(36),
    race_id         varchar(36),
    class_id        varchar(36),
    max_level       int,
    primary key (id),
    constraint foreign key (race_id) references races (id) on delete cascade,
    constraint foreign key (class_id) references classes (id) on delete cascade
);

create table character_attributes (
    id              varchar(36),
    character_id    varchar(36),
    attribute_id    varchar(36),
    value           int,
    primary key (id),
    constraint foreign key (character_id) references characters (id) on delete cascade,
    constraint foreign key (attribute_id) references attributes (id) on delete cascade
);

create table character_classes (
    id              varchar(36),
    character_id    varchar(36),
    class_id        varchar(36),
    level           int,
    primary key (id),
    constraint foreign key (character_id) references characters (id) on delete cascade,
    constraint foreign key (class_id) references classes (id) on delete cascade
);
