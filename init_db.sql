-- 删除现有数据库（如果存在）
DROP DATABASE IF EXISTS DigitalFingerprintDB;

-- 尝试创建数据库，如果不存在的话
CREATE DATABASE IF NOT EXISTS DigitalFingerprintDB;

-- 选择数据库
USE DigitalFingerprintDB;

-- 创建用户信息表
CREATE TABLE users (
    user_id INT(9) UNSIGNED ZEROFILL NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

-- 创建作品信息表
CREATE TABLE works (
    work_id CHAR(11) NOT NULL,
    capture_time DATETIME NOT NULL,
    work_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (work_id)
);

-- 创建数字指纹表
CREATE TABLE digital_fingerprints (
    user_id INT(9) UNSIGNED ZEROFILL NOT NULL,
    work_id CHAR(11) NOT NULL,
    -- 选择 MEDIUMBLOB 而非 BLOB 是因为 BLOB 的最大存储只有 65535 字节，不足以存储大约八万位的数字指纹。
    -- MEDIUMBLOB 可以存储最大约 16MB 的数据，更适合我们的需求。
    digital_fingerprint MEDIUMBLOB NOT NULL,
    distribution_time DATETIME NOT NULL,
    PRIMARY KEY (user_id, work_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (work_id) REFERENCES works(work_id)
);

-- 插入用户信息初始数据
INSERT INTO users (user_id, gender, nickname) VALUES
(575651998, 'Female', 'kristina04'),
(859545852, 'Female', 'georgecrawford'),
(106080058, 'Female', 'fhall'),
(544667600, 'Male', 'monroerobert'),
(609949325, 'Female', 'wcook'),
(124405527, 'Female', 'atkinsangel'),
(109026978, 'Female', 'marysawyer'),
(644998327, 'Male', 'stewartdiana'),
(813841319, 'Male', 'james25'),
(713476406, 'Male', 'nsmith'),
(829594701, 'Female', 'barnettkristen'),
(721608630, 'Female', 'matthew20'),
(913380854, 'Female', 'johnking'),
(493436603, 'Female', 'edwardyoung'),
(679308914, 'Male', 'crawforddenise'),
(967468135, 'Female', 'hughesronald'),
(390023727, 'Female', 'bradleyblack'),
(157435433, 'Female', 'jonesroy'),
(425976704, 'Female', 'dixontyler'),
(961833604, 'Male', 'matthew04');

-- 插入作品信息初始数据
INSERT INTO works (work_id, capture_time, work_name) VALUES
('2CBD8C1F2', '2022-07-24 04:19:47', 'Photo_0'),
('1185817F8B', '2021-05-25 08:50:57', 'Photo_1'),
('7CC4820FC', '2022-11-10 23:15:06', 'Photo_2'),
('BB42F04B9', '2020-12-08 18:29:25', 'Photo_3'),
('A40F3CEBD', '2022-12-31 19:21:24', 'Photo_4'),
('283B2D9C5', '2023-03-10 19:03:36', 'Photo_5'),
('1303621F94', '2024-03-23 15:59:32', 'Photo_6'),
('109CA90C04', '2020-07-02 18:08:28', 'Photo_7'),
('3B85FFDE6', '2020-03-09 13:41:10', 'Photo_8'),
('9ED4C1BDC', '2020-10-09 08:10:37', 'Photo_9'),
('3921A716C', '2020-03-05 05:14:21', 'Photo_10'),
('782F1168', '2022-07-05 19:50:44', 'Photo_11'),
('17362D456A', '2020-05-10 20:18:45', 'Photo_12'),
('7CA53DED4', '2022-12-01 21:42:17', 'Photo_13'),
('16E99C35B2', '2020-12-17 21:22:05', 'Photo_14'),
('62F268142', '2022-01-19 17:33:28', 'Photo_15'),
('85C5BA0A7', '2023-11-22 06:15:13', 'Photo_16'),
('4B2C5328A', '2022-06-12 00:40:13', 'Photo_17'),
('18D7B95D3', '2021-05-09 07:21:20', 'Photo_18'),
('265E45886', '2023-02-28 09:21:17', 'Photo_19'),
('149984E207', '2023-10-27 17:10:58', 'Photo_20'),
('F3D0578F5', '2023-02-22 21:29:50', 'Photo_21'),
('E8774674F', '2023-11-24 03:08:47', 'Photo_22'),
('83B8FF183', '2024-03-29 20:33:26', 'Photo_23'),
('F820485B6', '2021-05-30 09:06:29', 'Photo_24'),
('6C1757A0F', '2024-01-22 12:17:26', 'Photo_25'),
('115F9C66BA', '2022-07-20 02:02:35', 'Photo_26'),
('64255DA25', '2023-12-03 04:05:45', 'Photo_27'),
('4A8CA7567', '2023-08-01 05:48:54', 'Photo_28'),
('32338BCE6', '2021-06-02 18:03:27', 'Photo_29');
