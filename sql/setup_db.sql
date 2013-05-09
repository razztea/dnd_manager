/*
    This contains the sql necessary to create the database
    and set up the root user.
*/

create database if not exists rpg_manager;

create user 'rpg_root'@'localhost' identified by 'rpg_root';
grant all on rpg_manager.* to 'rpg_root'@'localhost';

