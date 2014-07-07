SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema bo14g23
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bo14g23` DEFAULT CHARACTER SET utf8 ;
USE `bo14g23` ;

-- -----------------------------------------------------
-- Table `bo14g23`.`campus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`campus` (
  `campus_id` INT(11) NOT NULL AUTO_INCREMENT,
  `campus_name` VARCHAR(255) NOT NULL,
  `lonlat` POINT NOT NULL,
  PRIMARY KEY (`campus_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `bo14g23`.`institution`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`institution` (
  `institution_id` INT(11) NOT NULL AUTO_INCREMENT,
  `institution_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`institution_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8
COMMENT = 'Educational institution';


-- -----------------------------------------------------
-- Table `bo14g23`.`department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`department` (
  `department_id` INT(11) NOT NULL AUTO_INCREMENT,
  `institution_id` INT(11) NOT NULL,
  `department_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`department_id`),
  INDEX `fk_avdeling_institusjon1_idx` (`institution_id` ASC),
  CONSTRAINT `fk_avdeling_institusjon1`
    FOREIGN KEY (`institution_id`)
    REFERENCES `bo14g23`.`institution` (`institution_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `bo14g23`.`study`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`study` (
  `study_id` INT(11) NOT NULL AUTO_INCREMENT,
  `department_id` INT(11) NOT NULL,
  `campus_id` INT(11) NOT NULL,
  `name_of_study` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`study_id`),
  INDEX `fk_Studie_Avdeling1` (`department_id` ASC),
  INDEX `fk_studie_studiested1_idx` (`campus_id` ASC),
  CONSTRAINT `fk_Studie_Avdeling10`
    FOREIGN KEY (`department_id`)
    REFERENCES `bo14g23`.`department` (`department_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_studie_studiested1`
    FOREIGN KEY (`campus_id`)
    REFERENCES `bo14g23`.`campus` (`campus_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `bo14g23`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`user` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `study_id` INT(11) NOT NULL,
  `firstname` VARCHAR(255) NOT NULL,
  `surname` VARCHAR(255) NOT NULL,
  `latlon` POINT NOT NULL,
  `car` TINYINT(1) NOT NULL,
  `starting_year` INT(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  INDEX `fk_Bruker_Studie1` (`study_id` ASC),
  CONSTRAINT `fk_Bruker_Studie10`
    FOREIGN KEY (`study_id`)
    REFERENCES `bo14g23`.`study` (`study_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 234
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `bo14g23`.`email_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`email_user` (
  `user_id` INT(11) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`email`),
  INDEX `fk_Alternativ_Innlogging_Brukere1` (`user_id` ASC),
  CONSTRAINT `fk_Alternativ_Innlogging_Brukere10`
    FOREIGN KEY (`user_id`)
    REFERENCES `bo14g23`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `bo14g23`.`facebook_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`facebook_user` (
  `user_id` INT(11) NOT NULL,
  `facebook_id` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`facebook_id`),
  INDEX `fk_Facebook_Innlogging_Brukere1` (`user_id` ASC),
  CONSTRAINT `fk_Facebook_Innlogging_Brukere10`
    FOREIGN KEY (`user_id`)
    REFERENCES `bo14g23`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `bo14g23`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bo14g23`.`message` (
  `user_id_sender` INT(11) NOT NULL,
  `user_id_receiver` INT(11) NOT NULL,
  `message` TEXT NOT NULL,
  `sent` DATETIME NOT NULL,
  `read` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`user_id_sender`, `user_id_receiver`, `sent`),
  INDEX `fk_Meldingslogg_Student1` (`user_id_sender` ASC),
  CONSTRAINT `fk_Meldingslogg_Student10`
    FOREIGN KEY (`user_id_sender`)
    REFERENCES `bo14g23`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
