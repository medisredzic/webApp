DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS itemsSold;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    password TEXT NOT NULL,
    level INTEGER NOT NULL
);

CREATE TABLE items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    itemName TEXT NOT NULL,
    wholesalePrice FLOAT NOT NULL,
    retailPrice FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    barCode INTEGER UNIQUE NOT NULL
);

CREATE TABLE clients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clientName TEXT NOT NULL,
    clientAddress TEXT NOT NULL,
    clientCountry TEXT NOT NULL
);

CREATE TABLE bills(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cashier INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(cashier) REFERENCES user(id)
);

CREATE TABLE itemsSold(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    billId INTEGER NOT NULL,
    itemId INTEGER NOT NULL,
    soldAt FLOAT NOT NULL,
    FOREIGN KEY(billId) REFERENCES bills(id),
    FOREIGN KEY(itemId) REFERENCES items(id)
);