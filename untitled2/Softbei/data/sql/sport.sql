/*
Navicat MySQL Data Transfer

Source Server         : hello
Source Server Version : 50716
Source Host           : localhost:3306
Source Database       : softbei

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2017-06-25 12:47:48
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `sport`
-- ----------------------------
DROP TABLE IF EXISTS `sport`;
CREATE TABLE `sport` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `start_time` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `changuan` varchar(100) DEFAULT NULL,
  `endtime` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sport
-- ----------------------------
