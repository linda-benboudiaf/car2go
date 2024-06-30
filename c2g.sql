-- Table for storing car information
CREATE TABLE cars (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INT NOT NULL,
    availability BOOLEAN DEFAULT TRUE
);

-- Table for storing user information
CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Table for storing reservation information
CREATE TABLE reservations (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    car_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id)
);
