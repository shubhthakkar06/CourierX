-- ============================================================
-- CourierX — MySQL Database Setup Script
-- Run this once against your MySQL server before starting the app.
-- ============================================================

CREATE DATABASE IF NOT EXISTS Project;
USE Project;

-- Users table
CREATE TABLE IF NOT EXISTS user (
    userid       VARCHAR(31)  NOT NULL PRIMARY KEY,
    username     VARCHAR(30)  NOT NULL,
    password     VARCHAR(50)  NOT NULL,
    DOB          DATE,
    recoverycode INT          UNIQUE
);

-- Addresses table
CREATE TABLE IF NOT EXISTS addresses (
    userid           VARCHAR(31),
    pincode          CHAR(6),
    reciever_name    VARCHAR(30),
    reciever_city    VARCHAR(25),
    reciever_street  VARCHAR(25),
    reciever_house   VARCHAR(25),
    reciever_no      CHAR(10),
    FOREIGN KEY (userid) REFERENCES user(userid)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    orderID    INT          NOT NULL PRIMARY KEY,
    address    VARCHAR(150),
    weight     DECIMAL(5,2),
    price      VARCHAR(10),
    order_date VARCHAR(20),
    userid     VARCHAR(31),
    FOREIGN KEY (userid) REFERENCES user(userid)
);

-- Delivery tracking table
CREATE TABLE IF NOT EXISTS delivery (
    orderid     INT,
    delivery_no BIGINT,
    FOREIGN KEY (orderid) REFERENCES orders(orderID)
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    review  VARCHAR(20),
    orderid INT,
    FOREIGN KEY (orderid) REFERENCES orders(orderID)
);

-- Weight-price scale table
CREATE TABLE IF NOT EXISTS wtscale (
    min_weight INT,
    max_weight INT,
    price      INT
);

-- Wrong password attempt tracker (single row)
CREATE TABLE IF NOT EXISTS wpd (
    attemps INT DEFAULT 1
);
INSERT IGNORE INTO wpd VALUES (1);

-- Seed weight-price scale
INSERT IGNORE INTO wtscale VALUES
  (2, 4, 500), (4, 6, 1000), (6, 8, 1500), (8, 10, 2000),
  (10, 12, 2500), (12, 14, 3000), (14, 16, 3500), (16, 18, 4000),
  (18, 20, 4500), (20, 22, 5000), (22, 24, 5500), (24, 26, 6000),
  (26, 28, 6500), (28, 30, 7000);
