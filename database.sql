DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls(id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at timestamp
);

INSERT INTO urls (name, created_at) VALUES ('https://www.vk.com', '2023-05-15T17:48:02.034390'::timestamp);