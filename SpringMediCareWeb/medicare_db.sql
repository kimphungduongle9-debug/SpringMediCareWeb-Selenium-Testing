-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: medicare_db
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `appointment_date` datetime NOT NULL,
  `status` enum('pending','confirmed','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appointment_id`),
  KEY `idx_appointment_patient_id` (`patient_id`),
  KEY `idx_appointment_doctor_id` (`doctor_id`),
  CONSTRAINT `fk_appointment_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`),
  CONSTRAINT `fk_appointment_patient` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,1,1,'2026-04-10 09:00:00','confirmed','Mệt khi vận động, khó thở nhẹ.','2026-04-09 09:00:00'),(2,2,2,'2026-04-10 10:30:00','pending','Kham da lieu','2026-04-09 09:15:00'),(3,3,2,'2026-04-10 12:00:00','confirmed','Kham benh ngoai da','2026-04-09 09:30:00'),(4,4,3,'2026-04-10 13:30:00','pending','Kham rang','2026-04-09 09:45:00'),(5,5,2,'2026-04-10 15:00:00','confirmed','Kham noi mut mong nuoc','2026-04-09 10:00:00'),(6,6,4,'2026-04-10 16:30:00','pending','Kham mat','2026-04-09 10:15:00'),(7,7,3,'2026-04-10 18:00:00','confirmed','KIem tra sau rang','2026-04-09 10:30:00'),(8,8,4,'2026-04-10 19:30:00','cancelled','Do do can va kham mat','2026-04-09 10:45:00'),(9,2,2,'2026-04-10 13:00:00','confirmed','Lich hen bo sung tu thong bao NC7','2026-04-10 08:20:00'),(10,1,1,'2026-04-10 14:00:00','completed','Hồi hộp, đau tức ngực nhẹ.','2026-04-10 08:40:00'),(11,1,1,'2026-04-11 08:00:00','completed','Đau ngực khi gắng sức, khó thở.','2026-05-29 14:53:58'),(13,1,1,'2026-04-11 10:00:00','pending','Mệt khi vận động nhiều.','2026-05-29 16:02:27'),(14,1,1,'2026-04-11 10:30:00','pending','Tim đập mạnh, lo lắng, mất ngủ.','2026-05-29 16:21:51'),(15,1,1,'2026-04-12 09:10:00','pending','Hay tức ngực khó chịu','2026-05-29 16:48:12'),(16,3,4,'2026-04-11 10:00:00','pending','Đỏ mắt, chảy nước mắt, ngứa, có ghèn','2026-05-30 19:39:12'),(17,3,2,'2026-04-11 10:00:00','confirmed','Ngứa, nổi mẩn đỏ','2026-05-30 19:40:34'),(18,3,2,'2026-06-07 14:00:00','pending','Mụn đầu đen, Mụn viêm, Da nhờn','2026-06-03 18:37:19'),(19,1,2,'2026-06-07 15:00:00','confirmed','Ngứa, Nổi mẩn đỏ, Khô da','2026-06-03 18:45:43'),(20,1,1,'2026-06-08 10:00:00','completed','mệt mỏi','2026-06-06 08:46:07'),(30,1,1,'2026-04-11 08:30:00','pending','','2026-07-24 12:11:37'),(34,1,1,'2026-04-11 09:00:00','cancelled','Đau đầu và sốt nhẹ.','2026-07-25 17:26:57'),(35,1,1,'2026-04-11 09:30:00','cancelled','','2026-07-25 17:28:08'),(36,1,1,'2026-04-11 15:30:00','cancelled','','2026-07-25 17:29:56'),(37,1,1,'2026-04-11 09:00:00','cancelled','Đau đầu và sốt nhẹ.','2026-07-28 22:28:25'),(38,1,1,'2026-04-11 09:30:00','cancelled','','2026-07-28 22:29:36'),(39,1,1,'2026-04-11 14:00:00','cancelled','Dữ liệu chuẩn bị cho TC-BOOKING-007','2026-07-28 22:31:18'),(40,1,1,'2026-04-11 15:30:00','cancelled','Dữ liệu chuẩn bị cho TC-BOOKING-008','2026-07-28 22:32:34'),(41,1,1,'2026-04-11 09:00:00','cancelled','Đau đầu và sốt nhẹ.','2026-07-28 22:35:57'),(42,1,1,'2026-04-11 09:30:00','cancelled','','2026-07-28 22:37:09'),(43,1,1,'2026-04-11 14:00:00','cancelled','Dữ liệu chuẩn bị cho TC-BOOKING-007','2026-07-28 22:38:12'),(44,1,1,'2026-04-11 15:30:00','cancelled','Dữ liệu chuẩn bị cho TC-BOOKING-008','2026-07-28 22:38:39'),(45,1,2,'2026-07-31 09:00:00','pending','Nổi nhiều nốt đỏ, ngứa và sưng một bên mặt.','2026-07-29 18:51:39'),(46,7,3,'2026-07-31 10:00:00','confirmed','TC-APPOINTMENT-002 - Admin xác nhận lịch','2026-07-29 20:11:42'),(47,7,3,'2026-07-31 14:00:00','cancelled','TC-APPOINTMENT-003 - Admin hủy lịch','2026-07-29 20:11:42'),(48,7,3,'2026-08-01 09:00:00','pending','TC-APPOINTMENT-004 - Bác sĩ chỉ xem hồ sơ','2026-07-29 20:11:42'),(49,7,3,'2026-08-01 10:00:00','pending','TC-APPOINTMENT-005 - Truy cập lịch chưa xác nhận','2026-07-29 20:11:42'),(50,7,3,'2026-08-01 14:00:00','confirmed','TC-APPOINTMENT-006 - Bác sĩ được khám','2026-07-29 20:11:42'),(51,7,3,'2026-08-02 09:00:00','confirmed','TC-APPOINTMENT-007 - Kiểm tra bác sĩ khác','2026-07-29 20:11:42'),(52,7,3,'2026-08-02 10:00:00','cancelled','TC-APPOINTMENT-008 - Lịch đã hủy','2026-07-29 20:11:42'),(53,7,3,'2026-08-02 14:00:00','completed','TC-APPOINTMENT-009 - Lưu hồ sơ và hoàn thành lịch','2026-07-29 20:11:42'),(54,7,3,'2026-08-10 09:00:00','completed','TC-MEDICAL-001','2026-07-30 21:37:25'),(55,7,3,'2026-08-10 10:00:00','confirmed','TC-MEDICAL-002','2026-07-30 21:37:25'),(56,7,3,'2026-08-10 14:00:00','confirmed','TC-MEDICAL-003','2026-07-30 21:37:25'),(57,7,3,'2026-08-11 09:00:00','completed','TC-MEDICAL-004','2026-07-30 21:37:25'),(58,7,3,'2026-08-11 10:00:00','completed','TC-MEDICAL-005','2026-07-30 21:37:25'),(59,7,3,'2026-08-11 14:00:00','completed','TC-MEDICAL-006','2026-07-30 21:37:25'),(60,7,3,'2026-08-12 09:00:00','completed','TC-MEDICAL-007','2026-07-30 21:37:25'),(61,7,3,'2026-08-12 10:00:00','completed','TC-MEDICAL-008','2026-07-31 13:00:56'),(62,7,3,'2026-08-12 14:00:00','completed','TC-MEDICAL-009','2026-07-31 13:00:56'),(63,7,3,'2026-08-01 07:00:00','completed','SELENIUM-TC-MEDICAL-007','2026-07-31 16:44:28'),(64,7,3,'2026-08-01 07:30:00','completed','SELENIUM-TC-MEDICAL-005','2026-07-31 17:21:13'),(65,7,3,'2026-08-01 08:00:00','completed','SELENIUM-TC-MEDICAL-006','2026-07-31 17:29:09'),(66,7,3,'2026-08-01 08:30:00','completed','SELENIUM-TC-MEDICAL-009','2026-07-31 22:39:39'),(67,7,3,'2026-08-01 09:30:00','completed','SELENIUM-TC-MEDICAL-001','2026-07-31 22:58:00'),(68,7,3,'2026-08-01 10:30:00','confirmed','SELENIUM-TC-MEDICAL-002','2026-07-31 23:12:20'),(69,7,3,'2026-08-01 11:00:00','confirmed','SELENIUM-TC-MEDICAL-003','2026-07-31 23:18:38'),(70,7,3,'2026-08-01 13:00:00','completed','SELENIUM-TC-MEDICAL-004','2026-07-31 23:25:41'),(71,7,3,'2026-08-01 13:30:00','completed','SELENIUM-TC-MEDICAL-008','2026-07-31 23:29:52'),(72,7,3,'2026-08-02 07:00:00','completed','SELENIUM-TC-MEDICAL-001','2026-08-01 14:57:31'),(78,7,3,'2026-08-02 07:30:00','cancelled','SELENIUM-TC-APPOINTMENT-002-1785574298','2026-08-01 15:51:39'),(79,7,3,'2026-08-02 07:30:00','cancelled','SELENIUM-TC-APPOINTMENT-003-1785574549','2026-08-01 15:55:50'),(80,7,3,'2026-08-02 07:30:00','cancelled','SELENIUM-TC-APPOINTMENT-003-1785574581','2026-08-01 15:56:22'),(81,7,3,'2026-08-02 07:30:00','cancelled','SELENIUM-TC-APPOINTMENT-002-1785574737','2026-08-01 15:58:58'),(82,7,3,'2026-08-02 07:30:00','pending','SELENIUM-TC-APPOINTMENT-005','2026-08-01 20:48:46'),(83,7,3,'2026-08-02 08:00:00','confirmed','SELENIUM-TC-APPOINTMENT-006','2026-08-01 20:55:24'),(84,7,3,'2026-08-02 08:30:00','confirmed','SELENIUM-TC-APPOINTMENT-007','2026-08-01 21:04:32'),(85,7,3,'2026-08-02 09:30:00','cancelled','SELENIUM-TC-APPOINTMENT-008','2026-08-01 21:11:15'),(86,7,3,'2026-08-02 09:30:00','completed','SELENIUM-TC-APPOINTMENT-009','2026-08-01 22:16:34'),(87,1,1,'2026-08-02 07:00:00','pending','SELENIUM-TC-APPOINTMENT-001-1785599469','2026-08-01 22:51:28'),(88,1,1,'2026-08-02 07:30:00','pending','SELENIUM-TC-APPOINTMENT-001-1785599624','2026-08-01 22:54:03'),(89,7,3,'2026-08-02 10:00:00','pending','SELENIUM-TC-APPOINTMENT-004','2026-08-01 22:58:06'),(90,7,3,'2026-08-03 07:00:00','confirmed','SELENIUM-TC-APPOINTMENT-002-1785654081','2026-08-02 14:01:22'),(91,7,3,'2026-08-03 07:30:00','cancelled','SELENIUM-TC-APPOINTMENT-003-1785654103','2026-08-02 14:01:44'),(92,7,3,'2026-08-03 07:30:00','completed','SELENIUM-TC-APPOINTMENT-009','2026-08-02 14:03:33'),(93,1,1,'2026-08-03 07:00:00','pending','SELENIUM-TC-APPOINTMENT-001-1785654232','2026-08-02 14:04:10'),(94,7,3,'2026-08-03 08:00:00','completed','SELENIUM-TC-MEDICAL-001','2026-08-02 14:11:45'),(95,1,1,'2026-04-11 09:00:00','cancelled','Đau đầu và sốt nhẹ.','2026-08-04 00:13:13'),(96,1,1,'2026-04-11 09:30:00','cancelled','','2026-08-04 00:14:25'),(97,1,1,'2026-04-11 14:00:00','cancelled','Dữ liệu chuẩn bị cho TC-BOOKING-007','2026-08-04 00:15:27'),(98,1,1,'2026-04-11 15:30:00','cancelled','Dữ liệu chuẩn bị cho TC-BOOKING-008','2026-08-04 00:15:55'),(99,7,3,'2026-08-05 07:00:00','completed','SELENIUM-TC-MEDICAL-001','2026-08-04 00:18:55'),(100,7,3,'2026-08-05 07:30:00','confirmed','SELENIUM-TC-APPOINTMENT-002-1785777809','2026-08-04 00:23:30'),(101,7,3,'2026-08-05 08:00:00','cancelled','SELENIUM-TC-APPOINTMENT-003-1785777831','2026-08-04 00:23:52'),(102,7,3,'2026-08-05 08:00:00','completed','SELENIUM-TC-APPOINTMENT-009','2026-08-04 00:25:40'),(103,1,1,'2026-08-05 07:00:00','pending','SELENIUM-TC-APPOINTMENT-001-1785777959','2026-08-04 00:26:18');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `uk_drug_category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Thuốc giảm đau - hạ sốt','Nhóm thuốc dùng để giảm đau nhẹ đến vừa và hạ sốt.','active'),(2,'Vitamin và khoáng chất','Nhóm thuốc bổ sung vitamin, khoáng chất, tăng sức đề kháng.','active'),(3,'Thuốc chống dị ứng','Nhóm thuốc hỗ trợ điều trị dị ứng, nổi mề đay, viêm mũi dị ứng.','active'),(4,'Thuốc tiêu hóa','Nhóm thuốc điều trị trào ngược dạ dày, khó tiêu, tiêu chảy.','active'),(5,'Thuốc kháng sinh','Nhóm thuốc điều trị nhiễm khuẩn, dùng theo chỉ định bác sĩ.','active'),(6,'Thuốc tim mạch - huyết áp','Nhóm thuốc điều trị tăng huyết áp, đau thắt ngực, bệnh tim mạch.','active'),(7,'Thuốc hô hấp','Nhóm thuốc hỗ trợ điều trị hen suyễn, co thắt phế quản.','active'),(8,'Thuốc kháng viêm','Nhóm thuốc giảm viêm, dùng theo chỉ định.','active'),(9,'Thuốc tẩy giun','Nhóm thuốc điều trị và dự phòng nhiễm giun sán.','active'),(10,'Thuốc răng hàm mặt','Nhóm thuốc điều trị nhiễm trùng răng miệng, viêm lợi, sâu răng.','active');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `specialty_id` int NOT NULL,
  `experience_years` int NOT NULL DEFAULT '0',
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `uk_doctor_user_id` (`user_id`),
  KEY `idx_doctor_specialty_id` (`specialty_id`),
  CONSTRAINT `fk_doctor_specialty` FOREIGN KEY (`specialty_id`) REFERENCES `specialty` (`specialty_id`),
  CONSTRAINT `fk_doctor_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (1,2,'Tran Binh',1,8,'https://res.cloudinary.com/dczz59gpu/image/upload/v1775723515/image6_mr167k.png'),(2,4,'Pham Dung',2,2,'https://res.cloudinary.com/dczz59gpu/image/upload/v1775723653/image7_j0izpd.png'),(3,8,'Ly Minh',5,3,'https://res.cloudinary.com/dczz59gpu/image/upload/v1775724405/image14_jab5qp.png'),(4,10,'Vu Thinh',7,4,'https://res.cloudinary.com/dczz59gpu/image/upload/v1775724612/image15_vdmxlr.png');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_schedule`
--

DROP TABLE IF EXISTS `doctor_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `work_date` date NOT NULL,
  `shift` enum('morning','afternoon','evening') NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `status` enum('available','unavailable') NOT NULL DEFAULT 'available',
  `note` text,
  PRIMARY KEY (`schedule_id`),
  KEY `fk_doctor_schedule_doctor` (`doctor_id`),
  CONSTRAINT `fk_doctor_schedule_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_schedule`
--

LOCK TABLES `doctor_schedule` WRITE;
/*!40000 ALTER TABLE `doctor_schedule` DISABLE KEYS */;
INSERT INTO `doctor_schedule` VALUES (1,1,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(2,1,'2026-04-11','afternoon','13:00:00','17:00:00','available','Ca chiều'),(3,1,'2026-04-11','evening','17:30:00','21:00:00','available','Ca tối'),(4,2,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(5,2,'2026-04-11','afternoon','13:00:00','17:00:00','available','Ca chiều'),(6,2,'2026-04-11','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(7,3,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(8,3,'2026-04-11','afternoon','13:00:00','17:00:00','available','Ca chiều'),(9,3,'2026-04-11','evening','17:30:00','21:00:00','available','Ca tối'),(10,4,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(11,4,'2026-04-11','afternoon','13:00:00','17:00:00','unavailable','Bác sĩ nghỉ ca chiều'),(12,4,'2026-04-11','evening','17:30:00','21:00:00','available','Ca tối'),(13,1,'2026-04-12','morning','07:00:00','11:30:00','available','Ca sáng'),(14,1,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(15,1,'2026-04-12','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(16,2,'2026-04-12','morning','07:00:00','11:30:00','available','Ca sáng'),(17,2,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(18,2,'2026-04-12','evening','17:30:00','21:00:00','available','Ca tối'),(19,3,'2026-04-12','morning','07:00:00','11:30:00','unavailable','Bác sĩ nghỉ ca sáng'),(20,3,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(21,3,'2026-04-12','evening','17:30:00','21:00:00','available','Ca tối'),(22,4,'2026-04-12','morning','07:00:00','11:30:00','available','Ca sáng'),(23,4,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(24,4,'2026-04-12','evening','17:30:00','21:00:00','available','Ca tối'),(25,1,'2026-06-07','morning','07:00:00','11:30:00','available','Ca sáng'),(26,1,'2026-06-07','afternoon','13:00:00','17:00:00','available','Ca chiều'),(27,1,'2026-06-07','evening','17:30:00','21:00:00','available','Ca tối'),(28,2,'2026-06-07','morning','07:00:00','11:30:00','available','Ca sáng'),(29,2,'2026-06-07','afternoon','13:00:00','17:00:00','available','Ca chiều'),(30,2,'2026-06-07','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(31,1,'2026-06-08','morning','07:00:00','11:30:00','available','Ca sáng'),(32,1,'2026-06-08','afternoon','13:00:00','17:00:00','available','Ca chiều'),(33,1,'2026-06-08','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(34,2,'2026-06-08','morning','07:00:00','11:30:00','available','Ca sáng'),(35,2,'2026-06-08','afternoon','13:00:00','17:00:00','available','Ca chiều'),(36,2,'2026-06-08','evening','17:30:00','21:00:00','available','Ca tối'),(37,1,'2026-06-09','morning','07:00:00','11:30:00','available','Ca sáng'),(38,1,'2026-06-09','afternoon','13:00:00','17:00:00','available','Ca chiều'),(39,2,'2026-06-09','morning','07:00:00','11:30:00','available','Ca sáng'),(40,2,'2026-06-09','afternoon','13:00:00','17:00:00','available','Ca chiều'),(41,4,'2026-07-30','morning','07:00:00','11:30:00','available','Ca sáng'),(42,4,'2026-07-30','afternoon','13:00:00','17:00:00','available','Ca chiều'),(43,4,'2026-07-30','evening','17:30:00','21:00:00','available','Ca tối'),(44,3,'2026-07-30','morning','07:00:00','11:30:00','available','Ca sáng'),(45,3,'2026-07-30','afternoon','13:00:00','17:00:00','available','Ca chiều'),(46,3,'2026-07-30','evening','17:30:00','21:00:00','available','Ca tối'),(47,2,'2026-07-30','morning','07:00:00','11:30:00','available','Ca sáng'),(48,2,'2026-07-30','afternoon','13:00:00','17:00:00','available','Ca chiều'),(49,2,'2026-07-30','evening','17:30:00','21:00:00','available','Ca tối'),(50,1,'2026-07-30','morning','07:00:00','11:30:00','available','Ca sáng'),(51,1,'2026-07-30','afternoon','13:00:00','17:00:00','available','Ca chiều'),(52,1,'2026-07-30','evening','17:30:00','21:00:00','available','Ca tối'),(53,4,'2026-07-31','morning','07:00:00','11:30:00','available','Ca sáng'),(54,4,'2026-07-31','afternoon','13:00:00','17:00:00','available','Ca chiều'),(55,4,'2026-07-31','evening','17:30:00','21:00:00','available','Ca tối'),(56,3,'2026-07-31','morning','07:00:00','11:30:00','available','Ca sáng'),(57,3,'2026-07-31','afternoon','13:00:00','17:00:00','available','Ca chiều'),(58,3,'2026-07-31','evening','17:30:00','21:00:00','available','Ca tối'),(59,2,'2026-07-31','morning','07:00:00','11:30:00','available','Ca sáng'),(60,2,'2026-07-31','afternoon','13:00:00','17:00:00','available','Ca chiều'),(61,2,'2026-07-31','evening','17:30:00','21:00:00','available','Ca tối'),(62,1,'2026-07-31','morning','07:00:00','11:30:00','available','Ca sáng'),(63,1,'2026-07-31','afternoon','13:00:00','17:00:00','available','Ca chiều'),(64,1,'2026-07-31','evening','17:30:00','21:00:00','available','Ca tối'),(65,4,'2026-08-01','morning','07:00:00','11:30:00','available','Ca sáng'),(66,4,'2026-08-01','afternoon','13:00:00','17:00:00','available','Ca chiều'),(67,4,'2026-08-01','evening','17:30:00','21:00:00','available','Ca tối'),(68,3,'2026-08-01','morning','07:00:00','11:30:00','available','Ca sáng'),(69,3,'2026-08-01','afternoon','13:00:00','17:00:00','available','Ca chiều'),(70,3,'2026-08-01','evening','17:30:00','21:00:00','available','Ca tối'),(71,2,'2026-08-01','morning','07:00:00','11:30:00','available','Ca sáng'),(72,2,'2026-08-01','afternoon','13:00:00','17:00:00','available','Ca chiều'),(73,2,'2026-08-01','evening','17:30:00','21:00:00','available','Ca tối'),(74,1,'2026-08-01','morning','07:00:00','11:30:00','available','Ca sáng'),(75,1,'2026-08-01','afternoon','13:00:00','17:00:00','available','Ca chiều'),(76,1,'2026-08-01','evening','17:30:00','21:00:00','available','Ca tối'),(77,4,'2026-08-02','morning','07:00:00','11:30:00','available','Ca sáng'),(78,4,'2026-08-02','afternoon','13:00:00','17:00:00','available','Ca chiều'),(79,4,'2026-08-02','evening','17:30:00','21:00:00','available','Ca tối'),(80,3,'2026-08-02','morning','07:00:00','11:30:00','available','Ca sáng'),(81,3,'2026-08-02','afternoon','13:00:00','17:00:00','available','Ca chiều'),(82,3,'2026-08-02','evening','17:30:00','21:00:00','available','Ca tối'),(83,2,'2026-08-02','morning','07:00:00','11:30:00','available','Ca sáng'),(84,2,'2026-08-02','afternoon','13:00:00','17:00:00','available','Ca chiều'),(85,2,'2026-08-02','evening','17:30:00','21:00:00','available','Ca tối'),(86,1,'2026-08-02','morning','07:00:00','11:30:00','available','Ca sáng'),(87,1,'2026-08-02','afternoon','13:00:00','17:00:00','available','Ca chiều'),(88,1,'2026-08-02','evening','17:30:00','21:00:00','available','Ca tối'),(89,4,'2026-08-03','morning','07:00:00','11:30:00','available','Ca sáng'),(90,4,'2026-08-03','afternoon','13:00:00','17:00:00','available','Ca chiều'),(91,4,'2026-08-03','evening','17:30:00','21:00:00','available','Ca tối'),(92,3,'2026-08-03','morning','07:00:00','11:30:00','available','Ca sáng'),(93,3,'2026-08-03','afternoon','13:00:00','17:00:00','available','Ca chiều'),(94,3,'2026-08-03','evening','17:30:00','21:00:00','available','Ca tối'),(95,2,'2026-08-03','morning','07:00:00','11:30:00','available','Ca sáng'),(96,2,'2026-08-03','afternoon','13:00:00','17:00:00','available','Ca chiều'),(97,2,'2026-08-03','evening','17:30:00','21:00:00','available','Ca tối'),(98,1,'2026-08-03','morning','07:00:00','11:30:00','available','Ca sáng'),(99,1,'2026-08-03','afternoon','13:00:00','17:00:00','available','Ca chiều'),(100,1,'2026-08-03','evening','17:30:00','21:00:00','available','Ca tối'),(101,4,'2026-08-04','morning','07:00:00','11:30:00','available','Ca sáng'),(102,4,'2026-08-04','afternoon','13:00:00','17:00:00','available','Ca chiều'),(103,4,'2026-08-04','evening','17:30:00','21:00:00','available','Ca tối'),(104,3,'2026-08-04','morning','07:00:00','11:30:00','available','Ca sáng'),(105,3,'2026-08-04','afternoon','13:00:00','17:00:00','available','Ca chiều'),(106,3,'2026-08-04','evening','17:30:00','21:00:00','available','Ca tối'),(107,2,'2026-08-04','morning','07:00:00','11:30:00','available','Ca sáng'),(108,2,'2026-08-04','afternoon','13:00:00','17:00:00','available','Ca chiều'),(109,2,'2026-08-04','evening','17:30:00','21:00:00','available','Ca tối'),(110,1,'2026-08-04','morning','07:00:00','11:30:00','available','Ca sáng'),(111,1,'2026-08-04','afternoon','13:00:00','17:00:00','available','Ca chiều'),(112,1,'2026-08-04','evening','17:30:00','21:00:00','available','Ca tối'),(113,4,'2026-08-05','morning','07:00:00','11:30:00','available','Ca sáng'),(114,4,'2026-08-05','afternoon','13:00:00','17:00:00','available','Ca chiều'),(115,4,'2026-08-05','evening','17:30:00','21:00:00','available','Ca tối'),(116,3,'2026-08-05','morning','07:00:00','11:30:00','available','Ca sáng'),(117,3,'2026-08-05','afternoon','13:00:00','17:00:00','available','Ca chiều'),(118,3,'2026-08-05','evening','17:30:00','21:00:00','available','Ca tối'),(119,2,'2026-08-05','morning','07:00:00','11:30:00','available','Ca sáng'),(120,2,'2026-08-05','afternoon','13:00:00','17:00:00','available','Ca chiều'),(121,2,'2026-08-05','evening','17:30:00','21:00:00','available','Ca tối'),(122,1,'2026-08-05','morning','07:00:00','11:30:00','available','Ca sáng'),(123,1,'2026-08-05','afternoon','13:00:00','17:00:00','available','Ca chiều'),(124,1,'2026-08-05','evening','17:30:00','21:00:00','available','Ca tối');
/*!40000 ALTER TABLE `doctor_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drug`
--

DROP TABLE IF EXISTS `drug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drug` (
  `drug_id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `quantity` int NOT NULL DEFAULT '0',
  `min_quantity` int NOT NULL DEFAULT '20',
  `production_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `dosage_form` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `strength` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `manufacturer` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('available','low_stock','expired','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'available',
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`drug_id`),
  KEY `idx_drug_category_id` (`category_id`),
  CONSTRAINT `fk_drug_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drug`
--

LOCK TABLES `drug` WRITE;
/*!40000 ALTER TABLE `drug` DISABLE KEYS */;
INSERT INTO `drug` VALUES (1,1,'Paracetamol','Giam dau ha sot',5000.00,99,20,'2025-01-01','2027-12-31','Viên nén','viên','500mg','DHG Pharma','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726283/Paracetamol_ewnf42.jpg'),(2,2,'Vitamin C','Tang suc de khang',3000.00,199,20,'2024-10-15','2027-10-15','Viên nén','viên','500mg','Domesco','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726425/Vitamin_C_vmc8io.png'),(3,3,'Cetirizine','Thuoc chong di ung',7000.00,150,20,'2024-08-20','2027-08-20','Viên nén','viên','10mg','Stada','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726456/Cetirizine_nlrkhh.jpg'),(4,1,'Panadol Extra','Giam dau nhanh, ha sot, co cafein giup tinh tao',6000.00,299,20,'2025-02-10','2028-02-10','Viên nén','viên','500mg + 65mg','GSK','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726587/PanadolExtra_en6wuf.jpg'),(5,4,'Gaviscon','Dieu tri trao nguoc da day va o chua',2000.00,120,20,'2025-03-01','2028-03-01','Gói hỗn dịch','gói','10ml','Reckitt','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726805/Gaviscon_evnufe.jpg'),(6,5,'Augmentin','Khang sinh dieu tri nhiem khuan duong ho hap',50000.00,150,20,'2025-01-15','2027-01-15','Viên nén','viên','625mg','GSK','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726846/Augmentin_c2k4mg.jpg'),(7,6,'Amlodipine','Dieu tri cao huyet ap va dau that nguc',40000.00,50,20,'2024-12-01','2027-12-01','Viên nén','viên','5mg','Stella','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726876/Amlodipine_qr9yot.jpg'),(8,7,'Salbutamol','Thuoc xit gian phe quan, dieu tri hen suyen',100000.00,60,20,'2025-02-20','2027-02-20','Bình xịt','bình','100mcg/liều','GSK','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726914/Salbutamol_hlfvob.jpg'),(9,1,'Efferalgan','Giam dau, ha sot dang sui bot',50000.00,15,20,'2025-01-10','2028-01-10','Viên sủi','viên','500mg','UPSA','low_stock','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726960/Efferalgan_jqcfn7.jpg'),(10,1,'Hapacol 150','Thuoc ha sot chuyen dung cho tre em',30000.00,70,20,'2025-03-15','2028-03-15','Gói bột','gói','150mg','DHG Pharma','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727012/Hapacol150_hgtmz5.jpg'),(11,8,'Dexamethasone','Thuoc khang viem manh, dieu tri di ung nang',10000.00,80,20,'2025-02-05','2027-02-05','Viên nén','viên','0.5mg','Mekophar','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727049/Dexamethasone_imzdmn.jpg'),(12,9,'Mebendazole','Thuoc tay giun dinh ky cho nguoi lon va tre em',55000.00,90,20,'2024-11-20','2027-11-20','Viên nén','viên','500mg','Mebiphar','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727101/Mebendazole_qr5iyw.jpg'),(13,4,'Smecta','Thuoc dieu tri tieu chay va dau thuc quan, da day',60000.00,45,20,'2025-01-25','2028-01-25','Gói bột','gói','3g','Ipsen','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727107/Smecta_pxtqnu.jpg'),(14,10,'Rodogyl','Khang sinh dac tri nhiem trung rang mieng, viem loi',70000.00,70,20,'2025-03-10','2028-03-10','Viên nén','viên','Spiramycin + Metronidazole','Sanofi','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727161/Rodogyl_yzm4vf.jpg'),(15,10,'Franrogyl','Dieu tri sau rang, viem chan rang va phu ne',10000.00,120,20,'2025-02-28','2028-02-28','Viên nén','viên','Spiramycin + Metronidazole','OPV','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727167/Franrogyl_zztcjg.jpg');
/*!40000 ALTER TABLE `drug` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_record`
--

DROP TABLE IF EXISTS `medical_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_record` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `diagnosis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `treatment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `appointment_id` int DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `uq_medical_record_appointment` (`appointment_id`),
  KEY `idx_medical_record_patient_id` (`patient_id`),
  KEY `idx_medical_record_doctor_id` (`doctor_id`),
  CONSTRAINT `fk_medical_record_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`),
  CONSTRAINT `fk_medical_record_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`),
  CONSTRAINT `fk_medical_record_patient` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_record`
--

LOCK TABLES `medical_record` WRITE;
/*!40000 ALTER TABLE `medical_record` DISABLE KEYS */;
INSERT INTO `medical_record` VALUES (1,1,1,'Nghi viem hong','Da tung cam cum','2026-04-10 09:30:00',NULL),(2,1,2,'Di ung da nhe','Da tung viem da co dia','2026-04-10 11:00:00',NULL),(3,3,2,'Viem da tiep xuc','Boi thuoc mo, tranh hoa chat','2026-04-10 12:30:00',NULL),(4,5,2,'Thuy dau','Cach ly, boi ho nuoc, ha sot','2026-04-10 14:00:00',NULL),(5,7,3,'Sau rang so 36','Han rang tham my','2026-04-10 15:30:00',NULL),(6,1,1,'Roi loan nhip tim nhe','Nghi ngoi, theo doi them','2026-04-10 17:00:00',NULL),(7,1,1,'Viêm họng nhẹ, có ho','Uống thuốc theo chỉ định, nghỉ ngơi và tái khám nếu sốt','2026-05-30 12:19:16',NULL),(8,1,1,'Rối loạn nhịp tim nhẹ','Uống thuốc theo chỉ định, nghỉ ngơi và theo dõi thêm','2026-05-30 13:37:02',15),(9,1,1,'Thiếu máu cơ tim nhẹ','Điều chỉnh chế độ ăn, dùng thuốc theo chỉ định','2026-05-30 16:25:12',11),(10,1,1,'Tăng huyết áp giai đoạn 1','Theo dõi huyết áp hằng ngày, giảm muối, tập thể dục, dùng thuốc hạ áp theo chỉ định','2026-05-30 17:02:27',10),(11,1,1,'tăng huyết áp loại 1','nghỉ ngơi','2026-06-06 08:49:15',20),(13,7,3,'Răng sâu','Trám răng và uống thuốc theo chỉ định.','2026-07-29 22:29:04',53),(14,7,3,'Viêm họng nhẹ','Uống thuốc theo hướng dẫn và nghỉ ngơi','2026-07-30 21:37:55',57),(15,7,3,'Cảm cúm','Nghỉ ngơi, uống nhiều nước và theo dõi sức khỏe','2026-07-30 21:37:55',58),(16,7,3,'Đau đầu, mệt mỏi','Nghỉ ngơi','2026-07-30 21:37:55',59),(17,7,3,'Đau dạ dày','Ăn uống đúng giờ và sử dụng thuốc theo chỉ định','2026-07-30 21:37:55',60),(18,7,3,'Aaaa','Bbbbbb','2026-07-30 21:46:25',54),(19,7,3,'Viêm mũi dị ứng','Uống thuốc theo chỉ định.','2026-07-31 13:00:56',61),(20,7,3,'Đau lưng','Nghỉ ngơi, hạn chế vận động mạnh và theo dõi triệu chứng','2026-07-31 13:00:56',62),(21,7,3,'Chẩn đoán Selenium TC-MEDICAL-007','Điều trị Selenium TC-MEDICAL-007','2026-07-31 16:44:28',63),(22,7,3,'Đau lưng do ngồi lâu','Nghỉ ngơi và hạn chế vận động mạnh','2026-07-31 17:21:13',64),(23,7,3,'Chẩn đoán cập nhật TC-MEDICAL-006 1785777504','Hướng điều trị cập nhật TC-MEDICAL-006 1785777504','2026-07-31 17:29:09',65),(24,7,3,'Chẩn đoán ban đầu TC-MEDICAL-009','Hướng điều trị ban đầu TC-MEDICAL-009','2026-07-31 22:39:40',66),(25,7,3,'Đau đầu nhẹ do thiếu ngủ','Nghỉ ngơi và uống đủ nước','2026-07-31 23:02:31',67),(26,7,3,'Chẩn đoán TC-MEDICAL-004','Hướng điều trị TC-MEDICAL-004','2026-07-31 23:25:41',70),(27,7,3,'Chẩn đoán TC-MEDICAL-008','Hướng điều trị TC-MEDICAL-008','2026-07-31 23:29:52',71),(28,7,3,'Đau đầu nhẹ do thiếu ngủ','Nghỉ ngơi và uống đủ nước','2026-08-01 14:57:41',72),(29,7,3,'Đau cổ do ngồi sai tư thế','Nghỉ ngơi và tập vận động nhẹ','2026-08-01 22:16:44',86),(30,7,3,'Đau cổ do ngồi sai tư thế','Nghỉ ngơi và tập vận động nhẹ','2026-08-02 14:03:43',92),(31,7,3,'Đau đầu nhẹ do thiếu ngủ','Nghỉ ngơi và uống đủ nước','2026-08-02 14:11:55',94),(32,7,3,'Đau đầu nhẹ do thiếu ngủ','Nghỉ ngơi và uống đủ nước','2026-08-04 00:19:05',99),(33,7,3,'Đau cổ do ngồi sai tư thế','Nghỉ ngơi và tập vận động nhẹ','2026-08-04 00:25:50',102);
/*!40000 ALTER TABLE `medical_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_record_service`
--

DROP TABLE IF EXISTS `medical_record_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_record_service` (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_id` int NOT NULL,
  `service_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `unit_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_medical_record_service_record_id` (`record_id`),
  KEY `idx_medical_record_service_service_id` (`service_id`),
  CONSTRAINT `fk_medical_record_service_record` FOREIGN KEY (`record_id`) REFERENCES `medical_record` (`record_id`),
  CONSTRAINT `fk_medical_record_service_service` FOREIGN KEY (`service_id`) REFERENCES `medical_service` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_record_service`
--

LOCK TABLES `medical_record_service` WRITE;
/*!40000 ALTER TABLE `medical_record_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `medical_record_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_service`
--

DROP TABLE IF EXISTS `medical_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_service` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `specialty_id` int NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `unit_price` decimal(10,2) NOT NULL,
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  PRIMARY KEY (`service_id`),
  KEY `idx_medical_service_specialty_id` (`specialty_id`),
  CONSTRAINT `fk_medical_service_specialty` FOREIGN KEY (`specialty_id`) REFERENCES `specialty` (`specialty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_service`
--

LOCK TABLES `medical_service` WRITE;
/*!40000 ALTER TABLE `medical_service` DISABLE KEYS */;
INSERT INTO `medical_service` VALUES (1,'Điện tâm đồ ECG',1,'Đo hoạt động điện của tim để hỗ trợ chẩn đoán bệnh tim mạch.',120000.00,'active'),(2,'Siêu âm tim',1,'Kiểm tra cấu trúc và chức năng hoạt động của tim.',250000.00,'active'),(3,'Soi da',2,'Kiểm tra tình trạng da để hỗ trợ chẩn đoán bệnh da liễu.',90000.00,'active'),(4,'Test dị ứng',2,'Kiểm tra phản ứng dị ứng của bệnh nhân.',100000.00,'active'),(5,'Nhổ răng',5,'Thực hiện nhổ răng theo chỉ định của bác sĩ.',200000.00,'active'),(6,'Trám răng',5,'Điều trị sâu răng bằng phương pháp trám răng.',180000.00,'active'),(7,'Cạo vôi răng',5,'Làm sạch vôi răng và mảng bám.',150000.00,'active'),(8,'Chụp X-quang răng',5,'Chụp X-quang hỗ trợ chẩn đoán các bệnh lý răng miệng.',150000.00,'active'),(9,'Đo thị lực',7,'Kiểm tra khả năng nhìn và xác định mức độ cận, viễn hoặc loạn thị.',70000.00,'active'),(10,'Xét nghiệm máu',10,'Phân tích mẫu máu để hỗ trợ chẩn đoán bệnh.',80000.00,'active');
/*!40000 ALTER TABLE `medical_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT '0',
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`),
  KEY `idx_notification_user_id` (`user_id`),
  CONSTRAINT `fk_notification_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,1,'Ban co lich hen vao 09:00 ngay 10/04/2026',0,'2026-04-09 18:00:00'),(2,3,'Ban co lich hen vao 10:30 ngay 10/04/2026',0,'2026-04-09 18:05:00'),(3,2,'Ban co lich kham voi benh nhan Nguyen An',1,'2026-04-09 18:10:00'),(4,4,'Ban co lich kham voi benh nhan Le Chi',0,'2026-04-09 18:15:00'),(5,1,'Ban co ket qua xet nghiem moi',1,'2026-04-10 08:00:00'),(6,2,'Ban da duoc phan cong lich kham moi',0,'2026-04-10 08:10:00'),(7,3,'Ban co lich hen vao 13:00 ngay 10/04/2026',0,'2026-04-10 08:20:00'),(8,4,'Don thuoc cua ban da duoc cap nhat',1,'2026-04-10 08:30:00'),(9,1,'Ban co lich hen vao 14:00 ngay 10/04/2026',0,'2026-04-10 08:40:00'),(10,2,'Ho so benh an da duoc cap nhat',1,'2026-04-10 08:50:00'),(11,7,'Lich hen cua ban da duoc xac nhan',0,'2026-06-03 18:07:08'),(12,1,'Lich hen #19 voi bac si Pham Dung vao 15:00 07/06/2026 da duoc xac nhan',0,'2026-06-03 18:51:00'),(13,1,'Ban co don thuoc moi',0,'2026-06-03 22:52:07'),(14,1,'Ban co don thuoc moi #12 trong ho so kham benh #10',0,'2026-06-03 23:00:36'),(15,1,'Lich hen #20 voi bac si Tran Binh vao 10:00 08/06/2026 da duoc xac nhan',0,'2026-06-06 08:48:32'),(16,1,'Ban co don thuoc moi #13 trong ho so kham benh #11',0,'2026-06-06 08:50:19'),(17,14,'Lich hen #46 voi bac si Ly Minh vao 10:00 31/07/2026 da duoc xac nhan',0,'2026-07-29 21:14:39'),(18,14,'Lich hen #63 voi bac si Ly Minh vao 07:00 01/08/2026 da duoc xac nhan',0,'2026-07-31 16:44:28'),(19,14,'Lich hen #64 voi bac si Ly Minh vao 07:30 01/08/2026 da duoc xac nhan',0,'2026-07-31 17:21:13'),(20,14,'Lich hen #65 voi bac si Ly Minh vao 08:00 01/08/2026 da duoc xac nhan',0,'2026-07-31 17:29:09'),(21,14,'Lich hen #66 voi bac si Ly Minh vao 08:30 01/08/2026 da duoc xac nhan',0,'2026-07-31 22:39:40'),(22,14,'Lich hen #67 voi bac si Ly Minh vao 09:30 01/08/2026 da duoc xac nhan',0,'2026-07-31 22:58:00'),(23,14,'Lich hen #68 voi bac si Ly Minh vao 10:30 01/08/2026 da duoc xac nhan',0,'2026-07-31 23:12:20'),(24,14,'Lich hen #69 voi bac si Ly Minh vao 11:00 01/08/2026 da duoc xac nhan',0,'2026-07-31 23:18:38'),(25,14,'Lich hen #70 voi bac si Ly Minh vao 13:00 01/08/2026 da duoc xac nhan',0,'2026-07-31 23:25:41'),(26,14,'Lich hen #71 voi bac si Ly Minh vao 13:30 01/08/2026 da duoc xac nhan',0,'2026-07-31 23:29:52'),(27,14,'Lich hen #72 voi bac si Ly Minh vao 07:00 02/08/2026 da duoc xac nhan',0,'2026-08-01 14:57:31'),(28,14,'Lich hen #74 voi bac si Ly Minh vao 08:00 02/08/2026 da duoc xac nhan',0,'2026-08-01 15:40:27'),(29,14,'Lich hen #75 voi bac si Ly Minh vao 08:30 02/08/2026 da duoc xac nhan',0,'2026-08-01 15:41:06'),(30,14,'Lich hen #76 voi bac si Ly Minh vao 09:30 02/08/2026 da duoc xac nhan',0,'2026-08-01 15:41:38'),(31,14,'Lich hen #77 voi bac si Ly Minh vao 10:00 02/08/2026 da duoc xac nhan',0,'2026-08-01 15:49:05'),(32,14,'Lich hen #78 voi bac si Ly Minh vao 07:30 02/08/2026 da duoc xac nhan',0,'2026-08-01 15:51:47'),(33,14,'Lich hen #81 voi bac si Ly Minh vao 07:30 02/08/2026 da duoc xac nhan',0,'2026-08-01 15:59:07'),(34,14,'Lich hen #83 voi bac si Ly Minh vao 08:00 02/08/2026 da duoc xac nhan',0,'2026-08-01 20:55:24'),(35,14,'Lich hen #84 voi bac si Ly Minh vao 08:30 02/08/2026 da duoc xac nhan',0,'2026-08-01 21:04:32'),(36,14,'Lich hen #86 voi bac si Ly Minh vao 09:30 02/08/2026 da duoc xac nhan',0,'2026-08-01 22:16:35'),(37,14,'Lich hen #90 voi bac si Ly Minh vao 07:00 03/08/2026 da duoc xac nhan',0,'2026-08-02 14:01:31'),(38,14,'Lich hen #92 voi bac si Ly Minh vao 07:30 03/08/2026 da duoc xac nhan',0,'2026-08-02 14:03:33'),(39,14,'Lich hen #94 voi bac si Ly Minh vao 08:00 03/08/2026 da duoc xac nhan',0,'2026-08-02 14:11:45'),(40,14,'Lich hen #99 voi bac si Ly Minh vao 07:00 05/08/2026 da duoc xac nhan',0,'2026-08-04 00:18:55'),(41,14,'Lich hen #100 voi bac si Ly Minh vao 07:30 05/08/2026 da duoc xac nhan',0,'2026-08-04 00:23:39'),(42,14,'Lich hen #102 voi bac si Ly Minh vao 08:00 05/08/2026 da duoc xac nhan',0,'2026-08-04 00:25:40');
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `uk_patient_user_id` (`user_id`),
  CONSTRAINT `fk_patient_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,1,'Nguyen An','2002-05-10','Nam','Da Nang','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724408/image11_haldjd.jpg'),(2,3,'Le Chi','2015-08-12','Nu','Quang Nam','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722654/image_4_zo9nhr.png'),(3,7,'Dang Thu','2006-09-15','Nu','Ha Noi','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723040/Lighthearted_z1fwdi.jpg'),(4,9,'Bui Nam','1985-03-20','Nam','Thanh pho Ho Chi Minh','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724409/image12_ocjsfs.jpg'),(5,11,'Do Hung','1970-11-05','Nam','Dong Nai','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724411/image9_yjzrqb.jpg'),(6,13,'Nguyen Thi Tuyet Trinh','2005-04-25','Nu','Can Tho','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722814/image1_zbpauf.png'),(7,14,'Duong Le Kim Phung','2005-02-17','Nu','Soc Trang','https://res.cloudinary.com/dnxp96rpm/image/upload/v1785336612/939391b78f380e665729_1_wlz6o6.jpg'),(8,15,'Tran Anh Tuan','1958-09-23','Nam','Can Tho','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723319/image5_bptquf.jpg'),(9,41,'Nguyễn Nhi','2000-02-02','Nu','Lê Văn Lương',NULL);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `appointment_id` int NOT NULL,
  `amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `payment_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`),
  KEY `idx_payment_patient_id` (`patient_id`),
  KEY `idx_payment_appointment_id` (`appointment_id`),
  CONSTRAINT `fk_payment_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`),
  CONSTRAINT `fk_payment_patient` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,1,1,150000.00,'cash','paid','2026-04-10 10:05:00'),(2,2,2,200000.00,'banking','pending','2026-04-10 11:35:00'),(3,3,3,180000.00,'cash','paid','2026-04-10 12:10:00'),(4,4,4,220000.00,'banking','paid','2026-04-10 13:20:00'),(5,5,5,50000.00,'cash','pending','2026-04-10 14:00:00'),(6,6,6,160000.00,'banking','paid','2026-04-10 15:10:00'),(7,7,7,70000.00,'cash','paid','2026-04-10 16:00:00'),(8,8,8,90000.00,'banking','pending','2026-04-10 17:30:00'),(9,2,9,120000.00,'cash','paid','2026-04-10 18:45:00'),(10,1,10,140000.00,'banking','pending','2026-04-10 19:20:00');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription`
--

DROP TABLE IF EXISTS `prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription` (
  `prescription_id` int NOT NULL AUTO_INCREMENT,
  `record_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prescription_id`),
  KEY `idx_prescription_record_id` (`record_id`),
  KEY `idx_prescription_patient_id` (`patient_id`),
  KEY `idx_prescription_doctor_id` (`doctor_id`),
  CONSTRAINT `fk_prescription_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`),
  CONSTRAINT `fk_prescription_patient` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`),
  CONSTRAINT `fk_prescription_record` FOREIGN KEY (`record_id`) REFERENCES `medical_record` (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription`
--

LOCK TABLES `prescription` WRITE;
/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
INSERT INTO `prescription` VALUES (1,1,1,1,'2026-04-10 10:00:00'),(2,2,1,2,'2026-04-10 11:30:00'),(3,3,3,2,'2026-04-10 13:00:00'),(4,4,5,2,'2026-04-10 14:30:00'),(5,5,7,3,'2026-04-10 16:00:00'),(6,6,1,1,'2026-04-10 17:30:00'),(7,6,1,1,'2026-04-10 17:35:00'),(8,2,1,2,'2026-04-10 11:35:00'),(9,4,5,2,'2026-04-10 14:35:00'),(10,3,3,2,'2026-04-10 13:05:00'),(11,10,1,1,'2026-06-03 22:52:07'),(12,10,1,1,'2026-06-03 23:00:36'),(13,11,1,1,'2026-06-06 08:50:19');
/*!40000 ALTER TABLE `prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription_detail`
--

DROP TABLE IF EXISTS `prescription_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `prescription_id` int NOT NULL,
  `drug_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `dosage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_prescription_detail_prescription_id` (`prescription_id`),
  KEY `idx_prescription_detail_drug_id` (`drug_id`),
  CONSTRAINT `fk_prescription_detail_drug` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`drug_id`),
  CONSTRAINT `fk_prescription_detail_prescription` FOREIGN KEY (`prescription_id`) REFERENCES `prescription` (`prescription_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription_detail`
--

LOCK TABLES `prescription_detail` WRITE;
/*!40000 ALTER TABLE `prescription_detail` DISABLE KEYS */;
INSERT INTO `prescription_detail` VALUES (1,1,1,10,'Ngay 2 lan, moi lan 1 vien'),(2,2,2,5,'Ngay 1 lan, moi lan 1 vien'),(3,3,3,7,'Ngay 1 lan buoi toi, moi lan 1 vien'),(4,4,4,8,'Ngay 2 lan, moi lan 1 vien'),(5,5,5,6,'Ngay 1 lan, moi lan 1 vien'),(6,6,6,10,'Ngay 2 lan, moi lan 1 vien'),(7,7,7,4,'Ngay 1 lan buoi sang, moi lan 1 vien'),(8,8,8,12,'Ngay 3 lan, moi lan 1 vien'),(9,9,9,5,'Ngay 1 lan, moi lan 1 vien'),(10,10,10,3,'Ngay 1 lan buoi toi, moi lan 1 vien'),(11,11,1,1,'Uống 1 viên sau khi ăn'),(12,12,2,1,'Uống 1 viên sau khi ăn'),(13,13,4,1,'ngày');
/*!40000 ALTER TABLE `prescription_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specialty`
--

DROP TABLE IF EXISTS `specialty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `specialty` (
  `specialty_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`specialty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specialty`
--

LOCK TABLES `specialty` WRITE;
/*!40000 ALTER TABLE `specialty` DISABLE KEYS */;
INSERT INTO `specialty` VALUES (1,'Tim mach','Chuyên khoa chẩn đoán và điều trị các bệnh lý về hệ tuần hoàn, tim và mạch máu.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724816/timmach_wqaxmh.jpg'),(2,'Da lieu','Chăm sóc và điều trị các vấn đề về da, tóc, móng.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724839/khoadalieu_hipale.jpg'),(3,'Nhi khoa','Chăm sóc sức khỏe toàn diện và điều trị bệnh lý cho trẻ em từ sơ sinh đến tuổi vị thành niên.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724878/nhikhoa_jcnoao.jpg'),(4,'Khoa kham benh','Tiếp nhận, phân loại và thực hiện khám lâm sàng ban đầu cho mọi đối tượng bệnh nhân.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724972/khoakhambenh_ucexbz.jpg'),(5,'Rang ham mat','Khám và điều trị các bệnh lý về răng miệng, phục hình thẩm mỹ và phẫu thuật hàm mặt.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724971/ranghammat_jvwq9w.jpg'),(6,'San phu khoa','Chăm sóc sức khỏe phụ nữ, quản lý thai kỳ, sinh con và các bệnh lý phụ khoa.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775725122/sanphukhoa_cdzidj.jpg'),(7,'Mat','Chẩn đoán, điều trị các bệnh lý về mắt và thực hiện các thủ thuật đo thị lực, nhãn khoa.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775725131/khoamat_lnzmi9.jpg'),(8,'Tai mui hong','Điều trị chuyên sâu các bệnh về tai, mũi, xoang, họng và các cấu trúc vùng đầu cổ.','https://res.cloudinary.com/dczz59gpu/image/upload/v1775725184/khoataimuihong_gzaggj.jpg'),(9,'Y Học Cổ Truyền','Khám, điều trị và phục hồi sức khỏe bằng các phương pháp kết hợp Đông - Tây y như châm cứu, bấm huyệt, vật lý trị liệu cho các bệnh lý xương khớp, thần kinh.','https://res.cloudinary.com/dczz59gpu/image/upload/v1779612733/CheTrung_khanh-thanh-khu-chuyen-gia-10_rdfpsu.jpg'),(10,'Xét Nghiệm','Thực hiện các kỹ thuật cận lâm sàng tiên tiến như chụp X-quang, cắt lớp vi tính (CT), cộng hưởng từ (MRI), siêu âm và xét nghiệm máu để hỗ trợ chẩn đoán bệnh chính xác.','https://res.cloudinary.com/dczz59gpu/image/upload/v1779612880/co-so-vat-chat-tam-anh_ah9h5j.jpg');
/*!40000 ALTER TABLE `specialty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_result`
--

DROP TABLE IF EXISTS `test_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_result` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `record_id` int NOT NULL,
  `test_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`test_id`),
  KEY `idx_test_result_record_id` (`record_id`),
  CONSTRAINT `fk_test_result_record` FOREIGN KEY (`record_id`) REFERENCES `medical_record` (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_result`
--

LOCK TABLES `test_result` WRITE;
/*!40000 ALTER TABLE `test_result` DISABLE KEYS */;
INSERT INTO `test_result` VALUES (1,1,'Xet nghiem mau','Binh thuong','2026-04-10 09:45:00'),(2,2,'Test di ung','Di ung nhe voi thoi tiet','2026-04-10 11:15:00'),(3,3,'Soi da','Viem nhiem do vi khuan','2026-04-10 12:45:00'),(4,4,'Xet nghiem dich not phong','Duong tinh voi Varicella Zoster','2026-04-10 14:15:00'),(5,5,'Chup x-quang rang','Sau men rang dien rong','2026-04-10 15:45:00'),(6,6,'Diem tam do (ECG)','Nhip xoang hoi nhanh','2026-04-10 17:15:00'),(7,9,'Điện tâm đồ ECR','Thiếu máu cơ tim','2026-06-05 22:17:42');
/*!40000 ALTER TABLE `test_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('patient','doctor','staff','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Nguyen','An','an@gmail.com','901000001','patient_an','Abc@123','patient','2026-04-09 08:00:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724408/image11_haldjd.jpg'),(2,'Tran','Binh','binh@gmail.com','901000002','doctor_binh','Abc@123','doctor','2026-04-09 08:10:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723515/image6_mr167k.png'),(3,'Le','Chi','chi@gmail.com','901000003','patient_chi','Abc@123','patient','2026-04-09 08:20:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722654/image_4_zo9nhr.png'),(4,'Pham','Dung','dung@gmail.com','901000004','doctor_dung','Abc@123','doctor','2026-04-09 08:30:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723653/image7_j0izpd.png'),(5,'Vo','Ha','ha@gmail.com','901000005','staff_ha','Abc@123','staff','2026-04-09 08:40:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723238/imgae3_eumfhj.jpg'),(6,'Admin','System','admin@gmail.com','901000006','admin_system','Abc@123','admin','2026-04-09 08:50:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723803/images_knk042.png'),(7,'Dang','Thu','thu@gmail.com','901000007','patient_thu','Abc@123','patient','2026-04-09 08:55:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723040/Lighthearted_z1fwdi.jpg'),(8,'Ly','Minh','minh@gmail.com','901000008','doctor_minh','Abc@123','doctor','2026-04-09 09:00:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724405/image14_jab5qp.png'),(9,'Bui','Nam','nam@gmail.com','901000009','patient_nam','Abc@123','patient','2026-04-09 09:05:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724409/image12_ocjsfs.jpg'),(10,'Vu','Thinh','thinh@gmail.com','901000010','doctor_thinh','Abc@123','doctor','2026-04-09 09:10:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724612/image15_vdmxlr.png'),(11,'Do','Hung','hung@gmail.com','901000011','patient_hung','Abc@123','patient','2026-04-09 09:15:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724411/image9_yjzrqb.jpg'),(12,'Diep','Chi','chi@gmail.com','901000012','staff_chi','Abc@123','staff','2026-04-09 09:20:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723244/image4_uzb2oq.jpg'),(13,'Nguyen Thi','Tuyet Trinh','tuyettrinhnguyenthi25042005@gmail.com','901000013','patient_trinh','Abc@123','patient','2026-04-09 09:25:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722814/image1_zbpauf.png'),(14,'Duong Le','Kim Phung','kimphungduongle9@gmail.com','901000014','patient_phung','Abc@123','patient','2026-04-09 09:30:00','https://res.cloudinary.com/dnxp96rpm/image/upload/v1785336612/939391b78f380e665729_1_wlz6o6.jpg'),(15,'Tran','Anh Tuan','trananhtuan23092005@gmail.com','901000015','patient_tuan','Abc@123','patient','2026-04-09 09:35:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723319/image5_bptquf.jpg'),(33,'Duong','Phung','phungtest1466@gmail.com','0901234567','phung_auto_4711','$2a$10$L1/diFlNSuUTeYauG4fU0O.NoMsu5CXg0jP3O3WVvuN9O8u7HHMhK','patient','2026-07-16 19:36:33','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784205397/gd2zzai3p5fqeul25p6g.png'),(34,'Duong','Phung','phungtest2322@gmail.com','0901234567','phung_auto_2613','$2a$10$4zcGElpqofVI3Wjcgl9UFeoVqlHTrL6CVIfn0WCyqypCFBUt8JEOO','patient','2026-07-18 19:36:26','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784378189/kwvipbjvzezmctgi4ro2.png'),(35,'Phụng','Kim','api_register01@gmail.com','0912345601','api_register01','$2a$10$6kstOxBWS25oHylOmyeuyewC5q78UuSwzafZnaobg6UXHIJPOwJuq','patient','2026-07-24 20:06:42','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784898405/f6lqlilookzvv8bp1jzn.png'),(36,'Phụng','Kim','phung_test@gmail.com','0912345601','','$2a$10$p5wAsFdZcDCe8pz1p5nz6OrnR7qyXJ3i3EeQDHXBW5MM1bge3lK1K','patient','2026-07-24 20:29:01','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784899788/cuyrsji4feg9xxolqtr9.png'),(37,'Phụng','Kim','','0912345601','patient_phungg','$2a$10$YkOUyY9NkN.uEy75YdSOBOaHHicKRvVCe.GVIrtfYtthw7PMoe7eO','patient','2026-07-24 21:13:58','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784902440/rljvywj84nq3eiznd1jm.png'),(38,'Phụng','Kim','kimphung@gmail.com','0912345601','patient_phungggggg','$2a$10$/oaLM0TTxIiAOKkx7T30u.Js1sxjOL0pEriNvflSt5To0OL0GMu6m','patient','2026-07-24 21:23:48','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784903031/kae6tsfsgahr4xtbqd2v.png'),(39,'Phụng','Kim','kimphunggg@gmail.com','0912345601','patient_phungtest','$2a$10$SonGeN/XE5CekLJ0ilPVgeHZTrZmDY7mYWXxUYNXTPCtG7bGFz9zi','patient','2026-07-24 21:34:22',NULL),(40,'Phụng','Kim','kim@gmail.com','09123abc','patient_ph','$2a$10$6UNAna4Rn11/t5bQiedHqu3Z7EKYgQLm9v5BIOYSPTtizB8UgZaHy','patient','2026-07-24 21:42:15','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784904138/q3nfkgwtosc72at2yjkd.png'),(41,'Nguyễn','Nhi','my123@gmail','0123456782','phu','$2a$10$sPgdqaydry2yc/9dahMUXOD0Zzb.jEyTsS7rGTZzMykviXp3KezQK','patient','2026-07-24 21:51:48',NULL),(42,'Phụng','Kim','phungtest@gmail.com','0912345678','patient_pphutest','$2a$10$/22z/ecZYm6WLR9pwGSiQuLNOwjOAF0sKHj3PWNausfoljay1AKdu','patient','2026-07-24 22:03:07','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784905390/fpdjuuxoziv6jdm2osvo.png'),(43,'Phụng','Kim','phungtestgmail.com','0912345678','patient_pphutestp','$2a$10$CYFb79dSwca0KfoAPoQCzeCnI2GcPhJBSA/USoX0R1M.LvNPQY0UO','patient','2026-07-24 22:09:26','https://res.cloudinary.com/dxxwcby8l/image/upload/v1784905768/fmoln08d5was8w9lbo7s.png'),(44,'Duong','Phung','phungtest5226@gmail.com','0901234567','phung_auto_7126','$2a$10$topwZeuN3J473zyB8Wtc2Oq32xdeMZAI.tKyu5olBVX58MBBeUkKO','patient','2026-08-04 00:09:32','https://res.cloudinary.com/dxxwcby8l/image/upload/v1785776975/ixsnuki32tyegebydfey.png');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-05 21:50:33
