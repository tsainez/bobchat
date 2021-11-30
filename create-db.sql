-- create-db.sql
-- Everything in this script should be Data Definition Language (DDL)
-- Run ONCE to create and refresh database from scratch.
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users(
    username char(32) NOT NULL,
    PASSWORD char(32) NOT NULL,
    email char(32) NOT NULL,
    did int(8),
    PRIMARY KEY (username)
);
DROP TABLE IF EXISTS den;
CREATE TABLE IF NOT EXISTS den(
    id int(8),
    name char(32) NOT NULL,
    description char(256) NOT NULL
);
DROP TABLE IF EXISTS c_likes;
CREATE TABLE IF NOT EXISTS c_likes(
    username char(32) NOT NULL,
    cid int(8) NOT NULL
);
DROP TABLE IF EXISTS followers;
CREATE TABLE IF NOT EXISTS followers(
    username char(32) NOT NULL,
    follower char(32) NOT NULL
);
-- TODO: If a user makes a post, then it is under their profile instead of under a den.
DROP TABLE IF EXISTS posts;
CREATE TABLE IF NOT EXISTS posts(
    username char(32) NOT NULL,
    content char(4096) NOT NULL,
    pid int(8) NOT NULL,
    time date NOT NULL,
    did int(8) NOT NULL
);
DROP TABLE IF EXISTS comments;
CREATE TABLE IF NOT EXISTS comments(
    username char(32) NOT NULL,
    description char(256) NOT NULL,
    cid int(8) NOT NULL,
    pid int(8) NOT NULL
);
DROP TABLE IF EXISTS likes;
CREATE TABLE IF NOT EXISTS likes(
    username char(32) NOT NULL,
    pid int(8) NOT NULL
);
-- Populating database is done in populate.sql.