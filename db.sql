use finapp;
CREATE TABLE IF NOT EXISTS transaction (
    tr_id INT AUTO_INCREMENT PRIMARY KEY,
    tr_date DATE NOT NULL,
    account VARCHAR(30) NOT NULL,
    remarks VARCHAR(30),
    tr_type ENUM('CR', 'DR') NOT NULL
);


CREATE TABLE IF NOT EXISTS budget (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month VARCHAR(30) NOT NULL,
    name VARCHAR(30) NOT NULL,
    estimated_amount INT NOT NULL DEFAULT 0,
    status VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS account (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name varchar(255) NOT NULL
)

