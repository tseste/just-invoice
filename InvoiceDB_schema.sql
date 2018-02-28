-- MySQL dump 10.15  Distrib 10.0.33-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: InvoiceDB
-- ------------------------------------------------------
-- Server version	10.0.33-MariaDB

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
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customer` (
  `CustomerId` int(11) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `LastName` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Company` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Address` varchar(70) COLLATE utf8_unicode_ci DEFAULT NULL,
  `City` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Country` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `PostalCode` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Phone` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fax` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Email` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TRN` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `TaxOffice` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`CustomerId`),
  UNIQUE KEY `Customer_UN` (`TRN`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Invoice`
--

DROP TABLE IF EXISTS `Invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Invoice` (
  `InvoiceId` int(11) NOT NULL,
  `CustomerId` int(11) NOT NULL,
  `InvoiceDate` datetime NOT NULL,
  `BillingAddress` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BillingCity` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BillingCountry` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BillingPostalCode` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`InvoiceId`),
  KEY `Invoice_Customer_FK` (`CustomerId`),
  CONSTRAINT `Invoice_Customer_FK` FOREIGN KEY (`CustomerId`) REFERENCES `Customer` (`CustomerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `InvoiceRow`
--

DROP TABLE IF EXISTS `InvoiceRow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `InvoiceRow` (
  `InvoiceRowId` int(11) NOT NULL AUTO_INCREMENT,
  `InvoiceId` int(11) NOT NULL,
  `ProductId` int(11) NOT NULL,
  `UnitPrice` decimal(10,2) NOT NULL,
  `Quantity` float NOT NULL,
  `Units` float NOT NULL,
  PRIMARY KEY (`InvoiceRowId`),
  KEY `InvoiceRow_Invoice_FK` (`InvoiceId`),
  KEY `InvoiceRow_Product_FK` (`ProductId`),
  CONSTRAINT `InvoiceRow_Invoice_FK` FOREIGN KEY (`InvoiceId`) REFERENCES `Invoice` (`InvoiceId`),
  CONSTRAINT `InvoiceRow_Product_FK` FOREIGN KEY (`ProductId`) REFERENCES `Product` (`ProductId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Product` (
  `ProductId` int(11) NOT NULL AUTO_INCREMENT,
  `Name` mediumtext COLLATE utf8_unicode_ci NOT NULL,
  `Description` text COLLATE utf8_unicode_ci,
  `UnitTypeId` int(11) NOT NULL,
  `UnitPrice` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ProductId`),
  KEY `Product_ProductUnitType_FK` (`UnitTypeId`),
  CONSTRAINT `Product_ProductUnitType_FK` FOREIGN KEY (`UnitTypeId`) REFERENCES `ProductUnitType` (`UnitTypeId`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ProductUnitType`
--

DROP TABLE IF EXISTS `ProductUnitType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ProductUnitType` (
  `UnitTypeId` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`UnitTypeId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'InvoiceDB'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_Customer` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_Customer`(
FirstName_pr VARCHAR(50),
LastName_pr VARCHAR(50),
Company_pr VARCHAR(80),
Address_pr VARCHAR(70),
City_pr VARCHAR(40),
Country_pr VARCHAR(40),
PostalCode_pr VARCHAR(10),
Phone_pr VARCHAR(24),
Fax_pr VARCHAR(24),
Email_pr VARCHAR(60),
TRN_pr VARCHAR(20),
TaxOffice_pr VARCHAR(40))
BEGIN
	IF EXISTS(SELECT 1 FROM Customer WHERE TRN=TRN_pr) THEN 
		UPDATE Customer
		SET FirstName=FirstName_pr,
			LastName=LastName_pr,
			Company=Company_pr,
			Address=Address_pr,
			City=City_pr,
			Country=Country_pr,
			PostalCode=PostalCode_pr,
			Phone=Phone_pr,
			Fax=Fax_pr,
			Email=Email_pr,
			TRN=TRN_pr,
			TaxOffice=TaxOffice_pr
		WHERE TRN=TRN_pr;
	ELSE
		INSERT INTO Customer (FirstName, LastName,
							  Company, Address,
							  City, Country,
							  PostalCode, Phone,
							  Fax, Email, TRN,
							  TaxOffice)

		VALUES (FirstName_pr, LastName_pr,
			    Company_pr, Address_pr,
			    City_pr, Country_pr,
			    PostalCode_pr, Phone_pr,
			    Fax_pr, Email_pr, TRN_pr,
			    TaxOffice_pr);
	END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_Product` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_Product`(
Name_pr MEDIUMTEXT,
Description_pr TEXT,
UnitTypeId_pr INTEGER,
UnitPrice_pr DECIMAL(10,2))
BEGIN
	IF EXISTS(SELECT 1 FROM Product WHERE Name=Name_pr) THEN 
		UPDATE Product
		SET Name=Name_pr,
			Description=Description_pr,
			UnitTypeId=UnitTypeId_pr,
			UnitPrice=UnitPrice_pr
		WHERE Name=Name_pr;
	ELSE
		INSERT INTO Product (Name, Description, UnitTypeId, UnitPrice)
		VALUES (Name_pr, Description_pr, UnitTypeId_pr, UnitPrice_pr);
	END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-28 17:47:44
