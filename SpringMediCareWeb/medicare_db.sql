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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,1,1,'2026-04-10 09:00:00','confirmed','Mệt khi vận động, khó thở nhẹ.','2026-04-09 09:00:00'),(2,2,2,'2026-04-10 10:30:00','pending','Kham da lieu','2026-04-09 09:15:00'),(3,3,2,'2026-04-10 12:00:00','confirmed','Kham benh ngoai da','2026-04-09 09:30:00'),(4,4,3,'2026-04-10 13:30:00','pending','Kham rang','2026-04-09 09:45:00'),(5,5,2,'2026-04-10 15:00:00','confirmed','Kham noi mut mong nuoc','2026-04-09 10:00:00'),(6,6,4,'2026-04-10 16:30:00','pending','Kham mat','2026-04-09 10:15:00'),(7,7,3,'2026-04-10 18:00:00','confirmed','KIem tra sau rang','2026-04-09 10:30:00'),(8,8,4,'2026-04-10 19:30:00','cancelled','Do do can va kham mat','2026-04-09 10:45:00'),(9,2,2,'2026-04-10 13:00:00','confirmed','Lich hen bo sung tu thong bao NC7','2026-04-10 08:20:00'),(10,1,1,'2026-04-10 14:00:00','completed','Hồi hộp, đau tức ngực nhẹ.','2026-04-10 08:40:00'),(11,1,1,'2026-04-11 08:00:00','completed','Đau ngực khi gắng sức, khó thở.','2026-05-29 14:53:58'),(12,1,1,'2026-04-11 09:00:00','cancelled','Đau tức ngực thoáng qua, mệt mỏi.','2026-05-29 15:01:03'),(13,1,1,'2026-04-11 10:00:00','pending','Mệt khi vận động nhiều.','2026-05-29 16:02:27'),(14,1,1,'2026-04-11 10:30:00','pending','Tim đập mạnh, lo lắng, mất ngủ.','2026-05-29 16:21:51'),(15,1,1,'2026-04-12 09:10:00','pending','Hay tức ngực khó chịu','2026-05-29 16:48:12'),(16,3,4,'2026-04-11 10:00:00','pending','Đỏ mắt, chảy nước mắt, ngứa, có ghèn','2026-05-30 19:39:12'),(17,3,2,'2026-04-11 10:00:00','confirmed','Ngứa, nổi mẩn đỏ','2026-05-30 19:40:34'),(18,3,2,'2026-06-07 14:00:00','pending','Mụn đầu đen, Mụn viêm, Da nhờn','2026-06-03 18:37:19'),(19,1,2,'2026-06-07 15:00:00','confirmed','Ngứa, Nổi mẩn đỏ, Khô da','2026-06-03 18:45:43');
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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_schedule`
--

LOCK TABLES `doctor_schedule` WRITE;
/*!40000 ALTER TABLE `doctor_schedule` DISABLE KEYS */;
INSERT INTO `doctor_schedule` VALUES (1,1,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(2,1,'2026-04-11','afternoon','13:00:00','17:00:00','available','Ca chiều'),(3,1,'2026-04-11','evening','17:30:00','21:00:00','available','Ca tối'),(4,2,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(5,2,'2026-04-11','afternoon','13:00:00','17:00:00','available','Ca chiều'),(6,2,'2026-04-11','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(7,3,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(8,3,'2026-04-11','afternoon','13:00:00','17:00:00','available','Ca chiều'),(9,3,'2026-04-11','evening','17:30:00','21:00:00','available','Ca tối'),(10,4,'2026-04-11','morning','07:00:00','11:30:00','available','Ca sáng'),(11,4,'2026-04-11','afternoon','13:00:00','17:00:00','unavailable','Bác sĩ nghỉ ca chiều'),(12,4,'2026-04-11','evening','17:30:00','21:00:00','available','Ca tối'),(13,1,'2026-04-12','morning','07:00:00','11:30:00','available','Ca sáng'),(14,1,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(15,1,'2026-04-12','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(16,2,'2026-04-12','morning','07:00:00','11:30:00','available','Ca sáng'),(17,2,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(18,2,'2026-04-12','evening','17:30:00','21:00:00','available','Ca tối'),(19,3,'2026-04-12','morning','07:00:00','11:30:00','unavailable','Bác sĩ nghỉ ca sáng'),(20,3,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(21,3,'2026-04-12','evening','17:30:00','21:00:00','available','Ca tối'),(22,4,'2026-04-12','morning','07:00:00','11:30:00','available','Ca sáng'),(23,4,'2026-04-12','afternoon','13:00:00','17:00:00','available','Ca chiều'),(24,4,'2026-04-12','evening','17:30:00','21:00:00','available','Ca tối'),(25,1,'2026-06-07','morning','07:00:00','11:30:00','available','Ca sáng'),(26,1,'2026-06-07','afternoon','13:00:00','17:00:00','available','Ca chiều'),(27,1,'2026-06-07','evening','17:30:00','21:00:00','available','Ca tối'),(28,2,'2026-06-07','morning','07:00:00','11:30:00','available','Ca sáng'),(29,2,'2026-06-07','afternoon','13:00:00','17:00:00','available','Ca chiều'),(30,2,'2026-06-07','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(31,1,'2026-06-08','morning','07:00:00','11:30:00','available','Ca sáng'),(32,1,'2026-06-08','afternoon','13:00:00','17:00:00','available','Ca chiều'),(33,1,'2026-06-08','evening','17:30:00','21:00:00','unavailable','Bác sĩ không trực ca tối'),(34,2,'2026-06-08','morning','07:00:00','11:30:00','available','Ca sáng'),(35,2,'2026-06-08','afternoon','13:00:00','17:00:00','available','Ca chiều'),(36,2,'2026-06-08','evening','17:30:00','21:00:00','available','Ca tối'),(37,1,'2026-06-09','morning','07:00:00','11:30:00','available','Ca sáng'),(38,1,'2026-06-09','afternoon','13:00:00','17:00:00','available','Ca chiều'),(39,2,'2026-06-09','morning','07:00:00','11:30:00','available','Ca sáng'),(40,2,'2026-06-09','afternoon','13:00:00','17:00:00','available','Ca chiều');
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
INSERT INTO `drug` VALUES (1,1,'Paracetamol','Giam dau ha sot',5000.00,100,20,'2025-01-01','2027-12-31','Viên nén','viên','500mg','DHG Pharma','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726283/Paracetamol_ewnf42.jpg'),(2,2,'Vitamin C','Tang suc de khang',3000.00,200,20,'2024-10-15','2027-10-15','Viên nén','viên','500mg','Domesco','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726425/Vitamin_C_vmc8io.png'),(3,3,'Cetirizine','Thuoc chong di ung',7000.00,150,20,'2024-08-20','2027-08-20','Viên nén','viên','10mg','Stada','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726456/Cetirizine_nlrkhh.jpg'),(4,1,'Panadol Extra','Giam dau nhanh, ha sot, co cafein giup tinh tao',6000.00,300,20,'2025-02-10','2028-02-10','Viên nén','viên','500mg + 65mg','GSK','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726587/PanadolExtra_en6wuf.jpg'),(5,4,'Gaviscon','Dieu tri trao nguoc da day va o chua',2000.00,120,20,'2025-03-01','2028-03-01','Gói hỗn dịch','gói','10ml','Reckitt','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726805/Gaviscon_evnufe.jpg'),(6,5,'Augmentin','Khang sinh dieu tri nhiem khuan duong ho hap',50000.00,150,20,'2025-01-15','2027-01-15','Viên nén','viên','625mg','GSK','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726846/Augmentin_c2k4mg.jpg'),(7,6,'Amlodipine','Dieu tri cao huyet ap va dau that nguc',40000.00,50,20,'2024-12-01','2027-12-01','Viên nén','viên','5mg','Stella','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726876/Amlodipine_qr9yot.jpg'),(8,7,'Salbutamol','Thuoc xit gian phe quan, dieu tri hen suyen',100000.00,60,20,'2025-02-20','2027-02-20','Bình xịt','bình','100mcg/liều','GSK','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726914/Salbutamol_hlfvob.jpg'),(9,1,'Efferalgan','Giam dau, ha sot dang sui bot',50000.00,15,20,'2025-01-10','2028-01-10','Viên sủi','viên','500mg','UPSA','low_stock','https://res.cloudinary.com/dczz59gpu/image/upload/v1775726960/Efferalgan_jqcfn7.jpg'),(10,1,'Hapacol 150','Thuoc ha sot chuyen dung cho tre em',30000.00,70,20,'2025-03-15','2028-03-15','Gói bột','gói','150mg','DHG Pharma','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727012/Hapacol150_hgtmz5.jpg'),(11,8,'Dexamethasone','Thuoc khang viem manh, dieu tri di ung nang',10000.00,80,20,'2025-02-05','2027-02-05','Viên nén','viên','0.5mg','Mekophar','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727049/Dexamethasone_imzdmn.jpg'),(12,9,'Mebendazole','Thuoc tay giun dinh ky cho nguoi lon va tre em',55000.00,90,20,'2024-11-20','2027-11-20','Viên nén','viên','500mg','Mebiphar','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727101/Mebendazole_qr5iyw.jpg'),(13,4,'Smecta','Thuoc dieu tri tieu chay va dau thuc quan, da day',60000.00,45,20,'2025-01-25','2028-01-25','Gói bột','gói','3g','Ipsen','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727107/Smecta_pxtqnu.jpg'),(14,10,'Rodogyl','Khang sinh dac tri nhiem trung rang mieng, viem loi',70000.00,70,20,'2025-03-10','2028-03-10','Viên nén','viên','Spiramycin + Metronidazole','Sanofi','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727161/Rodogyl_yzm4vf.jpg'),(15,10,'Franrogyl','Dieu tri sau rang, viem chan rang va phu ne',10000.00,120,20,'2025-02-28','2028-02-28','Viên nén','viên','Spiramycin + Metronidazole','OPV','available','https://res.cloudinary.com/dczz59gpu/image/upload/v1775727167/Franrogyl_zztcjg.jpg'),(16,1,'Ibuprofen 400mg','Giảm đau, kháng viêm, hạ sốt',35000.00,20,10,'2025-05-03','2026-06-08','','viên','400mg','Traphaco','available','https://res.cloudinary.com/dnxp96rpm/image/upload/v1780495622/Screenshot_2026-06-03_210014_gjzshl.png');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_record`
--

LOCK TABLES `medical_record` WRITE;
/*!40000 ALTER TABLE `medical_record` DISABLE KEYS */;
INSERT INTO `medical_record` VALUES (1,1,1,'Nghi viem hong','Da tung cam cum','2026-04-10 09:30:00',NULL),(2,1,2,'Di ung da nhe','Da tung viem da co dia','2026-04-10 11:00:00',NULL),(3,3,2,'Viem da tiep xuc','Boi thuoc mo, tranh hoa chat','2026-04-10 12:30:00',NULL),(4,5,2,'Thuy dau','Cach ly, boi ho nuoc, ha sot','2026-04-10 14:00:00',NULL),(5,7,3,'Sau rang so 36','Han rang tham my','2026-04-10 15:30:00',NULL),(6,1,1,'Roi loan nhip tim nhe','Nghi ngoi, theo doi them','2026-04-10 17:00:00',NULL),(7,1,1,'Viêm họng nhẹ, có ho','Uống thuốc theo chỉ định, nghỉ ngơi và tái khám nếu sốt','2026-05-30 12:19:16',NULL),(8,1,1,'Rối loạn nhịp tim nhẹ','Uống thuốc theo chỉ định, nghỉ ngơi và theo dõi thêm','2026-05-30 13:37:02',15),(9,1,1,'Thiếu máu cơ tim nhẹ','Điều chỉnh chế độ ăn, dùng thuốc theo chỉ định','2026-05-30 16:25:12',11),(10,1,1,'Tăng huyết áp giai đoạn 1','Theo dõi huyết áp hằng ngày, giảm muối, tập thể dục, dùng thuốc hạ áp theo chỉ định','2026-05-30 17:02:27',10);
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,1,'Ban co lich hen vao 09:00 ngay 10/04/2026',0,'2026-04-09 18:00:00'),(2,3,'Ban co lich hen vao 10:30 ngay 10/04/2026',0,'2026-04-09 18:05:00'),(3,2,'Ban co lich kham voi benh nhan Nguyen An',1,'2026-04-09 18:10:00'),(4,4,'Ban co lich kham voi benh nhan Le Chi',0,'2026-04-09 18:15:00'),(5,1,'Ban co ket qua xet nghiem moi',1,'2026-04-10 08:00:00'),(6,2,'Ban da duoc phan cong lich kham moi',0,'2026-04-10 08:10:00'),(7,3,'Ban co lich hen vao 13:00 ngay 10/04/2026',0,'2026-04-10 08:20:00'),(8,4,'Don thuoc cua ban da duoc cap nhat',1,'2026-04-10 08:30:00'),(9,1,'Ban co lich hen vao 14:00 ngay 10/04/2026',0,'2026-04-10 08:40:00'),(10,2,'Ho so benh an da duoc cap nhat',1,'2026-04-10 08:50:00'),(11,7,'Lich hen cua ban da duoc xac nhan',0,'2026-06-03 18:07:08'),(12,1,'Lich hen #19 voi bac si Pham Dung vao 15:00 07/06/2026 da duoc xac nhan',0,'2026-06-03 18:51:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,1,'Nguyen An','2002-05-10','Nam','Da Nang','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724408/image11_haldjd.jpg'),(2,3,'Le Chi','2015-08-12','Nu','Quang Nam','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722654/image_4_zo9nhr.png'),(3,7,'Dang Thu','2006-09-15','Nu','Ha Noi','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723040/Lighthearted_z1fwdi.jpg'),(4,9,'Bui Nam','1985-03-20','Nam','Thanh pho Ho Chi Minh','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724409/image12_ocjsfs.jpg'),(5,11,'Do Hung','1970-11-05','Nam','Dong Nai','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724411/image9_yjzrqb.jpg'),(6,13,'Nguyen Thi Tuyet Trinh','2005-04-25','Nu','Can Tho','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722814/image1_zbpauf.png'),(7,14,'Duong Le Kim Phung','2005-02-17','Nu','Soc Trang','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723083/z7701887361673_45790b4fa6072813384cfd6dfca22887_fdvg9p.jpg'),(8,15,'Tran Anh Tuan','1958-09-23','Nam','Can Tho','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723319/image5_bptquf.jpg');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription`
--

LOCK TABLES `prescription` WRITE;
/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
INSERT INTO `prescription` VALUES (1,1,1,1,'2026-04-10 10:00:00'),(2,2,1,2,'2026-04-10 11:30:00'),(3,3,3,2,'2026-04-10 13:00:00'),(4,4,5,2,'2026-04-10 14:30:00'),(5,5,7,3,'2026-04-10 16:00:00'),(6,6,1,1,'2026-04-10 17:30:00'),(7,6,1,1,'2026-04-10 17:35:00'),(8,2,1,2,'2026-04-10 11:35:00'),(9,4,5,2,'2026-04-10 14:35:00'),(10,3,3,2,'2026-04-10 13:05:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription_detail`
--

LOCK TABLES `prescription_detail` WRITE;
/*!40000 ALTER TABLE `prescription_detail` DISABLE KEYS */;
INSERT INTO `prescription_detail` VALUES (1,1,1,10,'Ngay 2 lan, moi lan 1 vien'),(2,2,2,5,'Ngay 1 lan, moi lan 1 vien'),(3,3,3,7,'Ngay 1 lan buoi toi, moi lan 1 vien'),(4,4,4,8,'Ngay 2 lan, moi lan 1 vien'),(5,5,5,6,'Ngay 1 lan, moi lan 1 vien'),(6,6,6,10,'Ngay 2 lan, moi lan 1 vien'),(7,7,7,4,'Ngay 1 lan buoi sang, moi lan 1 vien'),(8,8,8,12,'Ngay 3 lan, moi lan 1 vien'),(9,9,9,5,'Ngay 1 lan, moi lan 1 vien'),(10,10,10,3,'Ngay 1 lan buoi toi, moi lan 1 vien');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_result`
--

LOCK TABLES `test_result` WRITE;
/*!40000 ALTER TABLE `test_result` DISABLE KEYS */;
INSERT INTO `test_result` VALUES (1,1,'Xet nghiem mau','Binh thuong','2026-04-10 09:45:00'),(2,2,'Test di ung','Di ung nhe voi thoi tiet','2026-04-10 11:15:00'),(3,3,'Soi da','Viem nhiem do vi khuan','2026-04-10 12:45:00'),(4,4,'Xet nghiem dich not phong','Duong tinh voi Varicella Zoster','2026-04-10 14:15:00'),(5,5,'Chup x-quang rang','Sau men rang dien rong','2026-04-10 15:45:00'),(6,6,'Diem tam do (ECG)','Nhip xoang hoi nhanh','2026-04-10 17:15:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Nguyen','An','an@gmail.com','901000001','patient_an','Abc@123','patient','2026-04-09 08:00:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724408/image11_haldjd.jpg'),(2,'Tran','Binh','binh@gmail.com','901000002','doctor_binh','Abc@123','doctor','2026-04-09 08:10:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723515/image6_mr167k.png'),(3,'Le','Chi','chi@gmail.com','901000003','patient_chi','Abc@123','patient','2026-04-09 08:20:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722654/image_4_zo9nhr.png'),(4,'Pham','Dung','dung@gmail.com','901000004','doctor_dung','Abc@123','doctor','2026-04-09 08:30:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723653/image7_j0izpd.png'),(5,'Vo','Ha','ha@gmail.com','901000005','staff_ha','Abc@123','staff','2026-04-09 08:40:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723238/imgae3_eumfhj.jpg'),(6,'Admin','System','admin@gmail.com','901000006','admin_system','Abc@123','admin','2026-04-09 08:50:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723803/images_knk042.png'),(7,'Dang','Thu','thu@gmail.com','901000007','patient_thu','Abc@123','patient','2026-04-09 08:55:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723040/Lighthearted_z1fwdi.jpg'),(8,'Ly','Minh','minh@gmail.com','901000008','doctor_minh','Abc@123','doctor','2026-04-09 09:00:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724405/image14_jab5qp.png'),(9,'Bui','Nam','nam@gmail.com','901000009','patient_nam','Abc@123','patient','2026-04-09 09:05:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724409/image12_ocjsfs.jpg'),(10,'Vu','Thinh','thinh@gmail.com','901000010','doctor_thinh','Abc@123','doctor','2026-04-09 09:10:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724612/image15_vdmxlr.png'),(11,'Do','Hung','hung@gmail.com','901000011','patient_hung','Abc@123','patient','2026-04-09 09:15:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775724411/image9_yjzrqb.jpg'),(12,'Diep','Chi','chi@gmail.com','901000012','staff_chi','Abc@123','staff','2026-04-09 09:20:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723244/image4_uzb2oq.jpg'),(13,'Nguyen Thi','Tuyet Trinh','tuyettrinhnguyenthi25042005@gmail.com','901000013','patient_trinh','Abc@123','patient','2026-04-09 09:25:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775722814/image1_zbpauf.png'),(14,'Duong Le','Kim Phung','kimphungduongle9@gmail.com','901000014','patient_phung','Abc@123','patient','2026-04-09 09:30:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723083/z7701887361673_45790b4fa6072813384cfd6dfca22887_fdvg9p.jpg'),(15,'Tran','Anh Tuan','trananhtuan23092005@gmail.com','901000015','patient_tuan','Abc@123','patient','2026-04-09 09:35:00','https://res.cloudinary.com/dczz59gpu/image/upload/v1775723319/image5_bptquf.jpg');
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

-- Dump completed on 2026-06-03 21:14:57
