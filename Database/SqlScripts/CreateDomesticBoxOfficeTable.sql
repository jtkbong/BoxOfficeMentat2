CREATE TABLE `boxofficementat`.`DomesticBoxOffice` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `MovieId` VARCHAR(100) NOT NULL,
  `StartDate` DATE NULL,
  `EndDate` DATE NULL,
  `Gross` INT NOT NULL,
  `TheaterCount` INT,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ASC),
  FOREIGN KEY (MovieId) REFERENCES Movies(Id)
);
