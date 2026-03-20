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
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `origin` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (78,'Science Fiction','movie'),(79,'Adventure','movie'),(80,'Action','movie'),(81,'Thriller','movie'),(82,'Fantasy','movie'),(83,'Drama','movie'),(84,'War','movie'),(85,'Crime','movie'),(86,'History','movie'),(87,'Comedy','movie'),(88,'Animation','movie'),(89,'Horror','movie'),(90,'Romance','movie'),(91,'Documentary','movie'),(92,'Mystery','movie'),(93,'TV Movie','movie'),(94,'Sci-Fi & Fantasy','tv'),(95,'Talk','tv'),(96,'Action & Adventure','tv'),(97,'Family','tv'),(98,'Reality','tv'),(99,'War & Politics','tv'),(100,'Western','tv'),(101,'Kids','tv'),(102,'Music','movie'),(103,'Wuxia','manga'),(104,'Psychological','manga'),(105,'Boys\' Love','manga'),(106,'Isekai','manga'),(107,'Educational','game'),(108,'Survival','game'),(109,'Sci-Fi','manga'),(110,'Mecha','manga'),(111,'Philosophical','manga'),(112,'Slice of Life','manga'),(113,'Tragedy','manga'),(114,'Sports','manga'),(115,'Historical','manga'),(116,'Girls\' Love','manga'),(117,'Medical','manga'),(118,'Superhero','manga'),(119,'Magical Girls','manga'),(120,'Sandbox','game'),(121,'Open world','game'),(125,'Warfare','game'),(126,'Stealth','game'),(127,'Party','game'),(128,'4X (explore, expand, exploit, and exterminate)','game'),(129,'Business','game'),(130,'Non-fiction','game'),(131,'Erotic','game'),(132,'Soap','tv'),(133,'News','tv');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-20  0:12:57
