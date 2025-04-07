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