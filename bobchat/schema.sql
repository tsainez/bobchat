DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS dens;
DROP TABLE IF EXISTS user_den_assoc;
drop table if exists post_like_assoc;
drop table if exists comments;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    PASSWORD TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email TEXT NOT NULL,
    major TEXT NOT NULL
);
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    den_id INTEGER NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (den_id) REFERENCES dens (id)
);
CREATE TABLE dens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    author_id INTEGER NOT NULL DEFAULT 1,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users (id)
);
CREATE TABLE user_den_assoc(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    den_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (den_id) REFERENCES dens (id)
);
CREATE TABLE post_like_assoc(
    id integer PRIMARY KEY autoincrement,
    user_id integer NOT NULL,
    post_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    unique(user_id, post_id)
);
create table comments(
    id integer primary key autoincrement,
    author_id integer not null,
    post_id integer not null,
    body text not null,
    foreign key (post_id) references posts(id),
    foreign key (author_id) references users(id)
);