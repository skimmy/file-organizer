BEGIN;
CREATE TABLE publication (
    id INT PRIMARY KEY,
    isbn CHAR(13),
    title VARCHAR(128) NOT NULL,
    year INT,
    edition VARCHAR(128),
    publisher VARCHAR(128),
    verified BOOLEAN NOT NULL DEFAULT False
);
CREATE TABLE file (
    md5 CHAR(32) NOT NULL,
    path VARCHAR(256),
    publication int,
    PRIMARY KEY(md5),
    FOREIGN KEY(publication) REFERENCES publication(id)
);
CREATE TABLE author (
    id INT PRIMARY KEY, 
    first_name VARCHAR(64) NOT NULL,
    middle_name VARCHAR(64),
    last_name VARCHAR(64) NOT NULL
);
CREATE TABLE topic (
    id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    UNIQUE(name)
);
CREATE TABLE repository(
    id INT PRIMARY KEY,
    description TEXT,
    path VARCHAR(256)
);
CREATE TABLE author_pub (
    id_author INT NOT NULL,
    id_pub INT NOT NULL,
    PRIMARY KEY(id_author, id_pub),
    FOREIGN KEY(id_author) REFERENCES author(id),
    FOREIGN KEY(id_pub) REFERENCES publication(id)
);
CREATE TABLE topic_pub(
    id_topic INT NOT NULL,
    id_pub INT NOT NULL,
    PRIMARY KEY(id_topic, id_pub),
    FOREIGN KEY(id_topic) REFERENCES topic(id),
    FOREIGN KEY(id_pub) REFERENCES publication(id)
);
CREATE TABLE repository_file(
    id_repo INT NOT NULL,
    id_file CHAR(32) NOT NULL,
    PRIMARY KEY(id_repo, id_file),
    FOREIGN KEY(id_repo) REFERENCES repository(id),
    FOREIGN KEY(id_file) REFERENCES file(md5)
);

COMMIT;
