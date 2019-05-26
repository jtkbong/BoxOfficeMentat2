CREATE TABLE `Studios` (
  `Id` varchar(110) NOT NULL,
  `Name` varchar(120) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;