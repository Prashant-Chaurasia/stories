CREATE TABLE IF NOT EXISTS stories_schema.stories (
    id varchar(255) primary key,
    created_at timestamp,
    state varchar(20),
    grapher_name text,
    name text,
    description text,
    duration numeric,
    file_type varchar(20),
    file bytea,
    latitude numeric,
    longitude numeric
);