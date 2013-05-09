/*
    This file holds some useful inserts for testing
*/

insert into users (username, password, master)
    values ('da_master', AES_ENCRYPT('1234', username), TRUE);

insert into users (username, password, master)
    values ('da_player', AES_ENCRYPT('5678', username), FALSE);
