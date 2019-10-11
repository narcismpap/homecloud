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
-- Table structure for table `home_viewedlist`
--

USE `homecloud`; 

DROP TABLE IF EXISTS `home_viewedlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_viewedlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `added_on` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `home_viewedlist_d06c534f` (`movie_id`),
  KEY `home_viewedlist_6340c63c` (`user_id`),
  CONSTRAINT `movie_id_refs_id_291b6b8f` FOREIGN KEY (`movie_id`) REFERENCES `home_movie` (`id`),
  CONSTRAINT `user_id_refs_id_d4c4ae57` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_viewedlist`
--

LOCK TABLES `home_viewedlist` WRITE;
/*!40000 ALTER TABLE `home_viewedlist` DISABLE KEYS */;
INSERT INTO `home_viewedlist` VALUES
(2,225,1,'2014-09-07'),
(6,59,2,'2014-09-07'),
(8,67,3,'2014-09-07'),
(9,77,3,'2014-09-07'),
(10,65,3,'2014-09-07'),
(11,59,3,'2014-09-07'),
(16,381,1,'2014-09-07'),
(17,376,1,'2014-09-07'),
(18,374,1,'2014-09-07'),
(19,370,1,'2014-09-07'),
(20,369,1,'2014-09-07'),
(21,392,2,'2015-01-02');
/*!40000 ALTER TABLE `home_viewedlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-30 11:39:11
