-- This view may prove useful or not based on whether or not it becomes cumbersome with Flask.
DROP VIEW IF EXISTS posts_from_user;
CREATE VIEW IF NOT EXISTS posts_from_user AS
SELECT *
FROM posts
WHERE username = "user";
-- How many posts did users make between 2019 and 2021?
SELECT username,
    COUNT(*)
FROM posts
WHERE time BETWEEN 2019 AND 2021
GROUP BY username;
-- From those posts, what were the PIDs for the user "user"? Print the PID and content.
SELECT username,
    pid,
    content
FROM posts
WHERE time BETWEEN 2019 AND 2021
    AND username = "user";
-- What posts have keywords "Lorem"?
-- At the moment, it should return all of them.
SELECT pid
FROM posts
WHERE content LIKE "%Lorem%";
-- From those posts, who made them?
SELECT username,
    p1.pid
FROM posts AS p1,
    (
        SELECT pid
        FROM posts
        WHERE content LIKE "%Lorem%"
    ) AS p2
WHERE p1.pid = p2.pid;
-- How about we make it so that user "nathan" likes "user"'s post with PID 1, and "tony"'s post with PID 3?
INSERT INTO likes
VALUES("nathan", "1"),
    ("nathan", "3");
-- How many likes does "user" have?
-- Should return '1'.
SELECT COUNT(*)
FROM posts_from_user,
    likes
WHERE likes.pid = posts_from_user.pid;
-- What if user "nathan" wants to view all the posts he's liked?
-- This query displays that information.
SELECT posts.username,
    posts.pid,
    content
FROM posts,
    likes
WHERE likes.pid = posts.pid
    AND likes.username = "nathan";
-- Which users liked "tony"'s post with PID 3?
SELECT likes.username
FROM posts,
    likes
WHERE likes.pid = posts.pid
    AND posts.pid = "3";
-- It seems as though our project might be more about hooking up the front-end and back-end to work properly
-- more than writing super complex queries. However, if one wants to perform an advanced search that might
-- call for more intellectually challenging queries.