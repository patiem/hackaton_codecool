BEGIN TRANSACTION;
CREATE TABLE `Quiz` (
	`ID`	INTEGER,
	`Title`	TEXT NOT NULL,
	PRIMARY KEY(`ID`)
);
INSERT INTO `Quiz` VALUES (1,'English');
INSERT INTO `Quiz` VALUES (2,'Math');
CREATE TABLE `Questions` (
	`Id`	INTEGER,
	`quiz_id`	INTEGER NOT NULL,
	`question`	TEXT NOT NULL,
	`img`	TEXT,
	`a_one`	TEXT NOT NULL,
	`a_two`	TEXT NOT NULL,
	`a_three`	TEXT NOT NULL,
	`a_good`	TEXT NOT NULL,
	PRIMARY KEY(`Id`)
);
INSERT INTO `Questions` VALUES (1,1,'What is it?','http://kids.nationalgeographic.com/content/dam/kids/photos/animals/Mammals/H-P/photoark-lion.png.adapt.945.1.jpg','lion','dog','cat','lion');
INSERT INTO `Questions` VALUES (2,1,'What is it?','http://www.freeiconspng.com/uploads/png-tree-8-by-paradise234-d5hfi67-18.png','flower','tree','trash','tree');
INSERT INTO `Questions` VALUES (3,1,'What is it?','http://www.wnd.com/files/2015/03/poop-emoji-emoticon-600-300x300.jpg','bee','pee','poo','poo');
INSERT INTO `Questions` VALUES (4,2,'4 + 4 = ?','','4','8','0','8');
INSERT INTO `Questions` VALUES (5,2,'4 - 4 = ?','','4','8','0','poo');
INSERT INTO `Questions` VALUES (6,2,'4 * 4 = ?','','16','8','0','poo');
COMMIT;
