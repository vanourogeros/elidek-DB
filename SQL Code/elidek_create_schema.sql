CREATE TABLE IF NOT EXISTS Executive (
  Executive_ID INT UNSIGNED NOT NULL,
  Name VARCHAR(45) NOT NULL,
  Surname VARCHAR(45) NOT NULL,
  -- Position VARCHAR(45) NULL,
  PRIMARY KEY (Executive_ID))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Program`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Program (
  Program_ID INT UNSIGNED NOT NULL,
  Name VARCHAR(45) NOT NULL,
  ELIDEK_Sector VARCHAR(45) NOT NULL,
  PRIMARY KEY (Program_ID))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Organization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS  Organization (
  Organization_ID INT UNSIGNED NOT NULL,
  Acronym VARCHAR(45) NOT NULL,
  Name VARCHAR(45) NOT NULL,
  Street VARCHAR(45) NOT NULL,
  Street_Number INT UNSIGNED NOT NULL,
  City VARCHAR(45) NOT NULL,
  Postal_Code INT UNSIGNED NOT NULL,
  Org_type ENUM('University', 'Company', 'Research Center') NOT NULL,
  CHECK(Postal_Code > 9999 and Postal_Code < 100000),
  PRIMARY KEY (Organization_ID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table mydb.`Researcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS  Researcher (
  Researcher_ID INT UNSIGNED NOT NULL,
  Name VARCHAR(45) NOT NULL,
  Surname VARCHAR(45) NOT NULL,
  Gender VARCHAR(45) NOT NULL,
  Birth_Date DATE NOT NULL,
  Recruitment_Date DATE NOT NULL,
  Organization_ID INT UNSIGNED NOT NULL,
  CHECK(Gender IN ('Male','Female','Other')),
  CHECK(DATEDIFF(NOW(), Birth_Date) > 5840 AND DATEDIFF(Recruitment_Date, NOW()) < 0), -- Researcher must be at least 16 years old
  PRIMARY KEY (Researcher_ID),
  INDEX fk_Researcher_Organization1_idx (Organization_ID ASC) ,
  CONSTRAINT fk_Researcher_Organization1
    FOREIGN KEY (Organization_ID)
    REFERENCES Organization (Organization_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table mydb.`Project`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS  Project (
  Project_ID INT UNSIGNED NOT NULL,
  Name VARCHAR(45) NOT NULL,
  Summary VARCHAR(1500) NOT NULL,
  Project_Funds VARCHAR(45) NOT NULL CHECK (Project_Funds > 100000 AND Project_Funds < 1000000),
  Start_Date DATE NOT NULL,
  End_Date DATE NOT NULL,
  CHECK(DATEDIFF(End_Date,Start_Date) > 364 AND DATEDIFF(End_Date,Start_Date) < 1461 AND DATEDIFF(Start_Date, NOW()) < 0),
  Executive_ID INT UNSIGNED NOT NULL,
  Program_ID INT UNSIGNED NOT NULL,
  Organization_ID INT UNSIGNED NOT NULL,
  Research_Manager_ID INT UNSIGNED NOT NULL,
  PRIMARY KEY (Project_ID),
  INDEX fk_Project_Executive_idx (Executive_ID ASC) ,
  INDEX fk_Project_Program_idx (Program_ID ASC) ,
  INDEX fk_Project_Organization_idx (Organization_ID ASC) ,
  UNIQUE INDEX Project_ID_UNIQUE (Project_ID ASC) ,
  CONSTRAINT fk_Project_Organization
    FOREIGN KEY (Organization_ID)
    REFERENCES Organization (Organization_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_Manages
    FOREIGN KEY (Executive_ID)
    REFERENCES Executive (Executive_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_Research_Manager
    FOREIGN KEY (Research_Manager_ID)
    REFERENCES Researcher (Researcher_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_Project_Program
    FOREIGN KEY (Program_ID)
    REFERENCES Program (Program_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table mydb.`University`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS University (
  University_ID INT UNSIGNED NOT NULL,
  Ministry_Budget INT UNSIGNED NULL,
  PRIMARY KEY (University_ID),
  Org_type ENUM('University') NOT NULL REFERENCES Organization (Org_Type),
  CONSTRAINT fk_University_Organization1
    FOREIGN KEY (University_ID)
    REFERENCES Organization (Organization_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Research Center`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Research_Center (
  Research_Center_ID INT UNSIGNED NOT NULL,
  Org_type ENUM('Research Center') NOT NULL REFERENCES Organization (Org_Type),
  Ministry_Budget VARCHAR(45) NULL,
  Actions_Budget VARCHAR(45) NULL,
  PRIMARY KEY (Research_Center_ID),
  CONSTRAINT fk_Research_Center_ID
    FOREIGN KEY (Research_Center_ID)
    REFERENCES Organization (Organization_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Company (
  Company_ID INT UNSIGNED NOT NULL,
  Org_type ENUM('Company') NOT NULL REFERENCES Organization (Org_Type),
  Equity INT UNSIGNED NULL,
  PRIMARY KEY (Company_ID),
  CONSTRAINT fk_Company_ID
    FOREIGN KEY (Company_ID)
    REFERENCES Organization (Organization_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Research_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Research_Field (
  Field_ID INT UNSIGNED NOT NULL,
  Name VARCHAR(45) NOT NULL,
  PRIMARY KEY (Field_ID))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Work_to_be_Submitted`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Work_to_be_Submitted (
  Title VARCHAR(45) NOT NULL,
  Project_ID INT UNSIGNED NOT NULL,
  Summary VARCHAR(300) NOT NULL,
  Submission_Date DATE NOT NULL,
  PRIMARY KEY (Title, Project_ID),
  INDEX fk_project0_idx (Project_ID ASC) ,
  CONSTRAINT fk_project0
    FOREIGN KEY (Project_ID)
    REFERENCES Project (Project_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Works_On`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Works_On (
  Researcher_ID INT UNSIGNED NOT NULL,
  Project_ID INT UNSIGNED NOT NULL,
  Start_Date DATE NOT NULL,
  PRIMARY KEY (Researcher_ID, Project_ID),
  INDEX fk_project_idx (Project_ID ASC) ,
  CONSTRAINT fk_project
    FOREIGN KEY (Project_ID)
    REFERENCES Project (Project_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_researcher
    FOREIGN KEY (Researcher_ID)
    REFERENCES Researcher (Researcher_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Evaluation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Evaluation (
  Researcher_ID INT UNSIGNED NOT NULL,
  Project_ID INT UNSIGNED NOT NULL,
  Evaluation_Date DATE NOT NULL,
  Evaluation_Grade INT UNSIGNED NULL,
  PRIMARY KEY (Researcher_ID, Project_ID),
  INDEX fk_Project_ID_idx (Project_ID ASC) ,
  CONSTRAINT fk_Researcher_ID
    FOREIGN KEY (Researcher_ID)
    REFERENCES Researcher (Researcher_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_Project_ID
    FOREIGN KEY (Project_ID)
    REFERENCES Project (Project_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Org_Phone`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Org_Phone (
  Organization_ID INT UNSIGNED NOT NULL,
  Phone_Number CHAR(10) NOT NULL,
  CONSTRAINT chk_phone CHECK (Phone_Number RLIKE('[0-9]{10}')),
  -- CONSTRAINT chk_phone CHECK REGEXP('[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'), -- check that no number is not a digit 
  PRIMARY KEY (Organization_ID, Phone_Number),
  CONSTRAINT fk_Organization_ID
    FOREIGN KEY (Organization_ID)
    REFERENCES Organization (Organization_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.`Refers_To`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Refers_To (
  Field_ID INT UNSIGNED NOT NULL,
  Project_ID INT UNSIGNED NOT NULL,
  PRIMARY KEY (Field_ID, Project_ID),
  INDEX Project_Field_ID_idx (Project_ID ASC) ,
  CONSTRAINT Field_ID
    FOREIGN KEY (Field_ID)
    REFERENCES Research_Field (Field_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT Project_Field_ID
    FOREIGN KEY (Project_ID)
    REFERENCES Project (Project_ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


DELIMITER $
CREATE TRIGGER chk_Eval_Not_Work_On BEFORE INSERT ON Evaluation 
FOR EACH ROW
BEGIN
    IF ((SELECT Organization_ID FROM Researcher WHERE Researcher_ID = new.Researcher_ID) = (SELECT Organization_ID FROM Project WHERE Project_ID = new.Project_ID) ) THEN 
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Evaluation failed - A researcher cannot evaluate a project from their organization';
    END IF;
    
    IF (DATEDIFF(new.Evaluation_Date, (SELECT Start_Date FROM Project WHERE Project_ID = new.Project_ID) > 0)) THEN 
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Evaluation failed - Evaluation date must be before project start date';
    END IF;
    
    IF (new.Project_ID IN (SELECT Project_ID FROM evaluation)) THEN
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Evaluation failed - Project already has an evaluator';
    END IF;
END$   
DELIMITER ; 

DELIMITER ;

DELIMITER $
CREATE TRIGGER chk_Res_Work_On_One_Org BEFORE INSERT ON Works_On 
FOR EACH ROW
BEGIN
    IF ((SELECT Organization_ID FROM Researcher WHERE Researcher_ID = new.Researcher_ID) <> 
        (SELECT Organization_ID FROM Project WHERE Project_ID = new.Project_ID)) THEN 
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Works_On failed - A researcher can only work on projects from the organization they are in.';
    END IF;
    
    IF (DATEDIFF(new.Start_Date, (SELECT End_Date FROM Project WHERE Project_ID = new.Project_ID)) > 0 OR 
        DATEDIFF(new.Start_Date, (SELECT Start_Date FROM Project WHERE Project_ID = new.Project_ID)) < 0) THEN 
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Works_On failed - Start date must be between start and end date of project.';
    END IF;
END$   
DELIMITER ; 

DELIMITER $
CREATE TRIGGER chk_Work_Submission_between_projDates BEFORE INSERT ON Work_To_Be_Submitted 
FOR EACH ROW
BEGIN
    IF (DATEDIFF(new.Submission_Date, (SELECT End_Date FROM Project WHERE Project_ID = new.Project_ID)) > 0 OR 
        DATEDIFF(new.Submission_Date, (SELECT Start_Date FROM Project WHERE Project_ID = new.Project_ID)) < 0) THEN 
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Work_To_Be_Submitted failed - Submission date must be between start and end date of project.';
    END IF;
END$   
DELIMITER ; 

DELIMITER $
CREATE TRIGGER chk_res_org_update BEFORE UPDATE ON Researcher
FOR EACH ROW
BEGIN
    IF (new.Organization_ID <> old.Organization_ID) THEN 
		IF ((SELECT COUNT(*) FROM Works_On WHERE Works_On.Researcher_ID = old.Researcher_ID) > 0) THEN
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Researcher failed - Organization can only change if researcher has no projects.';
	   END IF;
    END IF;
END$   
DELIMITER ; 

DELIMITER $
CREATE TRIGGER chk_proj_org_update BEFORE UPDATE ON Project
FOR EACH ROW
BEGIN
    IF (new.Organization_ID <> old.Organization_ID) THEN 
		IF ((SELECT COUNT(*) FROM Works_On WHERE Works_On.Project_ID = old.Project_ID) > 0) THEN
    SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on Project failed - Organization can only change if project has no researchers.';
	   END IF;
    END IF;
END$   
DELIMITER ; 

DELIMITER $
CREATE TRIGGER chk_phone_unique BEFORE INSERT ON org_phone
FOR EACH ROW
BEGIN
    IF (new.Phone_Number IN (SELECT Phone_Number from org_phone)) THEN
	SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on org_phone failed - A phone number cannot exist twice in the table.';
    END IF;
END$   
DELIMITER ; 

-- -----------------------------------------------------
-- View 1: Projects per Researcher
-- -----------------------------------------------------


CREATE VIEW projects_per_researcher AS
SELECT Researcher.Researcher_ID,
	   CONCAT(Researcher.Name, ' ', Researcher.Surname) AS `Full_Name`,
       Researcher.Organization_ID AS Org_ID,
       Project.Project_ID,
       Project.Name AS `Project_Name`
FROM Researcher INNER JOIN Works_On ON Researcher.Researcher_ID=Works_On.Researcher_ID
INNER JOIN Project on Works_On.Project_ID=Project.Project_ID
ORDER BY Researcher.Researcher_ID;

-- -----------------------------------------------------
-- View 2: Projects per Field
-- -----------------------------------------------------

CREATE VIEW projects_per_field AS
SELECT Project.Project_ID,
       Project.Name AS `Project_Name`,
       Research_Field.Field_ID,
       Research_Field.Name as `Field_Name`
FROM Project INNER JOIN Refers_To ON Project.Project_ID=Refers_To.Project_ID
INNER JOIN Research_Field on Refers_To.Field_ID=Research_Field.Field_ID
ORDER BY Field_ID;





