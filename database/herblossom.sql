/*
 Navicat Premium Dump SQL

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80040 (8.0.40)
 Source Host           : localhost:3306
 Source Schema         : herblossom

 Target Server Type    : MySQL
 Target Server Version : 80040 (8.0.40)
 File Encoding         : 65001

 Date: 21/03/2025 21:45:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for post
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post`  (
  `post_id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '文章ID',
  `user_id` int UNSIGNED NOT NULL COMMENT '用户ID',
  `title` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '正文内容',
  `tags` VARCHAR(255),
  `category` VARCHAR(50),
  `comment_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论数量',
  `create_time` VARCHAR(255),
  `image_urls` TEXT,
  PRIMARY KEY (`post_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE,
  INDEX `idx_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci
  COMMENT = '帖子表'
  ROW_FORMAT = Dynamic;
-- ----------------------------
-- Records of post
-- ----------------------------

-- ----------------------------
-- Table structure for topic
-- ----------------------------
DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic`  (
  `topic_id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '话题ID',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '话题名称',
  `cover` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '封面图片token',
  `description` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '话题描述',
  `post_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '帖子数量',
  `follower_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '关注者数量',
  PRIMARY KEY (`topic_id`) USING BTREE,
  INDEX `name`(`name` ASC) USING BTREE,
  INDEX `follower_count`(`follower_count` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '话题表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of topic
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `email` varchar(320) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮箱',
  `avatar` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像token',
  `cover` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '封面图片token',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  `follower_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '关注我的人数',
  `followee_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '我关注的人数',
  `following_topic_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '我关注的话题数',
  `post_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '我发表的问题数量',
  `comment_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '我发表的回答数量',
  `bio` varchar(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '个人简介',
  `company` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公司名称',
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地址',
  PRIMARY KEY (`user_id`) USING BTREE,
  INDEX `user_name`(`username` ASC) USING BTREE,
  INDEX `email`(`email` ASC) USING BTREE,
  INDEX `follower_count`(`follower_count` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '1', '1', '../static/images/chiikawa.jpg', '../static/images/chiikawa.jpg', '1', 1, 2, 3, 4, 5, '6', 'ucd', 'Beijing');

SET FOREIGN_KEY_CHECKS = 1;

-- 博客表结构
DROP TABLE IF EXISTS `blog`;
CREATE TABLE `blog` (
  `blog_id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '博客ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '博客标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '博客内容',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '博客图片URL',
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '博客分类',
  `read_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '阅读时间',
  `author_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '作者名称',
  `author_avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '作者头像URL',
  `publish_date` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '发布日期',
  `link_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '博客链接URL',
  `is_featured` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否特色博客',
  `create_time` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '创建时间',
  PRIMARY KEY (`blog_id`) USING BTREE,
  INDEX `category`(`category` ASC) USING BTREE,
  INDEX `create_time`(`create_time` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '博客表' ROW_FORMAT = Dynamic;


-- Table structure for job
-- ----------------------------
DROP TABLE IF EXISTS `job`;
CREATE TABLE `job` (
  `job_id` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `salary` int DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `experience` varchar(255) DEFAULT NULL,
  `education` varchar(255) DEFAULT NULL,
  `short_desc` varchar(255) DEFAULT NULL,
  `full_desc` text,
  `tags` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS comment;

CREATE TABLE comment (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `post_id` INT UNSIGNED NOT NULL,
    `user_id` INT UNSIGNED NOT NULL,
    `content` TEXT NOT NULL,
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `is_author` TINYINT(1) DEFAULT 0,
    FOREIGN KEY (`post_id`) REFERENCES `post`(`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
