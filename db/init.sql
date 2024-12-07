-- Create the movies table
CREATE TABLE movies (
    film_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    duration TEXT NOT NULL,
    director TEXT NOT NULL,
    description TEXT,
    img_link TEXT
);

-- Create the times table
CREATE TABLE times (
    film_id VARCHAR(255) NOT NULL,
    day VARCHAR(50) NOT NULL, -- Use VARCHAR with a specified length instead of TEXT
    time VARCHAR(20) NOT NULL, -- Use VARCHAR for time
    PRIMARY KEY (film_id, day, time),
    FOREIGN KEY (film_id) REFERENCES movies (film_id) ON DELETE CASCADE
);