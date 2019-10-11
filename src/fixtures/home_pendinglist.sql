-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: db    Database: homecloud
-- ------------------------------------------------------
-- Server version	5.7.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `home_pendinglist`
--

USE `homecloud`; 

DROP TABLE IF EXISTS `home_pendinglist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_pendinglist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `added_on` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `home_pendinglist_d06c534f` (`movie_id`),
  KEY `home_pendinglist_6340c63c` (`user_id`),
  CONSTRAINT `movie_id_refs_id_d50c2d28` FOREIGN KEY (`movie_id`) REFERENCES `home_movie` (`id`),
  CONSTRAINT `user_id_refs_id_52d0d07c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_pendinglist`
--

LOCK TABLES `home_pendinglist` WRITE;
/*!40000 ALTER TABLE `home_pendinglist` DISABLE KEYS */;
INSERT INTO `home_pendinglist` VALUES
(5,62,1,'2014-09-07'),
(7,61,2,'2014-09-07'),
(8,68,3,'2014-09-07'),
(9,293,1,'2014-09-07'),
(10,141,1,'2014-09-07'),
(11,58,1,'2014-09-07'),
(12,185,1,'2014-09-07'),
(13,177,1,'2014-09-07'),
(14,174,1,'2014-09-07'),
(15,167,1,'2014-09-07'),
(16,228,1,'2014-09-07'),
(17,284,1,'2014-09-07'),
(18,194,1,'2014-09-07'),
(19,237,1,'2014-09-07'),
(20,181,1,'2014-09-07'),
(21,183,1,'2014-09-07'),
(22,148,1,'2014-09-07'),
(23,270,1,'2014-09-07'),
(24,190,1,'2014-09-07'),
(25,211,1,'2014-09-07'),
(26,306,2,'2014-09-07'),
(27,56,1,'2014-09-07'),
(28,375,1,'2014-09-07'),
(29,378,1,'2014-09-07'),
(30,151,1,'2014-09-07'),
(31,147,1,'2014-09-07'),
(34,379,1,'2014-09-07'),
(36,390,2,'2014-11-10');
/*!40000 ALTER TABLE `home_pendinglist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-30 11:39:10
