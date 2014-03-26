import sqlite3

def buildDB():

	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()

	#create the tables
	c.execute('create table eskimo_versions (id integer primary key not null, version int, prefix varchar(255), length integer);')
	c.execute('create table eskimo_currencies (id integer primary key not null, currency varchar(255), longName varchar(255), version integer, foreign key(version) references eskimo_versions(id));')
	c.execute('create table eskimo_privK (id integer primary key not null, privK varchar(255), currency integer, foreign key(currency) references eskimo_currencies(id));')

	#load the known data about version numbers
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (0,'1',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (1,'Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|m|n|o',33))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (2,'o|p|q|r|s|t|u|v|w|x|y|z|2',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (3,'2',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (4,'2|3',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (5,'3',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (6,'3',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (7,'3|4',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (8,'4',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (9,'4|5',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (10,'5',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (11,'5',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (12,'5|6',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (13,'6',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (14,'6|7',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (15,'7',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (16,'7',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (17,'7|8',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (18,'8',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (19,'8|9',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (20,'9',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (21,'9',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (22,'9|A',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (23,'A',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (24,'A|B',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (25,'B',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (26,'B',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (27,'B|C',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (28,'C',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (29,'C|D',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (30,'D',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (31,'D',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (32,'D|E',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (33,'E',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (34,'E|F',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (35,'F',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (36,'F',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (37,'F|G',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (38,'G',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (39,'G|H',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (40,'H',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (41,'H',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (42,'H|J',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (43,'J',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (44,'J|K',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (45,'K',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (46,'K',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (47,'K|L',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (48,'L',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (49,'L|M',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (50,'M',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (51,'M',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (52,'M|N',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (53,'N',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (54,'N|P',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (55,'P',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (56,'P',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (57,'P|Q',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (58,'Q',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (59,'Q|R',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (60,'R',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (61,'R',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (62,'R|S',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (63,'S',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (64,'S|T',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (65,'T',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (66,'T',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (67,'T|U',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (68,'U',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (69,'U|V',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (70,'V',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (71,'V',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (72,'V|W',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (73,'W',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (74,'W|X',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (75,'X',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (76,'X',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (77,'X|Y',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (78,'Y',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (79,'Y|Z',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (80,'Z',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (81,'Z',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (82,'Z|a',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (83,'a',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (84,'a|b',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (85,'b',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (86,'b|c',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (87,'c',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (88,'c',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (89,'c|d',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (90,'d',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (91,'d|e',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (92,'e',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (93,'e',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (94,'e|f',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (95,'f',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (96,'f|g',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (97,'g',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (98,'g',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (99,'g|h',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (100,'h',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (101,'h|i',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (102,'i',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (103,'i',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (104,'i|j',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (105,'j',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (106,'j|k',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (107,'k',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (108,'k',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (109,'k|m',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (110,'m',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (111,'m|n',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (112,'n',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (113,'n',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (114,'n|o',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (115,'o',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (116,'o|p',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (117,'p',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (118,'p',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (119,'p|q',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (120,'q',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (121,'q|r',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (122,'r',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (123,'r',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (124,'r|s',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (125,'s',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (126,'s|t',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (127,'t',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (128,'t',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (129,'t|u',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (130,'u',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (131,'u|v',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (132,'v',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (133,'v',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (134,'v|w',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (135,'w',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (136,'w|x',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (137,'x',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (138,'x',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (139,'x|y',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (140,'y',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (141,'y|z',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (142,'z',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (143,'z',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (144,'z|2',34))
	c.execute('insert into eskimo_versions (version, prefix, length) VALUES (?,?,?);', (145,'2',35))


	conn.commit()
	conn.close()

	return