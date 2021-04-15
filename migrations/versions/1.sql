CREATE TABLE IF NOT EXISTS stories_schema.stories (
    id varchar(255) primary key,
    created_at timestamp,
    grapher_name text,
    name text,
    description text,
    duration integer,
    file_type varchar(20),
    file bytea,
    state varchar(20)
);