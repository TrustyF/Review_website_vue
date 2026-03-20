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
-- Table structure for table `themes`
--

DROP TABLE IF EXISTS `themes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `themes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `origin` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `themes`
--

LOCK TABLES `themes` WRITE;
/*!40000 ALTER TABLE `themes` DISABLE KEYS */;
INSERT INTO `themes` VALUES (1,'Science fiction','game'),(2,'Survival','game'),(3,'Open world','game'),(4,'Action','game'),(5,'Fantasy','game'),(6,'Historical','game'),(7,'Horror','game'),(8,'Comedy','game'),(9,'Sandbox','game'),(10,'Mystery','game'),(11,'Warfare','game'),(12,'Educational','game'),(13,'4X (explore, expand, exploit, and exterminate)','game'),(14,'Stealth','game'),(15,'Drama','game'),(16,'Business','game'),(17,'Non-fiction','game'),(18,'Party','game'),(19,'Kids','game'),(20,'Thriller','game'),(21,'Role-playing (RPG)','game'),(22,'Strategy','game'),(23,'MOBA','game'),(24,'Turn-based strategy (TBS)','game'),(25,'Sport','game'),(26,'Adventure','game'),(27,'Indie','game'),(28,'Puzzle','game'),(29,'Visual Novel','game'),(30,'Hack and slash/Beat \'em up','game'),(31,'Racing','game'),(32,'Platform','game'),(33,'Arcade','game'),(34,'Music','game'),(35,'Card & Board Game','game'),(36,'Shooter','game'),(37,'Fighting','game'),(38,'Quiz/Trivia','game'),(39,'Simulator','game'),(40,'Real Time Strategy (RTS)','game'),(41,'Tactical','game'),(42,'Point-and-click','game'),(43,'Pinball','game');
/*!40000 ALTER TABLE `themes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-20  0:13:16
