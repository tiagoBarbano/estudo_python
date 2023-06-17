-- Active: 1676159336194@@127.0.0.1@5432@postgres@public
CREATE TABLE users(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT,
    password TEXT,
    email TEXT,
    full_name TEXT,
    disabled BOOLEAN,
    data_criacao Date
);
COMMENT ON TABLE  IS '';
COMMENT ON COLUMN .name IS '';