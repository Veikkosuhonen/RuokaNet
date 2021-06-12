CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    balance DECIMAL
);

CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    shopname TEXT UNIQUE,
    n_owners INT
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    itemname TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    itemid INT REFERENCES items,
    price DECIMAL,
    shopId INT REFERENCES shops,
    UNIQUE (itemid, shopid)
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    shopid INT REFERENCES shops,
    userid INT REFERENCES users,
    itemid INT REFERENCES items,
    amount INT,
    price DECIMAL,
    closetime TIMESTAMP
);

CREATE TABLE shop_owners (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users,
    shopid INT REFERENCES shops,
    UNIQUE (userid, shopid)
);

CREATE TABLE invites (
    id SERIAL PRIMARY KEY,
    senderid INT REFERENCES users,
    receiverid INT REFERENCES users,
    shopid INT REFERENCES shops,
    invitestatus INT,
    UNIQUE (senderid, receiverid, shopid, invitestatus)
);

CREATE TABLE shop_inventory (
    shopid INT REFERENCES shops,
    itemid INT REFERENCES items,
    quantity INT,
    UNIQUE (shopid, itemid)
);

CREATE TABLE user_inventory (
    userid INT REFERENCES users,
    itemid INT REFERENCES items,
    quantity INT,
    UNIQUE (userid, itemid)
);

CREATE TABLE user_activity (
    userid INT REFERENCES users,
    description TEXT,
    closetime TIMESTAMP
)