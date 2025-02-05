-- BOOL is SQL can be either true, false or NULL

-- USERS SERVICE
CREATE SCHEMA [IF NOT EXISTS] users;
CREATE TABLE [IF NOT EXISTS] users.user (
	"id" INTEGER NOT NULL,
	"username" TEXT NOT NULL UNIQUE,
	"email" TEXT UNIQUE, -- See if 42 API fetches student's email adresses make this NOT NULL
	"password" NOT NULL, -- Passwords need to be salted + hashed + form checks (x characters longs / alphanumeric, ect...)
	"avatar" BLOB DEFAULT, -- Need a default avatar OR fetch student PP from 42 API
	"is_online" BOOL NOT NULL,
	"pref_language" TEXT NOT NULL DEFAULT "en", -- This is to be determined with support-language option
	"2FA_enabled" BOOL DEFAULT false,
	"tournament_alias" TEXT,
	PRIMARY KEY ("id")
)

-- MATCH-MACKING
CREATE SCHEMA [IF NOT EXISTS] matches;
CREATE TABLE [IF NOT EXISTS] matches.match (
	"id" INTEGER NOT NULL,
	PRIMARY KEY ("id")

)

-- FRIENDSHIP SERVICE
CREATE SCHEMA [IF NOT EXISTS] friendships;
CREATE TABLE [IF NOT EXISTS] friendships.friendship (
	"id" INTEGER NOT NULL,
	PRIMARY KEY ("id")

)

-- TOURNAMENT
CREATE SCHEMA [IF NOT EXISTS] tournaments;
CREATE TABLE [IF NOT EXISTS] tournaments.tournament (
	"id" INTEGER NOT NULL,
	PRIMARY KEY ("id")

)