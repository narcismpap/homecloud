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
-- Table structure for table `auth_permission`
--

USE `homecloud`; 

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can add permission',2,'add_permission'),
(5,'Can change permission',2,'change_permission'),
(6,'Can delete permission',2,'delete_permission'),
(7,'Can add group',3,'add_group'),
(8,'Can change group',3,'change_group'),
(9,'Can delete group',3,'delete_group'),
(10,'Can add user',4,'add_user'),
(11,'Can change user',4,'change_user'),
(12,'Can delete user',4,'delete_user'),
(13,'Can add content type',5,'add_contenttype'),
(14,'Can change content type',5,'change_contenttype'),
(15,'Can delete content type',5,'delete_contenttype'),
(16,'Can add session',6,'add_session'),
(17,'Can change session',6,'change_session'),
(18,'Can delete session',6,'delete_session'),
(19,'Can add movie',7,'add_movie'),
(20,'Can change movie',7,'change_movie'),
(21,'Can delete movie',7,'delete_movie'),
(22,'Can add cast',8,'add_cast'),
(23,'Can change cast',8,'change_cast'),
(24,'Can delete cast',8,'delete_cast'),
(25,'Can add review',9,'add_review'),
(26,'Can change review',9,'change_review'),
(27,'Can delete review',9,'delete_review'),
(28,'Can add production company',10,'add_productioncompany'),
(29,'Can change production company',10,'change_productioncompany'),
(30,'Can delete production company',10,'delete_productioncompany'),
(31,'Can add movie production company',11,'add_movieproductioncompany'),
(32,'Can change movie production company',11,'change_movieproductioncompany'),
(33,'Can delete movie production company',11,'delete_movieproductioncompany'),
(34,'Can add genre',12,'add_genre'),
(35,'Can change genre',12,'change_genre'),
(36,'Can delete genre',12,'delete_genre'),
(37,'Can add movie genre',13,'add_moviegenre'),
(38,'Can change movie genre',13,'change_moviegenre'),
(39,'Can delete movie genre',13,'delete_moviegenre'),
(40,'Can add actor',14,'add_actor'),
(41,'Can change actor',14,'change_actor'),
(42,'Can delete actor',14,'delete_actor'),
(43,'Can add movie actor',15,'add_movieactor'),
(44,'Can change movie actor',15,'change_movieactor'),
(45,'Can delete movie actor',15,'delete_movieactor'),
(46,'Can add translate cache',16,'add_translatecache'),
(47,'Can change translate cache',16,'change_translatecache'),
(48,'Can delete translate cache',16,'delete_translatecache'),
(49,'Can add viewed list',17,'add_viewedlist'),
(50,'Can change viewed list',17,'change_viewedlist'),
(51,'Can delete viewed list',17,'delete_viewedlist'),
(52,'Can add pending list',18,'add_pendinglist'),
(53,'Can change pending list',18,'change_pendinglist'),
(54,'Can delete pending list',18,'delete_pendinglist');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-30 11:39:09
