pragma foreign_keys = on;
DROP TABLE IF EXISTS user_den_assoc;
drop table if exists comments;
DROP TABLE IF EXISTS posts;
drop table if exists post_like_assoc;
DROP TABLE IF EXISTS dens;
drop table if exists users;

CREATE TABLE if not exists users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    PASSWORD TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email TEXT NOT NULL,
    major TEXT NOT NULL
);

CREATE TABLE if not exists dens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    author_id INTEGER NOT NULL DEFAULT 1,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id)
);
CREATE TABLE if not exists posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    den_id INTEGER NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id) on delete cascade,
    FOREIGN KEY (den_id) REFERENCES dens(id) on delete cascade
);

CREATE TABLE if not exists user_den_assoc(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    den_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade,
    FOREIGN KEY (den_id) REFERENCES dens(id) on delete cascade
);
CREATE TABLE if not exists post_like_assoc(
    id integer PRIMARY KEY autoincrement,
    user_id integer NOT NULL,
    post_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade,
    FOREIGN KEY (post_id) REFERENCES posts(id) on delete cascade,
    unique(user_id, post_id)
);
create table if not exists comments(
    id integer primary key autoincrement,
    author_id integer not null,
    post_id integer not null,
    body text not null,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    foreign key (post_id) references posts(id) on delete cascade,
    foreign key (author_id) references users(id)on delete cascade
);

