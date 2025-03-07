-- ! This is the init script for postgres, do not delete
CREATE SCHEMA static_files_schema;
CREATE SCHEMA match_schema;
CREATE SCHEMA tournament_schema;
CREATE SCHEMA user_schema;

GRANT USAGE ON SCHEMA static_files_schema TO user1;
GRANT USAGE ON SCHEMA match_schema TO user1;
GRANT USAGE ON SCHEMA tournament_schema TO user1;
GRANT USAGE ON SCHEMA user_schema TO user1;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA static_files_schema TO user1;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA match_schema TO user1;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA tournament_schema TO user1;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA user_schema TO user1;