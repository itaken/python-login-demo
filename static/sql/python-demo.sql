-- MySQL dump 10.13  Distrib 5.7.18-15, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: python-demo
-- ------------------------------------------------------
-- Server version	5.7.18-15

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
/*!50717 SET @rocksdb_bulk_load_var_name='rocksdb_bulk_load' */;
/*!50717 SELECT COUNT(*) INTO @rocksdb_has_p_s_session_variables FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'performance_schema' AND TABLE_NAME = 'session_variables' */;
/*!50717 SET @rocksdb_get_is_supported = IF (@rocksdb_has_p_s_session_variables, 'SELECT COUNT(*) INTO @rocksdb_is_supported FROM performance_schema.session_variables WHERE VARIABLE_NAME=?', 'SELECT 0') */;
/*!50717 PREPARE s FROM @rocksdb_get_is_supported */;
/*!50717 EXECUTE s USING @rocksdb_bulk_load_var_name */;
/*!50717 DEALLOCATE PREPARE s */;
/*!50717 SET @rocksdb_enable_bulk_load = IF (@rocksdb_is_supported, 'SET SESSION rocksdb_bulk_load = 1', 'SET @rocksdb_dummy_bulk_load = 0') */;
/*!50717 PREPARE s FROM @rocksdb_enable_bulk_load */;
/*!50717 EXECUTE s */;
/*!50717 DEALLOCATE PREPARE s */;

--
-- Table structure for table `ita_connector`
--

DROP TABLE IF EXISTS `ita_connector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ita_connector` (
  `uid` int(11) NOT NULL,
  `access_token` varchar(100) NOT NULL,
  `update_time` datetime NOT NULL,
  `session_token` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ita_connector`
--

LOCK TABLES `ita_connector` WRITE;
/*!40000 ALTER TABLE `ita_connector` DISABLE KEYS */;
INSERT INTO `ita_connector` VALUES (100,'ebe5b685a8cda8143980a8b289ffde97','2017-08-04 17:24:35','72d04a211bdda8ad9473c8e69bc0fdbc'),(7,'c90b88c8759740fc3dc68a2cc202b635','2017-08-04 17:26:24','80e96a2e249e927ca9bf9c3b5526283d'),(8,'aa68fe0e42c591f10d566ded5b49f7ab','2017-08-04 17:18:43','9fdb8a7b27500867917d526e1b5e1ff7');
/*!40000 ALTER TABLE `ita_connector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ita_members`
--

DROP TABLE IF EXISTS `ita_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ita_members` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `password` varchar(100) NOT NULL,
  `enname` varchar(100) NOT NULL,
  `add_time` datetime NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `members_enname_IDX` (`enname`) USING HASH
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ita_members`
--

LOCK TABLES `ita_members` WRITE;
/*!40000 ALTER TABLE `ita_members` DISABLE KEYS */;
INSERT INTO `ita_members` VALUES (7,'admin','8508647f0e51db687aeda35c1cef229b','0da2ae7d2b403e40b50d7ca1d92be87d','2017-07-28 21:45:05'),(8,'itaken','3d5c0f4106f0de816cb3581d3245c344','ff3aecb792439106ee6fc903b1be1476','2017-07-28 21:45:32');
/*!40000 ALTER TABLE `ita_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'python-demo'
--
/*!50112 SET @disable_bulk_load = IF (@is_rocksdb_supported, 'SET SESSION rocksdb_bulk_load = @old_rocksdb_bulk_load', 'SET @dummy_rocksdb_bulk_load = 0') */;
/*!50112 PREPARE s FROM @disable_bulk_load */;
/*!50112 EXECUTE s */;
/*!50112 DEALLOCATE PREPARE s */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-11 17:53:02
