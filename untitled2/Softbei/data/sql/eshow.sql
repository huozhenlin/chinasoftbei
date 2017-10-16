/*
Navicat MySQL Data Transfer

Source Server         : hello
Source Server Version : 50716
Source Host           : localhost:3306
Source Database       : softbei

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2017-06-25 12:47:20
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `eshow`
-- ----------------------------
DROP TABLE IF EXISTS `eshow`;
CREATE TABLE `eshow` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `start_time` varchar(255) DEFAULT NULL,
  `endtime` varchar(100) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `hangye` varchar(100) DEFAULT NULL,
  `hold_num` varchar(100) DEFAULT NULL,
  `hold_cycle` varchar(100) DEFAULT NULL,
  `zhanguan` varchar(100) DEFAULT NULL,
  `zhuban` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of eshow
-- ----------------------------
