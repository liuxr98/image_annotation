/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : annotate

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 01/06/2022 16:50:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ai_model
-- ----------------------------
DROP TABLE IF EXISTS `ai_model`;
CREATE TABLE `ai_model`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `url` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `proj_url` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('NotTrained','InProgress','Error','Finished') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `ai_model_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for annotation_bbox
-- ----------------------------
DROP TABLE IF EXISTS `annotation_bbox`;
CREATE TABLE `annotation_bbox`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `factorX` float NULL DEFAULT NULL,
  `factorY` float NULL DEFAULT NULL,
  `factorWidth` float NULL DEFAULT NULL,
  `factorHeight` float NULL DEFAULT NULL,
  `image_id` int NULL DEFAULT NULL,
  `dataset_label_id` int NULL DEFAULT NULL,
  `additionalInfo` json NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `image_id`(`image_id` ASC) USING BTREE,
  INDEX `dataset_label_id`(`dataset_label_id` ASC) USING BTREE,
  CONSTRAINT `annotation_bbox_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `image` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `annotation_bbox_ibfk_2` FOREIGN KEY (`dataset_label_id`) REFERENCES `dataset_label` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for dataset
-- ----------------------------
DROP TABLE IF EXISTS `dataset`;
CREATE TABLE `dataset`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `user_id` int NULL DEFAULT NULL,
  `status` enum('None','InTeamTask','InAutoAnnotation') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `custom_label_format` json NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `dataset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for dataset_label
-- ----------------------------
DROP TABLE IF EXISTS `dataset_label`;
CREATE TABLE `dataset_label`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `dataset_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `dataset_id`(`dataset_id` ASC) USING BTREE,
  CONSTRAINT `dataset_label_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `dataset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 76 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for image
-- ----------------------------
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `img_src` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `width` int NULL DEFAULT NULL,
  `height` int NULL DEFAULT NULL,
  `dataset_id` int NULL DEFAULT NULL,
  `subtask_id` int NULL DEFAULT NULL,
  `task_id` int NULL DEFAULT NULL,
  `labeled` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `dataset_id`(`dataset_id` ASC) USING BTREE,
  INDEX `subtask_id`(`subtask_id` ASC) USING BTREE,
  INDEX `task_id`(`task_id` ASC) USING BTREE,
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `dataset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `image_ibfk_2` FOREIGN KEY (`subtask_id`) REFERENCES `sub_team_task` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `image_ibfk_3` FOREIGN KEY (`task_id`) REFERENCES `team_task` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 176 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for label_group
-- ----------------------------
DROP TABLE IF EXISTS `label_group`;
CREATE TABLE `label_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `label_group_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for label_group_label
-- ----------------------------
DROP TABLE IF EXISTS `label_group_label`;
CREATE TABLE `label_group_label`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `label_group_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `label_group_id`(`label_group_id` ASC) USING BTREE,
  CONSTRAINT `label_group_label_ibfk_1` FOREIGN KEY (`label_group_id`) REFERENCES `label_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 76 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sub_team_task
-- ----------------------------
DROP TABLE IF EXISTS `sub_team_task`;
CREATE TABLE `sub_team_task`  (
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `assignee_id` int NULL DEFAULT NULL,
  `assigner_username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `type` enum('label','review') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('InProgress','Submitted','Terminated','Deleted') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `team_task_id` int NULL DEFAULT NULL,
  `team_task_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `dataset_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `assignee_id`(`assignee_id` ASC) USING BTREE,
  INDEX `team_task_id`(`team_task_id` ASC) USING BTREE,
  CONSTRAINT `sub_team_task_ibfk_1` FOREIGN KEY (`assignee_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sub_team_task_ibfk_2` FOREIGN KEY (`team_task_id`) REFERENCES `team_task` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for team
-- ----------------------------
DROP TABLE IF EXISTS `team`;
CREATE TABLE `team`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `team_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for team_member
-- ----------------------------
DROP TABLE IF EXISTS `team_member`;
CREATE TABLE `team_member`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_id` int NULL DEFAULT NULL,
  `role` enum('labeler','reviewer') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `member_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `team_id`(`team_id` ASC) USING BTREE,
  INDEX `member_id`(`member_id` ASC) USING BTREE,
  CONSTRAINT `team_member_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `team_member_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for team_task
-- ----------------------------
DROP TABLE IF EXISTS `team_task`;
CREATE TABLE `team_task`  (
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('InProgress','Finished','TerminatedReserved','TerminatedUnreserved','Reviewed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `assigner_id` int NULL DEFAULT NULL,
  `dataset_id` int NULL DEFAULT NULL,
  `team_id` int NULL DEFAULT NULL,
  `subtask_num` int NULL DEFAULT NULL,
  `subtask_submitted_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `assigner_id`(`assigner_id` ASC) USING BTREE,
  INDEX `dataset_id`(`dataset_id` ASC) USING BTREE,
  INDEX `team_id`(`team_id` ASC) USING BTREE,
  CONSTRAINT `team_task_ibfk_1` FOREIGN KEY (`assigner_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `team_task_ibfk_2` FOREIGN KEY (`dataset_id`) REFERENCES `dataset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `team_task_ibfk_3` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password_hash` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
