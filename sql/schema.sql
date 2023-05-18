BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "publication" (
	"id"	INT,
	"isbn"	CHAR(13),
	"title"	VARCHAR(128) NOT NULL,
	"year"	INT,
	"edition"	VARCHAR(128),
	"publisher"	VARCHAR(128),
	"verified"	BOOLEAN NOT NULL DEFAULT False,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "file" (
	"md5"	CHAR(32) NOT NULL,
	"path"	VARCHAR(256),
	"publication"	int,
	PRIMARY KEY("md5"),
	FOREIGN KEY("publication") REFERENCES "publication"("id")
);
CREATE TABLE IF NOT EXISTS "author" (
	"id"	INT,
	"first_name"	VARCHAR(64) NOT NULL,
	"middle_name"	VARCHAR(64),
	"last_name"	VARCHAR(64) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "topic" (
	"id"	INT,
	"name"	VARCHAR(128) NOT NULL,
	UNIQUE("name"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "repository" (
	"id"	INT,
	"description"	TEXT,
	"path"	VARCHAR(256),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "author_pub" (
	"id_author"	INT NOT NULL,
	"id_pub"	INT NOT NULL,
	PRIMARY KEY("id_author","id_pub"),
	FOREIGN KEY("id_pub") REFERENCES "publication"("id"),
	FOREIGN KEY("id_author") REFERENCES "author"("id")
);
CREATE TABLE IF NOT EXISTS "topic_pub" (
	"id_topic"	INT NOT NULL,
	"id_pub"	INT NOT NULL,
	PRIMARY KEY("id_topic","id_pub"),
	FOREIGN KEY("id_pub") REFERENCES "publication"("id"),
	FOREIGN KEY("id_topic") REFERENCES "topic"("id")
);
CREATE TABLE IF NOT EXISTS "repository_file" (
	"id_repo"	INT NOT NULL,
	"id_file"	CHAR(32) NOT NULL,
	PRIMARY KEY("id_repo","id_file"),
	FOREIGN KEY("id_repo") REFERENCES "repository"("id"),
	FOREIGN KEY("id_file") REFERENCES "file"("md5")
);
COMMIT;
