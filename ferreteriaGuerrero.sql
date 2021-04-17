-- MySQL dump 10.16  Distrib 10.1.34-MariaDB, for Win32 (AMD64)
--
-- Host: localhost    Database: ferreteria_guerrero
-- ------------------------------------------------------
-- Server version	10.1.34-MariaDB

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
-- Table structure for table `caja`
--

DROP TABLE IF EXISTS `caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `caja` (
  `todal_dinero` decimal(10,0) NOT NULL,
  `50cent` int(11) NOT NULL,
  `peso` int(11) NOT NULL,
  `2pesos` int(11) NOT NULL,
  `5pesos` int(11) NOT NULL,
  `10pesos` int(11) NOT NULL,
  `20pesos` int(11) NOT NULL,
  `50pesos` int(11) NOT NULL,
  `100pesos` int(11) NOT NULL,
  `200pesos` int(11) NOT NULL,
  `500pesos` int(11) NOT NULL,
  `1000 pesos` int(11) NOT NULL,
  `ultima_mod` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caja`
--

LOCK TABLES `caja` WRITE;
/*!40000 ALTER TABLE `caja` DISABLE KEYS */;
/*!40000 ALTER TABLE `caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `rfc` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (2,'a','a','a','p@g.com','','');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `creditos`
--

DROP TABLE IF EXISTS `creditos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `descripcion_productos` varchar(500) NOT NULL,
  `adeudo` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creditos`
--

LOCK TABLES `creditos` WRITE;
/*!40000 ALTER TABLE `creditos` DISABLE KEYS */;
INSERT INTO `creditos` VALUES (2,2,'2021-03-21','2021-04-21','',0),(4,2,'2021-03-21','2021-03-21','',0);
/*!40000 ALTER TABLE `creditos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proveedor` varchar(100) NOT NULL,
  `dia` date NOT NULL,
  `hora` time NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(20) NOT NULL,
  `producto` varchar(50) NOT NULL,
  `grupo` varchar(50) NOT NULL DEFAULT '---',
  `preciopublico` float NOT NULL DEFAULT '0',
  `stockminimo` int(11) NOT NULL DEFAULT '0',
  `stockmaximo` int(11) NOT NULL DEFAULT '0',
  `stock` float NOT NULL DEFAULT '0',
  `proveedor` varchar(100) NOT NULL DEFAULT 'Desconocido',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=325 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (253,'253508','a','',0,0,0,0,'Desconocido'),(254,'254514','a','',0,0,0,0,'Desconocido'),(255,'255520','a','',0,0,0,0,'Desconocido'),(256,'256533','a','',0,0,0,0,'Desconocido'),(257,'257546','a','',0,0,0,0,'Desconocido'),(258,'258554','a','',0,0,0,0,'Desconocido'),(259,'259563','a','',0,0,0,0,'Desconocido'),(260,'260575','a','',0,0,0,0,'Desconocido'),(261,'261584','a','',0,0,0,0,'Desconocido'),(262,'262591','a','',0,0,0,0,'Desconocido'),(263,'26301','a','',0,0,0,0,'Desconocido'),(264,'26424','a','',0,0,0,0,'Desconocido'),(265,'265330','a','',0,0,0,0,'Desconocido'),(266,'266356','a','',0,0,0,0,'Desconocido'),(267,'267384','a','',0,0,0,0,'Desconocido'),(268,'268406','a','',0,0,0,0,'Desconocido'),(269,'269425','s','',0,0,0,0,'Desconocido'),(270,'270436','d','',0,0,0,0,'Desconocido'),(271,'271458','f','',0,0,0,0,'Desconocido'),(272,'272470','g','',0,0,0,0,'Desconocido'),(273,'273487','h','',0,0,0,0,'Desconocido'),(274,'274500','j','',0,0,0,0,'Desconocido'),(275,'275511','k','',0,0,0,0,'Desconocido'),(276,'276534','l','',0,0,0,0,'Desconocido'),(277,'277550','q','',0,0,0,0,'Desconocido'),(278,'278563','w','',0,0,0,0,'Desconocido'),(279,'279581','e','',0,0,0,0,'Desconocido'),(280,'28009','r','',0,0,0,0,'Desconocido'),(281,'28120','t','',0,0,0,0,'Desconocido'),(282,'28239','y','',0,0,0,0,'Desconocido'),(283,'28346','u','',0,0,0,0,'Desconocido'),(284,'28458','i','',0,0,0,0,'Desconocido'),(285,'28573','o','',0,0,0,0,'Desconocido'),(286,'28688','p','',0,0,0,0,'Desconocido'),(288,'288120','n','',0,0,0,0,'Desconocido'),(289,'289136','b','',0,0,0,0,'Desconocido'),(290,'290159','v','',0,0,0,0,'Desconocido'),(291,'291177','c','',0,0,0,0,'Desconocido'),(292,'292447','qq','',0,0,0,0,'Desconocido'),(293,'293466','ww','',0,0,0,0,'Desconocido'),(294,'294508','ee','',0,0,0,0,'Desconocido'),(296,'296542','tt','',0,0,0,0,'Desconocido'),(297,'297563','yy','',0,0,0,0,'Desconocido'),(298,'298577','uu','',0,0,0,0,'Desconocido'),(299,'299598','ii','',0,0,0,0,'Desconocido'),(301,'301201','otro producto','no lo se',500,10,20,15,'Desconocido'),(302,'302569','qwqwqw','',0,0,0,0,'Desconocido'),(303,'30307','bgbg','',0,0,0,0,'Desconocido'),(305,'999999','jueAS','el grupo',500,10,20,15,'Desconocido'),(309,'309108','Su papi muñaño','',100,0,50,8,'Desconocido'),(310,'310336','producto','grupo',4,1,2,3,'Desconocido'),(311,'311556','product','group',4,1,2,3,'Desconocido'),(312,'31232','cople 1/2','plus',0,0,0,54,'Desconocido'),(313,'313144','cople 1/4','plus',0,0,0,10,'Desconocido'),(314,'314416','cople 2/4','plus',0,0,0,0,'Desconocido'),(315,'315568','cople 2/5','galvanizado',0,0,0,0,'Desconocido'),(316,'316134','cople 2/4','galvanizado',0,0,0,0,'Desconocido'),(317,'317293','cople 2 piuk','plus',0,0,0,0,'Desconocido'),(318,'318510','cople 3/4','cpvc',20,0,0,9,'Desconocido'),(319,'319119','cople 1/2','cpvc',12,0,0,7,'Desconocido'),(320,'123','producto1','',0,0,0,0,'Desconocido'),(321,'1234','producto2','',0,0,0,19,'Desconocido'),(322,'12345','producto3','',0,0,0,2,'Desconocido'),(323,'323582','un producto 123','',0,0,0,0,'Desconocido'),(324,'324141','otro producto 1234','',0,0,0,0,'Desconocido');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_credito`
--

DROP TABLE IF EXISTS `productos_credito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productos_credito` (
  `id_credito` int(11) NOT NULL,
  `producto` varchar(50) NOT NULL,
  `cantidad` float NOT NULL DEFAULT '0',
  `precio` float NOT NULL DEFAULT '0',
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_credito`
--

LOCK TABLES `productos_credito` WRITE;
/*!40000 ALTER TABLE `productos_credito` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos_credito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_ventas`
--

DROP TABLE IF EXISTS `productos_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productos_ventas` (
  `id_venta` int(11) NOT NULL,
  `producto` varchar(100) NOT NULL,
  `cantidad` float NOT NULL,
  `precio` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_ventas`
--

LOCK TABLES `productos_ventas` WRITE;
/*!40000 ALTER TABLE `productos_ventas` DISABLE KEYS */;
INSERT INTO `productos_ventas` VALUES (1,'new',1,0),(7,'producto1',1,0),(8,'producto3',4,0),(8,'producto2',1,0);
/*!40000 ALTER TABLE `productos_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'un proveedor','123','nua dire'),(2,'abram','','');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surtidos`
--

DROP TABLE IF EXISTS `surtidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surtidos` (
  `id_producto` int(11) NOT NULL,
  `id_proveedor` int(11) NOT NULL,
  `fecha_surtido` date NOT NULL,
  `precio_compra` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surtidos`
--

LOCK TABLES `surtidos` WRITE;
/*!40000 ALTER TABLE `surtidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `surtidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `productos` tinyint(1) NOT NULL,
  `inventario` tinyint(1) NOT NULL,
  `proveedores` tinyint(1) NOT NULL,
  `clientes` tinyint(1) NOT NULL,
  `creditos` tinyint(1) NOT NULL,
  `ventas` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (14,'Administrador','1234',1,1,1,1,1,1),(19,'chuy','123',0,0,0,0,0,1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `cliente` varchar(100) NOT NULL,
  `tipodeventa` varchar(20) NOT NULL,
  `metododepago` varchar(20) NOT NULL,
  `fecha` date NOT NULL,
  `importe` float NOT NULL,
  `pago` float NOT NULL,
  `cambio` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,'Administrador','Público  en general','Al Contado','Efectivo','2021-02-22',0,0,0),(2,'Administrador','Público  en general','Al Contado','Efectivo','2021-02-23',0,0,0),(7,'Administrador','Público  en general','Al Contado','Efectivo','2021-02-25',0,0,0),(8,'Administrador','Público  en general','Al Contado','Efectivo','2021-02-25',0,0,0);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-17 17:05:27
