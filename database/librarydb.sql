/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44-log)
 Source Host           : localhost:3306
 Source Schema         : librarydb

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44-log)
 File Encoding         : 65001

 Date: 19/11/2024 17:08:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `author` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `publisher` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `edition` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `isbn` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `tag` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `isbn`(`isbn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of books
-- ----------------------------
INSERT INTO `books` VALUES (1, '1984', 'George Orwell', 'Secker & Warburg', '1st Edition', '978-0451524935', 'Dystopian');
INSERT INTO `books` VALUES (2, 'To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', '1st Edition', '978-0061120084', 'Fiction');
INSERT INTO `books` VALUES (3, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', '1st Edition', '978-0743273565', 'Classic');
INSERT INTO `books` VALUES (4, 'The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown and Company', '1st Edition', '978-0316769488', 'Fiction');
INSERT INTO `books` VALUES (5, 'Brave New World', 'Aldous Huxley', 'Chatto & Windus', '1st Edition', '978-0060850524', 'Dystopian');

-- ----------------------------
-- Table structure for borrow
-- ----------------------------
DROP TABLE IF EXISTS `borrow`;
CREATE TABLE `borrow`  (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `borrower_id` int(11) NOT NULL,
  `time_till_return` int(2) NOT NULL,
  `book_id` int(255) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of borrow
-- ----------------------------

-- ----------------------------
-- Table structure for lost
-- ----------------------------
DROP TABLE IF EXISTS `lost`;
CREATE TABLE `lost`  (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `date` date NULL DEFAULT NULL,
  `location` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of lost
-- ----------------------------

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `sender_name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `message` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `replied` int(1) NOT NULL,
  `send_date` datetime NOT NULL,
  `replier_id` int(11) NULL DEFAULT NULL,
  `replier_name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `reply` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `reply_date` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'unique',
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `identification` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `email` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `avatar` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'boss', 'password@123', 'administrator', 'boss@gmail.com', 'static/photo/WIN_20240229_14_48_30_Scan.jpg');
INSERT INTO `users` VALUES (2, 'TaylorSwift', 'password@123', 'student', 'taylor.swift@gmail.com', 'static/photo/default_avatar.png');
INSERT INTO `users` VALUES (3, 'DonaldTrump', 'password@123', 'staff', 'donald.trump@gmail.com', 'static/photo/default_avatar.png');
INSERT INTO `users` VALUES (4, '1', '1', 'Student', '1@1', 'static/photo/default_avatar.png');
INSERT INTO `users` VALUES (5, 'boranDuan', '123@@qwe', 'Student', 'Broa@123.com', 'static/photo/default_avatar.png');
INSERT INTO `users` VALUES (6, 'DBRDBR', '123@@qwe', 'Student', 'boran@123.com', 'static/photo/default_avatar.png');
INSERT INTO `users` VALUES (7, 'dbrdbr', '123@@qwe', 'Student', 'dbr@123.com', 'static/photo/default_avatar.png');

SET FOREIGN_KEY_CHECKS = 1;
