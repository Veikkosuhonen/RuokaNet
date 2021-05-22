CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    shopname TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    productName TEXT,
    price INT,
    shopId INT REFERENCES shops
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    amount INT,
    productId INT REFERENCES products,
    userId INT REFERENCES users,
    shopId INT REFERENCES shops,
    closeTime TIMESTAMP
);

CREATE TABLE shop_owners (
    id SERIAL PRIMARY KEY,
    userId INT REFERENCES users,
    shopId INT REFERENCES shops
);

CREATE TABLE invites (
    id SERIAL PRIMARY KEY,
    senderid INT REFERENCES users,
    receiverid INT REFERENCES users,
    shopid INT REFERENCES shops,
    invitestatus INT
);

/*CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    itemname TEXT,
);*/

