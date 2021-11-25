-- A script containing the SQL queries and data modification statements (INSERT/UPDATE/DELETE)
-- specified in your use-case diagram. There should be at least 20 SQL statements and they
-- should display diversity, i.e., queries with different format and modification statements
-- of different type.
-- Run by typing 'sqlite3 db.sqlite < db.sql'
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
-- USER WANTS TO UPDATE THEIR EMAIL
-- Hardcoded because we want to implement part of this with our front end technology.
INSERT INTO users
VALUES("user", "password", "user@gmail.com", NULL),
    (
        "nathan",
        "password",
        "nvasquez12@ucmerced.edu",
        2
    ),
    -- This user is part of Den 2, which is "linguistics club"
    ("tony", "password", "asainez@ucmerced.edu", 2),
    ("apsara", "password", "afite@ucmerced.edu", NULL),
    ("mithil", "password", "mpatel@ucmerced.edu", 4),
    ("hareez", "password", "hhussein@ucmerced.edu", 5);
-- Updating a user's email...
UPDATE users
SET email = 'new@gmail.com'
WHERE username = 'user'
    AND PASSWORD = 'correct';
INSERT INTO den(id, name, description)
VALUES (1, "ACM", "lorem ipsum"),
    (2, "Linguistics Club", "sit amen"),
    (3, "Medicine Club", "adipiscing elit"),
    (4, "Math & Science Club", "dignissim diam"),
    (
        5,
        "Intramural Basketball Club",
        "metus eleifend"
    );
-- If a post does not have a DID, then it is a post on a user's own profile. 
-- This is similar to tweeting on your profile instead of replying
INSERT INTO posts
VALUES (
        "user",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        1,
        1,
        -- You may notice that the time here is just sequentially increasing.
        -- We plan to make it so that the time is linked with the time the post was
        -- made, which would just be based on the server's clock (or perhaps synced
        -- to the user's computer clock or timezone.)
        1
    ),
    (
        "nathan",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        2,
        2,
        2
    ),
    (
        "tony",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        3,
        3,
        3
    ),
    (
        "apsara",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        4,
        4,
        4
    ),
    (
        "mithil",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        5,
        5,
        5
    );
-- Updating a user's password...
-- We assume that in our Python code, if it passes authentication then 
-- We will execute this query where all the quotes are filled out by a function
-- and replaced by way of {} and .format. 
UPDATE users
SET email = "new"
WHERE username = "user"
    AND PASSWORD = "correct"
    AND email = "correct";
-- Creating a view that stores a user's username, as well as all their posts information.
-- This would be useful if you wanted to execute a query such as "what are all this user's posts?"
-- Or perhaps searching all of a user's posts for a specific keyword. 
-- CREATE VIEW vw_combined AS 
--    SELECT * FROM TABLE1
--    UNION ALL
--    SELECT * FROM TABLE2
-- requires that there be the same number of columns, and the data types match at each position
DROP VIEW IF EXISTS posts_from_user;
CREATE VIEW IF NOT EXISTS posts_from_user AS
SELECT *
FROM posts
WHERE username == "user";
-- Theoretically could also be done by joining posts and user table.