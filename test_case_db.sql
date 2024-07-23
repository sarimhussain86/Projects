-- MySQL dump 10.13  Distrib 8.0.35-26.16, for Linux (x86_64)
--
-- Host: localhost    Database: test_case_db
-- ------------------------------------------------------
-- Server version	8.0.35-26.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `abcd`
--

DROP TABLE IF EXISTS `abcd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abcd` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `abcd_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `abcd_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `abcd_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abcd`
--

LOCK TABLES `abcd` WRITE;
/*!40000 ALTER TABLE `abcd` DISABLE KEYS */;
/*!40000 ALTER TABLE `abcd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `arabic`
--

DROP TABLE IF EXISTS `arabic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arabic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `arabic_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `arabic_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `arabic_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arabic`
--

LOCK TABLES `arabic` WRITE;
/*!40000 ALTER TABLE `arabic` DISABLE KEYS */;
INSERT INTO `arabic` VALUES (1,'TC-HW-01','Hardware','To check size of RAM installed on the server,\r\n','','Execute the following command on terminal\r\n$ htop\r\nfind out the total size of Memory.\r\nRepeat this step for all clinet sniffers.','RAM of server should be greater then or equal to 377GB',NULL,NULL,12,79,1,NULL,NULL),(3,'TC-HW-02','Hardware','To check the Storage on the servers,\nIt should be equal to Storage written in DA AUH AS-Built Document.',NULL,'Execute the following command on terminal\n$ df -h\nfind out the total storage.\nRepeat this step for all clinet sniffers.','\nRAID 1 For OS = 800 GB\nRAID 0 for sniffer = 4.4 TB',NULL,NULL,12,79,1,NULL,NULL),(5,'TC-HW-3','vc','vc',NULL,NULL,'gfds',NULL,NULL,12,79,1,NULL,NULL),(7,'TC-HW-01','Hardware','To check size of RAM installed on the server,\nIt should be equal to RAM written in DA AUH As-Built Document.',NULL,'Execute the following command on terminal\n$ htop\nfind out the total size of Memory.\nRepeat this step for all clinet sniffers.','RAM of server should be greater then or equal to 377GB',NULL,NULL,18,81,1,NULL,NULL),(9,'TC-HW-02','Hardware','To check the Storage on the servers,\nIt should be equal to Storage written in DA AUH AS-Built Document.',NULL,'Execute the following command on terminal\n$ df -h\nfind out the total storage.\nRepeat this step for all clinet sniffers.','\nRAID 1 For OS = 800 GB\nRAID 0 for sniffer = 4.4 TB',NULL,NULL,18,81,1,NULL,NULL),(11,'TC-HW-03','Hardware','To check all servers BIOS Version',NULL,'Execute the following command on terminal\n$ sudo dmidecode -s bios-version\nfind out the Bios version.\nRepeat this step for all clinet sniffers.','Bios Version should be 1.7.4',NULL,NULL,18,81,1,NULL,NULL),(13,'TC-HW-04','Hardware','To Check IDRAC FW version',NULL,NULL,'iDRAC Firmware Version should be 5.10.50.00',NULL,NULL,18,81,1,NULL,NULL),(15,'TC-HW-05','Hardware','To check size of RAM installed on the server,\nIt should be equal to RAM written DA AUH As-Built Document.',NULL,'Execute the following command on terminal\n$ htop\nfind out the total size of Memory.\nRepeat this step for all server sniffers.','RAM of server should be greater then or equal to 377GB',NULL,NULL,18,81,2,NULL,NULL),(17,'TC-HW-06','Hardware','To check the Storage on the servers,\nIt should be equal to Storage written in DA AUH AS-Built Document.',NULL,'Execute the following command on terminal\n$ df -h\nfind out the total storage.\nRepeat this step for all server sniffers.','\nRAID 1 For OS = 800 GB\nRAID 0 for sniffer = 4.4 TB',NULL,NULL,18,81,2,NULL,NULL),(19,'TC-HW-07','Hardware','To check all servers BIOS Version',NULL,'Execute the following command on terminal\n$ sudo dmidecode -s bios-version\nfind out the Bios version.\nRepeat this step for all server sniffers.','Bios Version should be 1.7.4',NULL,NULL,18,81,2,NULL,NULL),(21,'TC-HW-08','Hardware','To Check IDRAC FW version',NULL,'To login to IDRAC web user interface,\n1: Open a browser and enter the IdRAC IP address.\n2: Type username and password and click login\n3: Check for system information and check iDRAC Firmware Version.\nRepeat this step for all server sniffers.','iDRAC Firmware Version should be 5.10.50.00',NULL,NULL,18,81,2,NULL,NULL),(23,'TC-HW-14','Hardware','To check size of RAM installed on the server,\nIt should be equal to RAM written in DA DU As-Built Document.',NULL,'Execute the following command on terminal\n$ htop\nfind out the total size of Memory.\nRepeat this step for all API servers.','v',NULL,NULL,18,81,3,NULL,NULL),(25,'TC-HW-15','Hardware','To check the Storage on the servers,\nIt should be equal to Storage written in DA-DU AS-Built Document.',NULL,'Execute the following command on terminal\n$ df -h\nfind out the total storage.\nRepeat this step for all API servers.','\nRAID 1 For OS = 800 GB\nRAID 0 for sniffer = 4.4 TB',NULL,NULL,18,81,3,NULL,NULL),(27,'TC-HW-16','Hardware','To check all servers BIOS Version',NULL,'Execute the following command on terminal\n$ sudo dmidecode -s bios-version\nfind out the Bios version\nRepeat this step for all API servers.','Bios Version should be 1.7.4',NULL,NULL,18,81,3,NULL,NULL),(29,'TC-HW-17','Hardware','To Check IDRAC FW version',NULL,'To login to IDRAC web user interface,\n1: Open a browser and enter the IDRAC IP address.\n2: Type username and password and click login\n3: Check for system information and check iDRAC Firmware Version.\nRepeat this step for all API servers.','iDRAC Firmware Version should be 5.10.50.00',NULL,NULL,18,81,3,NULL,NULL),(31,'TC-HW-09','Hardware','To check size of RAM installed on the server,\nIt should be equal to RAM written in DA AUH As-Built Document.',NULL,'Execute the following command on terminal\n$ htop\nfind out the total size of Memory.\nRepeat this step for all DB servers.','RAM of server should be greater then or equal to 377GB',NULL,NULL,18,81,4,NULL,NULL),(33,'TC-HW-10','Hardware','To check the Storage on the servers,\nIt should be equal to Storage written in DA AUH AS-Built Document.',NULL,'Execute the following command on terminal\n$ df -h\nfind out the total storage.\nRepeat this step for all DB servers.','\nRAID 1 For OS = 800 GB\nRAID 0 for sniffer = 4.4 TB',NULL,NULL,18,81,4,NULL,NULL),(35,'TC-HW-11','Hardware','Check SAN Storage ',NULL,'Execute the following command on terminal\n$ df -h\nfind out the total storage.\nRepeat this step for all DB servers.',NULL,NULL,NULL,18,81,4,NULL,NULL),(37,'TC-HW-12','Hardware','To check all servers BIOS Version',NULL,'Execute the following command on terminal\n$ sudo dmidecode -s bios-version\nfind out the Bios version.\nRepeat this step for all DB servers.','Bios Version should be 1.7.4',NULL,NULL,18,81,4,NULL,NULL),(39,'TC-HW-13','Hardware','To Check IDRAC FW version',NULL,'To login to IDRAC web user interface,\n1: Open a browser and enter the IdRAC IP address.\n2: Type username and password and click login\n3: Check for system information and check iDRAC Firmware Version.\nRepeat this step for all DB servers.','iDRAC Firmware Version should be 5.10.50.00',NULL,NULL,18,81,4,NULL,NULL);
/*!40000 ALTER TABLE `arabic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `arabic_2`
--

DROP TABLE IF EXISTS `arabic_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arabic_2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `message` text,
  `erd` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `arabic_2_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `arabic_2_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `arabic_2_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arabic_2`
--

LOCK TABLES `arabic_2` WRITE;
/*!40000 ALTER TABLE `arabic_2` DISABLE KEYS */;
INSERT INTO `arabic_2` VALUES (1,'1.0','asdf',NULL,14,75,NULL,NULL,NULL);
/*!40000 ALTER TABLE `arabic_2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) DEFAULT NULL,
  `cat_type` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Connected Calls',1),(2,'Hold/Unhold',1),(3,'Forwarding Scenarios',1),(4,'SRVCC Scenarios',1),(5,'Conference Calls :3 Parties',1),(6,'Conference Calls : 4 Parties',1),(7,'Conference Calls : 5 Parties',1),(8,'SRVCC Conference Calls',1),(9,'VoWifi/ViWifi-Scenarios',1),(10,'SmartMCN-Scenarios',1),(11,'#Calls Scenarios',1);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faheem`
--

DROP TABLE IF EXISTS `faheem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faheem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `faheem_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `faheem_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `faheem_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faheem`
--

LOCK TABLES `faheem` WRITE;
/*!40000 ALTER TABLE `faheem` DISABLE KEYS */;
/*!40000 ALTER TABLE `faheem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gbhg`
--

DROP TABLE IF EXISTS `gbhg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gbhg` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `gbhg_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `gbhg_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `gbhg_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gbhg`
--

LOCK TABLES `gbhg` WRITE;
/*!40000 ALTER TABLE `gbhg` DISABLE KEYS */;
/*!40000 ALTER TABLE `gbhg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gilgat`
--

DROP TABLE IF EXISTS `gilgat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gilgat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `gilgat_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `gilgat_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `gilgat_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gilgat`
--

LOCK TABLES `gilgat` WRITE;
/*!40000 ALTER TABLE `gilgat` DISABLE KEYS */;
/*!40000 ALTER TABLE `gilgat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hassaan`
--

DROP TABLE IF EXISTS `hassaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hassaan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `hassaan_1` text,
  `hassaan_2` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `hassaan_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `hassaan_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `hassaan_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hassaan`
--

LOCK TABLES `hassaan` WRITE;
/*!40000 ALTER TABLE `hassaan` DISABLE KEYS */;
/*!40000 ALTER TABLE `hassaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hunza`
--

DROP TABLE IF EXISTS `hunza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hunza` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `hunza_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `hunza_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `hunza_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hunza`
--

LOCK TABLES `hunza` WRITE;
/*!40000 ALTER TABLE `hunza` DISABLE KEYS */;
/*!40000 ALTER TABLE `hunza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `islamabad`
--

DROP TABLE IF EXISTS `islamabad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `islamabad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `islamabad_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `islamabad_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `islamabad_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `islamabad`
--

LOCK TABLES `islamabad` WRITE;
/*!40000 ALTER TABLE `islamabad` DISABLE KEYS */;
/*!40000 ALTER TABLE `islamabad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `majid`
--

DROP TABLE IF EXISTS `majid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `majid` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `majid_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `majid_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `majid_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `majid`
--

LOCK TABLES `majid` WRITE;
/*!40000 ALTER TABLE `majid` DISABLE KEYS */;
/*!40000 ALTER TABLE `majid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_test_cases`
--

DROP TABLE IF EXISTS `master_test_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_test_cases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` varchar(12) DEFAULT NULL,
  `test_case_type` varchar(80) DEFAULT NULL,
  `test_case_description` varchar(300) DEFAULT NULL,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` varchar(300) DEFAULT NULL,
  `actual_result` varchar(100) DEFAULT NULL,
  `remarks` varchar(200) DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `master_test_cases_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `master_test_cases_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `master_test_cases_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_test_cases`
--

LOCK TABLES `master_test_cases` WRITE;
/*!40000 ALTER TABLE `master_test_cases` DISABLE KEYS */;
INSERT INTO `master_test_cases` VALUES (11,'TC-1','Non Functional','Test the endpoint with valid parameters.','Nill','Send a request for listing MDRs with correct offset and size via CURL or Postman.','sndjsnjd',NULL,NULL,8,15,NULL,NULL,NULL),(12,'TC-2','jdsfjksdfa','adfsadsfad','sfdasdfdfadsf','dasfsfda','asdfasdf',NULL,NULL,8,15,NULL,NULL,NULL),(14,'1','askjfhjka','dskjnvkjdsbv','kjsdnjkbdsjkbv','kjsdnvkjsd','dkjnfkjdasjkfnjk',NULL,NULL,9,19,NULL,NULL,NULL),(15,'1.11','jhfdbhbjh','kjdsbkjvbdsjk','kdjsbjkvsdbjkb','kjdbsvjkbsdkjbvkjb','sdjkbjkdsbvj',NULL,NULL,9,19,NULL,NULL,NULL),(16,'TC-3','dwd','asasdr','werfwef','cdscfsc','ewvwerf',NULL,NULL,8,15,NULL,NULL,NULL),(18,'dnasdknwd','a ncasdd ','a scmasd c','ascdsakc','a snckjscdsancsc','jkasncdf',NULL,NULL,28,32,NULL,NULL,NULL),(20,'zczc','zczxc','czxczcc','zcc','zxccz','svczed',NULL,NULL,30,34,NULL,NULL,NULL),(22,'ASQAS','axASC','DASXD','ADADSA','DASD','ADSD',NULL,NULL,36,40,NULL,NULL,NULL),(23,'TC-4','edwqd','dqwedqwqdqwq','qwdqwed','dqwed','qwedqwed',NULL,NULL,8,15,NULL,NULL,NULL),(25,'TC-1','n camc','sand cads','njkckasd','njkasdcd','ankmcnksdc',NULL,NULL,41,43,NULL,NULL,NULL),(27,'TC-2','acnasd c','ascsdc','nvlksnd','k asd c','laksncldc',NULL,NULL,41,43,NULL,NULL,NULL),(29,'TC-1','casdcasd','xcac','sacsdc','ascsdc','ascsdc',NULL,NULL,8,18,NULL,NULL,NULL),(31,'TC-2','ascasdc','asc csc','asdcasdc','ascsc','ascsdc',NULL,NULL,8,18,NULL,NULL,NULL),(33,'1','asxasdc','ascsdc','ascsdc','ascsdc','sacs',NULL,NULL,8,45,NULL,NULL,NULL);
/*!40000 ALTER TABLE `master_test_cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modules`
--

DROP TABLE IF EXISTS `modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modules` (
  `module_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int DEFAULT NULL,
  `module_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`module_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `modules_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modules`
--

LOCK TABLES `modules` WRITE;
/*!40000 ALTER TABLE `modules` DISABLE KEYS */;
INSERT INTO `modules` VALUES (1,1,'Client Sniffer'),(2,1,'Server Sniffer'),(3,1,'API Server'),(4,1,'DB Node'),(5,1,'Monitoring Server');
/*!40000 ALTER TABLE `modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muslima`
--

DROP TABLE IF EXISTS `muslima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muslima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `muslima_1` text,
  `muslima_2` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `muslima_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `muslima_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `muslima_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muslima`
--

LOCK TABLES `muslima` WRITE;
/*!40000 ALTER TABLE `muslima` DISABLE KEYS */;
/*!40000 ALTER TABLE `muslima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `note_id` int NOT NULL AUTO_INCREMENT,
  `topic` varchar(100) DEFAULT NULL,
  `note` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`note_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES (1,NULL,'Note: Need to check that service is\"Enable\" as well'),(2,NULL,'Following test cases to be skipped'),(3,NULL,'API Data retrieval from Sniffers Caching Disk (xflow)'),(4,NULL,'Additional Scenarios - Phase -2');
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(15) DEFAULT NULL,
  `project_version` double DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `project_created` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (8,'SMSoIP',1,'2024-05-17 09:50:17',0),(9,'Test',1,'2024-05-20 15:28:38',0),(10,'SMSoIP',2,'2024-07-01 15:33:29',0),(12,'api',1,'2024-07-01 16:02:15',0),(14,'Sampling',1,'2024-07-01 16:17:07',0),(16,'video',1,'2024-07-01 16:47:03',0),(18,'Test',2,'2024-07-01 17:30:01',0),(20,'backend',1,'2024-07-01 17:31:08',0),(22,'Sampling',2,'2024-07-02 11:22:30',0),(24,'Test',3,'2024-07-02 14:33:27',0),(26,'api',2,'2024-07-02 15:09:14',0),(28,'video',2,'2024-07-02 15:17:34',0),(30,'mdf',1,'2024-07-02 15:28:40',0),(32,'Test',4,'2024-07-02 15:39:33',0),(34,'backend',2,'2024-07-02 15:56:47',0),(36,'SMSoIP',3,'2024-07-02 16:01:45',0),(38,'SMSoIP',4,'2024-07-02 16:31:46',0),(40,'api',3,'2024-07-02 16:36:21',0),(41,'db test',1,'2024-07-03 09:54:35',0),(43,'ETSI',1,'2024-07-07 17:24:03',0);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saad`
--

DROP TABLE IF EXISTS `saad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description_1` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `saad_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `saad_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `saad_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saad`
--

LOCK TABLES `saad` WRITE;
/*!40000 ALTER TABLE `saad` DISABLE KEYS */;
/*!40000 ALTER TABLE `saad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sawat`
--

DROP TABLE IF EXISTS `sawat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sawat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `sawat_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `sawat_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `sawat_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sawat`
--

LOCK TABLES `sawat` WRITE;
/*!40000 ALTER TABLE `sawat` DISABLE KEYS */;
/*!40000 ALTER TABLE `sawat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selected_test_cases_for_new_test_cycle`
--

DROP TABLE IF EXISTS `selected_test_cases_for_new_test_cycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selected_test_cases_for_new_test_cycle` (
  `row_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `test_case_id` varchar(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selected_test_cases_for_new_test_cycle`
--

LOCK TABLES `selected_test_cases_for_new_test_cycle` WRITE;
/*!40000 ALTER TABLE `selected_test_cases_for_new_test_cycle` DISABLE KEYS */;
INSERT INTO `selected_test_cases_for_new_test_cycle` VALUES (14,19,9,'1'),(15,19,9,'1.11');
/*!40000 ALTER TABLE `selected_test_cases_for_new_test_cycle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensors`
--

DROP TABLE IF EXISTS `sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `apple` text,
  `orange` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `sensors_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `sensors_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `sensors_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors`
--

LOCK TABLES `sensors` WRITE;
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table_1`
--

DROP TABLE IF EXISTS `table_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `table_1_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `table_1_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `table_1_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_1`
--

LOCK TABLES `table_1` WRITE;
/*!40000 ALTER TABLE `table_1` DISABLE KEYS */;
/*!40000 ALTER TABLE `table_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table_2`
--

DROP TABLE IF EXISTS `table_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `column_2` text,
  `column_1` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `table_2_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `table_2_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `table_2_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_2`
--

LOCK TABLES `table_2` WRITE;
/*!40000 ALTER TABLE `table_2` DISABLE KEYS */;
/*!40000 ALTER TABLE `table_2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table_names`
--

DROP TABLE IF EXISTS `table_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_names` (
  `table_id` int NOT NULL AUTO_INCREMENT,
  `table_name` varchar(60) DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `exception` tinyint(1) DEFAULT NULL,
  `module_ids` varchar(50) DEFAULT NULL,
  `category_ids` varchar(50) DEFAULT NULL,
  `category_type` varchar(1) DEFAULT NULL,
  `table_prefix` int DEFAULT NULL,
  PRIMARY KEY (`table_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `table_names_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_names`
--

LOCK TABLES `table_names` WRITE;
/*!40000 ALTER TABLE `table_names` DISABLE KEYS */;
INSERT INTO `table_names` VALUES (15,'Arabic',8,NULL,NULL,NULL,NULL,NULL),(16,'Test 1',8,1,NULL,NULL,NULL,NULL),(17,'Table 1',8,1,NULL,NULL,NULL,NULL),(18,'Test 2',8,NULL,NULL,NULL,NULL,NULL),(19,'Table 3',9,NULL,NULL,NULL,NULL,NULL),(20,'Custom Header',14,NULL,NULL,NULL,NULL,NULL),(22,'Sensors',14,1,NULL,NULL,NULL,NULL),(24,'xflow',9,NULL,NULL,NULL,NULL,NULL),(26,'xflow2',9,NULL,NULL,NULL,NULL,NULL),(30,'table 2',16,1,NULL,NULL,NULL,NULL),(32,'table1',28,NULL,NULL,NULL,NULL,NULL),(34,'table 1',30,NULL,NULL,NULL,NULL,NULL),(36,'Arabic',16,NULL,NULL,NULL,NULL,NULL),(38,'Arabic',32,NULL,NULL,NULL,NULL,NULL),(40,'SS',36,NULL,NULL,NULL,NULL,NULL),(42,'gbhg',8,1,NULL,NULL,NULL,NULL),(43,'table1',41,NULL,NULL,NULL,NULL,NULL),(45,'table 5',8,NULL,NULL,NULL,NULL,NULL),(49,'TABLE',12,NULL,NULL,NULL,NULL,NULL),(59,'muslima',24,1,NULL,NULL,NULL,NULL),(61,'faheem',24,1,NULL,NULL,NULL,NULL),(63,'hunza',24,1,NULL,NULL,NULL,NULL),(65,'gilgat',24,1,NULL,NULL,NULL,NULL),(69,'arabic',9,1,NULL,NULL,NULL,NULL),(75,'araBIc',14,1,NULL,NULL,NULL,2),(77,'arabic',30,1,NULL,NULL,NULL,2),(79,'arabic',12,1,'[1]',NULL,'m',NULL),(81,'arabic',18,1,'[1, 2, 3, 4]',NULL,'m',NULL);
/*!40000 ALTER TABLE `table_names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tempa`
--

DROP TABLE IF EXISTS `tempa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tempa` (
  `id` int DEFAULT NULL,
  `amount` decimal(7,2) DEFAULT NULL,
  `tr_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50500 PARTITION BY RANGE  COLUMNS(tr_date)
(PARTITION p1 VALUES LESS THAN ('2024-01-15 15:00:00') ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN ('2024-01-15 16:00:00') ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN ('2024-01-15 17:00:00') ENGINE = InnoDB) */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tempa`
--

LOCK TABLES `tempa` WRITE;
/*!40000 ALTER TABLE `tempa` DISABLE KEYS */;
/*!40000 ALTER TABLE `tempa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_1`
--

DROP TABLE IF EXISTS `test_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_case_id` text,
  `test_case_type` text,
  `test_case_description` text,
  `prerequisites` text,
  `steps_to_execute` text,
  `expected_result` text,
  `actual_result` text,
  `remarks` text,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `module_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `table_id` (`table_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `test_1_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `test_1_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`),
  CONSTRAINT `test_1_ibfk_3` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_1`
--

LOCK TABLES `test_1` WRITE;
/*!40000 ALTER TABLE `test_1` DISABLE KEYS */;
INSERT INTO `test_1` VALUES (1,'1','functional','sdncksdjc',' jskdcksdajskac s','ajkc sdc','asdcmksd c',NULL,NULL,8,16,NULL,NULL,NULL);
/*!40000 ALTER TABLE `test_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_cases_result`
--

DROP TABLE IF EXISTS `test_cases_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_cases_result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_cycle_id` int DEFAULT NULL,
  `test_id` int DEFAULT NULL,
  `test_case_id` varchar(12) DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `table_id` int DEFAULT NULL,
  `actual_result` varchar(150) DEFAULT NULL,
  `remarks` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `test_id` (`test_id`),
  KEY `table_id` (`table_id`),
  CONSTRAINT `test_cases_result_ibfk_1` FOREIGN KEY (`test_id`) REFERENCES `master_test_cases` (`id`),
  CONSTRAINT `test_cases_result_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `api_test_cases` (`id`),
  CONSTRAINT `test_cases_result_ibfk_3` FOREIGN KEY (`test_id`) REFERENCES `new_codecs_test_cases` (`id`),
  CONSTRAINT `test_cases_result_ibfk_4` FOREIGN KEY (`test_id`) REFERENCES `system_performance_with_increased_retention` (`id`),
  CONSTRAINT `test_cases_result_ibfk_5` FOREIGN KEY (`test_id`) REFERENCES `sanity_test_calls` (`id`),
  CONSTRAINT `test_cases_result_ibfk_6` FOREIGN KEY (`id`) REFERENCES `test_cycles` (`id`),
  CONSTRAINT `test_cases_result_ibfk_7` FOREIGN KEY (`table_id`) REFERENCES `table_names` (`table_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_cases_result`
--

LOCK TABLES `test_cases_result` WRITE;
/*!40000 ALTER TABLE `test_cases_result` DISABLE KEYS */;
INSERT INTO `test_cases_result` VALUES (26,1,18,'dnasdknwd',28,32,NULL,NULL),(27,4,11,'TC-1',8,15,'Fail',''),(29,4,12,'TC-2',8,15,NULL,NULL),(31,4,16,'TC-3',8,15,'Pass','');
/*!40000 ALTER TABLE `test_cases_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_cycles`
--

DROP TABLE IF EXISTS `test_cycles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_cycles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_cycle_id` int DEFAULT NULL,
  `tester_name` varchar(20) DEFAULT NULL,
  `test_site` varchar(20) DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `project_closed` tinyint(1) DEFAULT NULL,
  `test_cycle_completed` tinyint(1) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `test_cycles_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_cycles`
--

LOCK TABLES `test_cycles` WRITE;
/*!40000 ALTER TABLE `test_cycles` DISABLE KEYS */;
INSERT INTO `test_cycles` VALUES (10,1,NULL,NULL,8,0,0,'2024-05-17 09:54:48',NULL),(11,2,NULL,NULL,8,0,0,'2024-05-17 09:58:18',NULL),(12,1,NULL,NULL,24,0,0,'2024-07-02 14:33:59',NULL),(14,3,NULL,NULL,8,0,0,'2024-07-02 14:45:48',NULL),(18,1,NULL,NULL,28,0,0,'2024-07-02 15:43:27',NULL),(19,4,NULL,NULL,8,0,0,'2024-07-02 16:58:15',NULL);
/*!40000 ALTER TABLE `test_cycles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `username` blob,
  `pwrd` blob
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (_binary 'Å·\Ås&\ö{\ó=ü!\óë§þ',_binary '³™Û¶\ê:²B¼F\É\Ë5s\Ì\Ú'),(_binary '}CH!žƒ\îR¸}\ó\r.bþ',_binary 'v»2E@ˆ—\ï™Á.[tv'),(_binary '‚Þ¢‹\Êr±‚L‚7\ã®r7',_binary '\å\È\Ï ‡’m»„A¯*\ï-‡'),(_binary '.\ï\ÂO;‹›µ¬\É/}º¡µ',_binary '.\ï\ÂO;‹›µ¬\É/}º¡µ'),(_binary '&µfmfŸ‹$\ópûgY\Ç',_binary '…>\ôJTaüAa5x„¡¹');
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xflow_testers`
--

DROP TABLE IF EXISTS `xflow_testers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `xflow_testers` (
  `tester_name` varchar(25) DEFAULT NULL,
  `account_created` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xflow_testers`
--

LOCK TABLES `xflow_testers` WRITE;
/*!40000 ALTER TABLE `xflow_testers` DISABLE KEYS */;
INSERT INTO `xflow_testers` VALUES ('faheem',0),('Hassaan',1),('MuSlima',1),('SAAD',1),('majid',1),('Abdul',0);
/*!40000 ALTER TABLE `xflow_testers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-07 23:10:10
