CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    shopname TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    balance DECIMAL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    productName TEXT,
    price DECIMAL,
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

CREATE TABLE shop_inventory (
    shopid INT REFERENCES shops,
    productid INT REFERENCES products,
    quantity INT
);

CREATE TABLE user_inventory (
    userid INT REFERENCES users,
    productid INT REFERENCES products,
    quantity INT
);

/*CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    itemname TEXT,
);*/

