CREATE TABLE Player
(
    id INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    position VARCHAR(10), 
    age INT, 
    player_height INT,
    player_weight INT
);

CREATE TABLE Season
(
    nba_season INT NOT NULL,
    player_id INT NOT NULL REFERENCES Player(id),
    ppg FLOAT,
    mpg FLOAT,
    fgp FLOAT,
    ftp FLOAT,
    ttp FLOAT,
    fga FLOAT,
    fta FLOAT,
    tpa FLOAT,
    rebound FLOAT,
    assists FLOAT,
    steals FLOAT,
    turnovers FLOAT,
    blocks FLOAT,
    bs_plus_minus FLOAT,
    PRIMARY KEY(nba_season, player_id)
);

CREATE TABLE Performance
(
    nba_season INT NOT NULL,
    player_id INT NOT NULL REFERENCES Player(id),
    game_date DATE NOT NULL,
    player_minutes INT,
    fgp FLOAT,
    ftp FLOAT, 
    ttp FLOAT,
    fga INT,
    fta INT,
    tpa INT,
    rebound INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks INT,
    bs_plus_minus INT,
    PRIMARY KEY(nba_season, player_id, game_date),
    FOREIGN KEY(nba_season, player_id) REFERENCES Season(nba_season, player_id)
)
