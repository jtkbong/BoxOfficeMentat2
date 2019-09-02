CREATE TABLE `boxofficementat`.`Reviews` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `MovieId` VARCHAR(100) NOT NULL,
  `DateTime` DATETIME NULL,
  `ReviewText` BLOB NULL,
  `ReviewStats` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ASC),
  FOREIGN KEY (MovieId) REFERENCES Movies(Id)
 );
