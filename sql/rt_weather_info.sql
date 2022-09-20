/*
 Navicat Premium Data Transfer

 Source Server         : localhost_MySQL
 Source Server Type    : MySQL
 Source Server Version : 50731
 Source Host           : localhost:3306
 Source Schema         : py_db_platform

 Target Server Type    : MySQL
 Target Server Version : 50731
 File Encoding         : 65001

 Date: 20/09/2022 14:33:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for rt_weather_info
-- ----------------------------
DROP TABLE IF EXISTS `rt_weather_info`;
CREATE TABLE `rt_weather_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `img_url` varchar(1000) COLLATE utf8_bin DEFAULT NULL COMMENT '图片地址',
  `img_digits` varchar(60) COLLATE utf8_bin DEFAULT NULL COMMENT '数字签名',
  `img_content` varchar(2000) COLLATE utf8_bin DEFAULT NULL COMMENT '图片内容',
  `is_used` varchar(1) COLLATE utf8_bin DEFAULT '0' COMMENT '是否使用过',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

SET FOREIGN_KEY_CHECKS = 1;
