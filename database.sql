CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

INSERT INTO urls (name, created_at) VALUES ('https://www.vk.com', '2023-04-24T18:11:44.443611'::timestamp);
INSERT INTO urls (name, created_at) VALUES ('https://www.warcraft.com', '2023-04-24T18:29:23.792500'::timestamp);
INSERT INTO urls (name, created_at) VALUES ('https://www.vk8.com', '2023-04-24T19:35:47.248273'::timestamp);
INSERT INTO urls (name, created_at) VALUES ('https://www.dota2.com', '2023-04-24T21:11:07.508025'::timestamp);
INSERT INTO urls (name, created_at) VALUES ('https://www.dota3.com', '2023-04-24T21:20:56.288827'::timestamp);
INSERT INTO urls (name, created_at) VALUES ('https://io.hexlet.ru', '2023-04-24T21:21:45.963363'::timestamp);