-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: farm_defense_db
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `actuator_status`
--

DROP TABLE IF EXISTS `actuator_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actuator_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `actuator_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `state` tinyint(1) DEFAULT '0',
  `mode` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'AUTO',
  `triggered_by` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT 'System Init',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `actuator_name` (`actuator_name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuator_status`
--

LOCK TABLES `actuator_status` WRITE;
/*!40000 ALTER TABLE `actuator_status` DISABLE KEYS */;
INSERT INTO `actuator_status` VALUES (1,'pump_1',0,'AUTO','Initial state: OFF','2026-09-19 08:01:25'),(2,'fan_motor_1',0,'AUTO','Initial state: OFF','2026-09-19 08:01:25'),(3,'led_grow_1',0,'AUTO','Initial state: OFF','2026-09-19 08:01:25'),(4,'pump',0,'AUTO','WATCHDOG: Max runtime exceeded (45s)','2026-09-19 08:50:35'),(5,'fan',0,'AUTO','Auto: Temp Normalized (<= 280)','2026-09-19 08:30:31'),(6,'led',0,'AUTO','Status Normal: Water level >= 500','2026-09-19 08:24:29');
/*!40000 ALTER TABLE `actuator_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `security_audit_logs`
--

DROP TABLE IF EXISTS `security_audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `security_audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `severity` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `details` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '127.0.0.1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_audit_logs`
--

LOCK TABLES `security_audit_logs` WRITE;
/*!40000 ALTER TABLE `security_audit_logs` DISABLE KEYS */;
INSERT INTO `security_audit_logs` VALUES (1,'SYSTEM_BOOT','INFO','Farm Defense Edge IoT initialized. All safety interlocks armed.','127.0.0.1','2026-09-19 08:08:25'),(2,'SYSTEM_BOOT','INFO','Farm Defense Edge IoT initialized. All safety interlocks armed.','127.0.0.1','2026-09-19 08:08:37'),(3,'SYSTEM_ONLINE','INFO','Farm Defense Edge server launched by operator.','127.0.0.1','2026-09-19 08:10:44'),(4,'AUTOMATION_EVENT','INFO','Pump ON: Moisture 30.37% < 35.0%','127.0.0.1','2026-09-19 08:10:44'),(5,'MANUAL_OVERRIDE','INFO','Operator manually set pump -> OFF','127.0.0.1','2026-09-19 08:11:27'),(6,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:12:56'),(7,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:13:51'),(8,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:14:02'),(9,'MANUAL_OVERRIDE','INFO','Operator manually set fan -> ON','127.0.0.1','2026-09-19 08:14:06'),(10,'MANUAL_OVERRIDE','INFO','Operator manually set fan -> OFF','127.0.0.1','2026-09-19 08:14:08'),(11,'MANUAL_OVERRIDE','INFO','Operator manually set pump -> ON','127.0.0.1','2026-09-19 08:14:10'),(12,'MANUAL_OVERRIDE','INFO','Operator manually set pump -> OFF','127.0.0.1','2026-09-19 08:14:10'),(13,'MANUAL_OVERRIDE','INFO','Operator manually set fan -> ON','127.0.0.1','2026-09-19 08:14:25'),(14,'MANUAL_OVERRIDE','INFO','Operator manually set fan -> OFF','127.0.0.1','2026-09-19 08:14:28'),(15,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:14:33'),(16,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:14:40'),(17,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:18:00'),(18,'SYSTEM_ONLINE','INFO','Farm Defense Edge server launched by operator.','127.0.0.1','2026-09-19 08:22:29'),(19,'MODE_CHANGE','INFO','Actuator pump returned to AUTO mode','127.0.0.1','2026-09-19 08:22:51'),(20,'AUTOMATION_EVENT','INFO','Pump ON: Soil 442.2 < 500','127.0.0.1','2026-09-19 08:22:51'),(21,'MODE_CHANGE','INFO','Actuator fan returned to AUTO mode','127.0.0.1','2026-09-19 08:22:51'),(22,'AUTOMATION_EVENT','INFO','Auto: Temp high (318.4 > 300)','127.0.0.1','2026-09-19 08:22:51'),(23,'MODE_CHANGE','INFO','Actuator led returned to AUTO mode','127.0.0.1','2026-09-19 08:22:51'),(24,'WATER_LEVEL_ALERT','WARN','Water level below 500: 410.0','127.0.0.1','2026-09-19 08:23:50'),(25,'WATCHDOG_TRIGGER','WARN','Runaway pump shut off after 45s continuous operation','127.0.0.1','2026-09-19 08:24:30'),(26,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:25:19'),(27,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:25:30'),(28,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:25:30'),(29,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:28:06'),(30,'AUTOMATION_EVENT','INFO','Pump ON: Soil 495.4 < 500','127.0.0.1','2026-09-19 08:30:31'),(31,'AUTOMATION_EVENT','INFO','Fan OFF: Temp stabilized','127.0.0.1','2026-09-19 08:30:31'),(32,'WATCHDOG_TRIGGER','WARN','Runaway pump shut off after 45s continuous operation','127.0.0.1','2026-09-19 08:31:31'),(33,'AUTOMATION_EVENT','INFO','Pump ON: Soil 498.0 < 500','127.0.0.1','2026-09-19 08:36:32'),(34,'WATCHDOG_TRIGGER','WARN','Runaway pump shut off after 45s continuous operation','127.0.0.1','2026-09-19 08:37:32'),(35,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:43:12'),(36,'AUTOMATION_EVENT','INFO','Pump ON: Soil 495.9 < 500','127.0.0.1','2026-09-19 08:43:33'),(37,'WATCHDOG_TRIGGER','WARN','Runaway pump shut off after 45s continuous operation','127.0.0.1','2026-09-19 08:44:34'),(38,'INTERNAL_ERROR','WARN','404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.','127.0.0.1','2026-09-19 08:45:54'),(39,'AUTOMATION_EVENT','INFO','Pump ON: Soil 494.4 < 500','127.0.0.1','2026-09-19 08:49:35'),(40,'WATCHDOG_TRIGGER','WARN','Runaway pump shut off after 45s continuous operation','127.0.0.1','2026-09-19 08:50:35');
/*!40000 ALTER TABLE `security_audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_data`
--

DROP TABLE IF EXISTS `sensor_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sensor_position` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sensor_value` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_sensor_time` (`sensor_position`,`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_data`
--

LOCK TABLES `sensor_data` WRITE;
/*!40000 ALTER TABLE `sensor_data` DISABLE KEYS */;
INSERT INTO `sensor_data` VALUES (1,'water_level',82.50,'2026-09-19 08:08:25'),(2,'soil_moisture',34.00,'2026-09-19 08:08:25'),(3,'temperature',28.50,'2026-09-19 08:08:25'),(4,'humidity',65.00,'2026-09-19 08:08:25'),(5,'water_level',82.50,'2026-09-19 08:08:37'),(6,'soil_moisture',34.00,'2026-09-19 08:08:37'),(7,'temperature',28.50,'2026-09-19 08:08:37'),(8,'humidity',65.00,'2026-09-19 08:08:37'),(9,'water_level',78.50,'2026-09-19 08:10:44'),(10,'soil_moisture',30.37,'2026-09-19 08:10:44'),(11,'temperature',29.30,'2026-09-19 08:10:44'),(12,'humidity',68.70,'2026-09-19 08:10:44'),(13,'water_level',78.50,'2026-09-19 08:11:39'),(14,'soil_moisture',29.28,'2026-09-19 08:11:39'),(15,'temperature',29.20,'2026-09-19 08:11:39'),(16,'humidity',68.50,'2026-09-19 08:11:39'),(17,'water_level',78.50,'2026-09-19 08:11:44'),(18,'soil_moisture',28.08,'2026-09-19 08:11:44'),(19,'temperature',29.50,'2026-09-19 08:11:44'),(20,'humidity',68.50,'2026-09-19 08:11:44'),(21,'water_level',78.50,'2026-09-19 08:12:44'),(22,'soil_moisture',26.60,'2026-09-19 08:12:44'),(23,'temperature',29.60,'2026-09-19 08:12:44'),(24,'humidity',68.90,'2026-09-19 08:12:44'),(25,'water_level',78.50,'2026-09-19 08:13:44'),(26,'soil_moisture',25.91,'2026-09-19 08:13:44'),(27,'temperature',29.30,'2026-09-19 08:13:44'),(28,'humidity',68.40,'2026-09-19 08:13:44'),(29,'water_level',78.50,'2026-09-19 08:13:57'),(30,'soil_moisture',25.09,'2026-09-19 08:13:57'),(31,'temperature',29.10,'2026-09-19 08:13:57'),(32,'humidity',68.70,'2026-09-19 08:13:57'),(33,'water_level',78.50,'2026-09-19 08:14:19'),(34,'soil_moisture',24.45,'2026-09-19 08:14:19'),(35,'temperature',29.00,'2026-09-19 08:14:19'),(36,'humidity',68.80,'2026-09-19 08:14:19'),(37,'water_level',78.50,'2026-09-19 08:14:45'),(38,'soil_moisture',23.46,'2026-09-19 08:14:45'),(39,'temperature',28.80,'2026-09-19 08:14:45'),(40,'humidity',69.90,'2026-09-19 08:14:45'),(41,'water_level',78.50,'2026-09-19 08:15:45'),(42,'soil_moisture',22.04,'2026-09-19 08:15:45'),(43,'temperature',28.70,'2026-09-19 08:15:45'),(44,'humidity',69.40,'2026-09-19 08:15:45'),(45,'water_level',78.50,'2026-09-19 08:16:45'),(46,'soil_moisture',20.30,'2026-09-19 08:16:45'),(47,'temperature',29.00,'2026-09-19 08:16:45'),(48,'humidity',68.80,'2026-09-19 08:16:45'),(49,'water_level',78.50,'2026-09-19 08:17:45'),(50,'soil_moisture',19.57,'2026-09-19 08:17:45'),(51,'temperature',29.20,'2026-09-19 08:17:45'),(52,'humidity',69.00,'2026-09-19 08:17:45'),(53,'water_level',78.50,'2026-09-19 08:18:45'),(54,'soil_moisture',18.58,'2026-09-19 08:18:46'),(55,'temperature',29.50,'2026-09-19 08:18:46'),(56,'humidity',70.00,'2026-09-19 08:18:46'),(57,'water_level',78.50,'2026-09-19 08:19:46'),(58,'soil_moisture',18.00,'2026-09-19 08:19:46'),(59,'temperature',29.30,'2026-09-19 08:19:46'),(60,'humidity',69.20,'2026-09-19 08:19:46'),(61,'water_level',78.50,'2026-09-19 08:20:46'),(62,'soil_moisture',18.00,'2026-09-19 08:20:46'),(63,'temperature',29.70,'2026-09-19 08:20:46'),(64,'humidity',70.10,'2026-09-19 08:20:46'),(65,'water_level',78.50,'2026-09-19 08:21:46'),(66,'soil_moisture',18.00,'2026-09-19 08:21:46'),(67,'temperature',30.00,'2026-09-19 08:21:46'),(68,'humidity',71.10,'2026-09-19 08:21:46'),(69,'water_level',680.00,'2026-09-19 08:22:29'),(70,'soil_moisture',444.81,'2026-09-19 08:22:29'),(71,'temperature',318.30,'2026-09-19 08:22:29'),(72,'humidity',64.80,'2026-09-19 08:22:29'),(73,'water_level',680.00,'2026-09-19 08:22:44'),(74,'soil_moisture',442.18,'2026-09-19 08:22:44'),(75,'temperature',318.40,'2026-09-19 08:22:44'),(76,'humidity',65.20,'2026-09-19 08:22:44'),(77,'water_level',672.60,'2026-09-19 08:22:52'),(78,'soil_moisture',466.36,'2026-09-19 08:22:52'),(79,'temperature',313.68,'2026-09-19 08:22:52'),(80,'humidity',63.60,'2026-09-19 08:22:52'),(81,'water_level',662.80,'2026-09-19 08:23:29'),(82,'soil_moisture',486.28,'2026-09-19 08:23:29'),(83,'temperature',308.78,'2026-09-19 08:23:29'),(84,'humidity',62.47,'2026-09-19 08:23:29'),(85,'water_level',410.00,'2026-09-19 08:23:50'),(86,'water_level',658.77,'2026-09-19 08:24:29'),(87,'soil_moisture',514.08,'2026-09-19 08:24:29'),(88,'temperature',304.26,'2026-09-19 08:24:29'),(89,'humidity',61.14,'2026-09-19 08:24:29'),(90,'water_level',658.77,'2026-09-19 08:25:30'),(91,'soil_moisture',512.06,'2026-09-19 08:25:30'),(92,'temperature',299.51,'2026-09-19 08:25:30'),(93,'humidity',59.46,'2026-09-19 08:25:30'),(94,'water_level',658.77,'2026-09-19 08:26:30'),(95,'soil_moisture',509.02,'2026-09-19 08:26:30'),(96,'temperature',296.02,'2026-09-19 08:26:30'),(97,'humidity',58.02,'2026-09-19 08:26:30'),(98,'water_level',658.77,'2026-09-19 08:27:30'),(99,'soil_moisture',506.14,'2026-09-19 08:27:30'),(100,'temperature',292.13,'2026-09-19 08:27:30'),(101,'humidity',55.81,'2026-09-19 08:27:30'),(102,'water_level',658.77,'2026-09-19 08:28:30'),(103,'soil_moisture',503.33,'2026-09-19 08:28:30'),(104,'temperature',287.03,'2026-09-19 08:28:30'),(105,'humidity',53.46,'2026-09-19 08:28:30'),(106,'water_level',658.77,'2026-09-19 08:29:30'),(107,'soil_moisture',501.28,'2026-09-19 08:29:30'),(108,'temperature',281.84,'2026-09-19 08:29:30'),(109,'humidity',52.18,'2026-09-19 08:29:30'),(110,'water_level',658.77,'2026-09-19 08:30:31'),(111,'soil_moisture',495.37,'2026-09-19 08:30:31'),(112,'temperature',278.53,'2026-09-19 08:30:31'),(113,'humidity',50.53,'2026-09-19 08:30:31'),(114,'water_level',651.03,'2026-09-19 08:31:31'),(115,'soil_moisture',518.80,'2026-09-19 08:31:31'),(116,'temperature',279.90,'2026-09-19 08:31:31'),(117,'humidity',50.70,'2026-09-19 08:31:31'),(118,'water_level',651.03,'2026-09-19 08:32:31'),(119,'soil_moisture',515.78,'2026-09-19 08:32:31'),(120,'temperature',279.40,'2026-09-19 08:32:31'),(121,'humidity',51.40,'2026-09-19 08:32:31'),(122,'water_level',651.03,'2026-09-19 08:33:31'),(123,'soil_moisture',510.26,'2026-09-19 08:33:31'),(124,'temperature',281.10,'2026-09-19 08:33:31'),(125,'humidity',51.60,'2026-09-19 08:33:31'),(126,'water_level',651.03,'2026-09-19 08:34:31'),(127,'soil_moisture',504.40,'2026-09-19 08:34:31'),(128,'temperature',280.80,'2026-09-19 08:34:31'),(129,'humidity',51.70,'2026-09-19 08:34:31'),(130,'water_level',651.03,'2026-09-19 08:35:32'),(131,'soil_moisture',500.33,'2026-09-19 08:35:32'),(132,'temperature',282.60,'2026-09-19 08:35:32'),(133,'humidity',52.60,'2026-09-19 08:35:32'),(134,'water_level',651.03,'2026-09-19 08:36:32'),(135,'soil_moisture',498.00,'2026-09-19 08:36:32'),(136,'temperature',284.10,'2026-09-19 08:36:32'),(137,'humidity',51.90,'2026-09-19 08:36:32'),(138,'water_level',641.29,'2026-09-19 08:37:32'),(139,'soil_moisture',519.88,'2026-09-19 08:37:32'),(140,'temperature',284.40,'2026-09-19 08:37:32'),(141,'humidity',52.90,'2026-09-19 08:37:32'),(142,'water_level',641.29,'2026-09-19 08:38:32'),(143,'soil_moisture',513.96,'2026-09-19 08:38:32'),(144,'temperature',285.80,'2026-09-19 08:38:32'),(145,'humidity',53.20,'2026-09-19 08:38:32'),(146,'water_level',641.29,'2026-09-19 08:39:32'),(147,'soil_moisture',511.92,'2026-09-19 08:39:32'),(148,'temperature',287.00,'2026-09-19 08:39:32'),(149,'humidity',52.50,'2026-09-19 08:39:32'),(150,'water_level',641.29,'2026-09-19 08:40:33'),(151,'soil_moisture',509.16,'2026-09-19 08:40:33'),(152,'temperature',287.20,'2026-09-19 08:40:33'),(153,'humidity',52.20,'2026-09-19 08:40:33'),(154,'water_level',641.29,'2026-09-19 08:41:33'),(155,'soil_moisture',505.71,'2026-09-19 08:41:33'),(156,'temperature',286.60,'2026-09-19 08:41:33'),(157,'humidity',52.70,'2026-09-19 08:41:33'),(158,'water_level',641.29,'2026-09-19 08:42:33'),(159,'soil_moisture',500.61,'2026-09-19 08:42:33'),(160,'temperature',286.50,'2026-09-19 08:42:33'),(161,'humidity',52.40,'2026-09-19 08:42:33'),(162,'water_level',641.29,'2026-09-19 08:43:33'),(163,'soil_moisture',495.86,'2026-09-19 08:43:33'),(164,'temperature',285.70,'2026-09-19 08:43:33'),(165,'humidity',52.90,'2026-09-19 08:43:33'),(166,'water_level',636.90,'2026-09-19 08:44:33'),(167,'soil_moisture',512.93,'2026-09-19 08:44:33'),(168,'temperature',284.80,'2026-09-19 08:44:33'),(169,'humidity',53.30,'2026-09-19 08:44:33'),(170,'water_level',636.90,'2026-09-19 08:45:34'),(171,'soil_moisture',510.86,'2026-09-19 08:45:34'),(172,'temperature',283.90,'2026-09-19 08:45:34'),(173,'humidity',53.10,'2026-09-19 08:45:34'),(174,'water_level',636.90,'2026-09-19 08:46:34'),(175,'soil_moisture',508.82,'2026-09-19 08:46:34'),(176,'temperature',284.50,'2026-09-19 08:46:34'),(177,'humidity',53.40,'2026-09-19 08:46:34'),(178,'water_level',636.90,'2026-09-19 08:47:34'),(179,'soil_moisture',503.23,'2026-09-19 08:47:34'),(180,'temperature',286.20,'2026-09-19 08:47:34'),(181,'humidity',54.20,'2026-09-19 08:47:34'),(182,'water_level',636.90,'2026-09-19 08:48:34'),(183,'soil_moisture',500.14,'2026-09-19 08:48:34'),(184,'temperature',286.90,'2026-09-19 08:48:34'),(185,'humidity',54.90,'2026-09-19 08:48:34'),(186,'water_level',636.90,'2026-09-19 08:49:34'),(187,'soil_moisture',494.43,'2026-09-19 08:49:34'),(188,'temperature',288.40,'2026-09-19 08:49:34'),(189,'humidity',54.20,'2026-09-19 08:49:35'),(190,'water_level',629.34,'2026-09-19 08:50:35'),(191,'soil_moisture',513.03,'2026-09-19 08:50:35'),(192,'temperature',289.70,'2026-09-19 08:50:35'),(193,'humidity',54.70,'2026-09-19 08:50:35'),(194,'water_level',629.34,'2026-09-19 08:51:35'),(195,'soil_moisture',510.50,'2026-09-19 08:51:35'),(196,'temperature',291.50,'2026-09-19 08:51:35'),(197,'humidity',54.50,'2026-09-19 08:51:35'),(198,'water_level',629.34,'2026-09-19 08:52:35'),(199,'soil_moisture',504.67,'2026-09-19 08:52:35'),(200,'temperature',291.10,'2026-09-19 08:52:35'),(201,'humidity',54.30,'2026-09-19 08:52:35');
/*!40000 ALTER TABLE `sensor_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-19 16:52:42
