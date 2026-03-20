CREATE DATABASE  IF NOT EXISTS `TrustyFox$review_site` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `TrustyFox$review_site`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: TrustyFox$review_site
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `media_user_list_assoc`
--

DROP TABLE IF EXISTS `media_user_list_assoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `media_user_list_assoc` (
  `media_id` int DEFAULT NULL,
  `user_list_id` int DEFAULT NULL,
  KEY `media_id` (`media_id`),
  KEY `user_list_id` (`user_list_id`),
  CONSTRAINT `media_user_list_assoc_ibfk_1` FOREIGN KEY (`media_id`) REFERENCES `medias` (`id`) ON DELETE CASCADE,
  CONSTRAINT `media_user_list_assoc_ibfk_2` FOREIGN KEY (`user_list_id`) REFERENCES `user_lists` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `media_user_list_assoc`
--

LOCK TABLES `media_user_list_assoc` WRITE;
/*!40000 ALTER TABLE `media_user_list_assoc` DISABLE KEYS */;
INSERT INTO `media_user_list_assoc` VALUES (1085,1),(556,1),(598,1),(545,1),(630,1),(520,1),(477,1),(1347,1),(415,1),(412,1),(1337,1),(471,1),(510,1),(491,1),(357,1),(1077,1),(1404,1),(515,1),(540,1),(464,1),(429,1);
/*!40000 ALTER TABLE `media_user_list_assoc` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-20  0:13:09
