CREATE TABLE `People` (
  `Id` varchar(120) NOT NULL,
  `Name` varchar(120) NOT NULL,
  `Actor` tinyint(4) NOT NULL DEFAULT '0',
  `Director` tinyint(4) NOT NULL DEFAULT '0',
  `Producer` tinyint(4) NOT NULL DEFAULT '0',
  `ScreenWriter` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;