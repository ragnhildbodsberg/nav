# Slette alle tabeller
DROP TABLE swportvlan;
DROP TABLE swport;
DROP TABLE gwport;

DROP TABLE boksinfo;
DROP TABLE boks;

DROP TABLE type;
DROP TABLE prefiks;
DROP TABLE rom;
DROP TABLE sted;
DROP TABLE anv;
DROP TABLE org;

DROP TABLE vpBoksXY;
DROP TABLE vpBoksGrp;
DROP TABLE vpBoksGrpInfo;

# Slette alle sekvenser
DROP SEQUENCE boks_boksid_seq;
DROP SEQUENCE boksinfo_boksinfoid_seq;
DROP SEQUENCE gwport_gwportid_seq;
DROP SEQUENCE prefiks_prefiksid_seq;
DROP SEQUENCE status_statusid_seq;
DROP SEQUENCE swport_swportid_seq;
DROP SEQUENCE swportvlan_swportvlanid_seq;

DROP SEQUENCE vpboksgrp_vpboksgrpid_seq;
DROP SEQUENCE vpboksgrpinfo_gruppeid_seq;
DROP SEQUENCE vpboksxy_vpboksxyid_seq;

# Slette alle indekser


# Definerer gruppe nav:
CREATE GROUP nav;

# Legger inn gartmann i nav:
ALTER GROUP nav add user gartmann;

# Fjerner gartmann fra nav:
ALTER GROUP nav drop user gartmann;


# org: descr fra 60 til 80
# boks: type ikke NOT NULL fordi ikke definert i nettel.txt

#community har blitt fjernet!
CREATE TABLE community (
  communityid SERIAL PRIMARY KEY,
  boksid INT4 NOT NULL REFERENCES boks ON UPDATE CASCADE ON DELETE CASCADE,
  ro CHAR(10),
  rw CHAR(10)
);

GRANT ALL ON community TO group nav;

#ro og rw g�r inn i boks
#tabellen type lagt til
#boks:sysname 20->30 dns er for lange for 20
#boks:type er ute av drift inntil bruk
#prefiks: vlan ikke NOT NULL
#prefiksid REFERENCES prefiks ikke boks overalt
#swport: lagt til port(nummer) og modul
#boksinfo:sysCon fra 30 til 40
#fremmedn�kler til prefiksid peker p� prefiks, ikke boks
#boksinfo:sysType CHAR(30):fjernet
#gwport og swport: speed endret til CHAR(10) for � kunne godta opptil 10 000 Tbps eller ned 0.000001 bps. (overkill?);
#alle char endret til varchar
#NOT NULL fjernet fra duplex i swport
#NOT NULL fjernet fra descr i rom
#############################################

CREATE TABLE org (
  orgid VARCHAR(10) PRIMARY KEY,
  forelder VARCHAR(10) REFERENCES org,
  descr VARCHAR(80),
  org2 VARCHAR(50),
  org3 VARCHAR(50),
  org4 VARCHAR(50)
);


CREATE TABLE anv (
  anvid VARCHAR(10) PRIMARY KEY,
  descr VARCHAR(20) NOT NULL
);


CREATE TABLE sted (
  sted VARCHAR(12) PRIMARY KEY,
  descr VARCHAR(60) NOT NULL
);

CREATE TABLE rom (
  romid VARCHAR(10) PRIMARY KEY,
  sted VARCHAR(12) REFERENCES sted,
  descr VARCHAR(50),
  rom2 VARCHAR(10),
  rom3 VARCHAR(10),
  rom4 VARCHAR(10),
  rom5 VARCHAR(10)
);


CREATE TABLE prefiks (
  prefiksid SERIAL PRIMARY KEY,
  nettadr VARCHAR(15) NOT NULL,
  maske VARCHAR(3) NOT NULL,
  vlan VARCHAR(4),
  nettype VARCHAR(10) NOT NULL,
  org VARCHAR(10) REFERENCES org,
  anv VARCHAR(10) REFERENCES anv,
  samband VARCHAR(20),
  komm VARCHAR(20)
);


CREATE TABLE type (
  type VARCHAR(10) PRIMARY KEY,
  typegruppe VARCHAR(10) NOT NULL,
  sysObjectID VARCHAR(30) NOT NULL,
  descr VARCHAR(60)
);


CREATE TABLE boks (
  boksid SERIAL PRIMARY KEY,
  ip VARCHAR(15) NOT NULL,
  romid VARCHAR(10) NOT NULL REFERENCES rom,
  type VARCHAR(10),
  sysName VARCHAR(30),
  kat VARCHAR(10) NOT NULL,
  kat2 VARCHAR(10),
  drifter VARCHAR(10) NOT NULL,
  ro VARCHAR(10),
  rw VARCHAR(10),
  prefiksid INT4 REFERENCES prefiks ON UPDATE CASCADE ON DELETE SET null,
  via2 integer REFERENCES boks ON UPDATE CASCADE ON DELETE SET null,
  via3 integer REFERENCES boks ON UPDATE CASCADE ON DELETE SET null,
  active BOOL DEFAULT true,
  static BOOL DEFAULT false,
  watch BOOL DEFAULT false,
  skygge BOOL DEFAULT false
);


CREATE TABLE boksinfo (
  boksid INT4 NOT NULL PRIMARY KEY REFERENCES boks ON UPDATE CASCADE ON DELETE CASCADE,
  software VARCHAR(13),
  sysLoc VARCHAR(50),
  sysCon VARCHAR(40),
  ais INT2,
  mem VARCHAR(10),
  flashMem VARCHAR(10),
  function VARCHAR(100),
  supVersion VARCHAR(10)
);



CREATE TABLE gwport (
  gwportid SERIAL PRIMARY KEY,
  boksid INT4 NOT NULL REFERENCES boks ON UPDATE CASCADE ON DELETE CASCADE,
  prefiksid INT4 REFERENCES prefiks ON UPDATE CASCADE ON DELETE SET null,
  indeks INT2 NOT NULL,
  interf VARCHAR(30) NOT NULL,
  gwip VARCHAR(15) NOT NULL,
  speed VARCHAR(10),
  antmask INT2,
  maxhosts INT2,
  ospf INT2,
  hsrppri VARCHAR(1),
  static BOOL DEFAULT false
);


CREATE TABLE swport (
  swportid SERIAL PRIMARY KEY,
  boksid INT4 NOT NULL REFERENCES boks ON UPDATE CASCADE ON DELETE CASCADE,
  ifindex INT2 NOT NULL,
  status VARCHAR(4) NOT NULL DEFAULT 'down',
  speed VARCHAR(10),
  duplex VARCHAR(4),
  trunk BOOL DEFAULT false,
  static BOOL DEFAULT false,
  modul VARCHAR(4) NOT NULL,
  port INT2 NOT NULL,
  portnavn VARCHAR(30),
  boksbak INT2 REFERENCES boks ON UPDATE CASCADE ON DELETE SET null
);


CREATE TABLE swportvlan (
  swportvlanid SERIAL PRIMARY KEY,
  swportid INT4 NOT NULL REFERENCES swport ON UPDATE CASCADE ON DELETE CASCADE,
  vlan INT2 NOT NULL,
  retning VARCHAR(1) NOT NULL DEFAULT 'x'
);


### vlanPlot tabeller ###
CREATE TABLE vpBoksGrpInfo (
  gruppeid SERIAL PRIMARY KEY,              
  name VARCHAR(16) NOT NULL
);
# Default nett
INSERT INTO vpboksgrpinfo (gruppeid,name) VALUES (0,'Bynett');
INSERT INTO vpboksgrpinfo (name) VALUES ('Kjernenett');
INSERT INTO vpboksgrpinfo (name) VALUES ('Testnett');

CREATE TABLE vpBoksGrp (
  vpBoksGrpId SERIAL PRIMARY KEY,
  gruppeid INT4 REFERENCES vpBoksGrpInfo ON UPDATE CASCADE ON DELETE CASCADE,
  pboksid INT4 NOT NULL,
  UNIQUE(gruppeid, pboksid)
);

CREATE TABLE vpBoksXY (
  vpBoksXYId SERIAL PRIMARY KEY, 
  pboksid INT4 NOT NULL,
  x INT2 NOT NULL,
  y INT2 NOT NULL,
  gruppeid INT4 NOT NULL REFERENCES vpBoksGrpInfo ON UPDATE CASCADE ON DELETE CASCADE,
  UNIQUE(pboksid, gruppeid)
);
### vlanPlot end ###

GRANT ALL ON org TO group nav;
GRANT ALL ON anv TO group nav;
GRANT ALL ON sted TO group nav;
GRANT ALL ON rom TO group nav;
GRANT ALL ON prefiks TO group nav;
GRANT ALL ON type TO group nav;
GRANT ALL ON boks TO group nav;
GRANT ALL ON boksinfo TO group nav;
GRANT ALL ON gwport TO group nav;
GRANT ALL ON swport TO group nav;
GRANT ALL ON swportvlan TO group nav;



GRANT ALL ON boks_id_seq TO group nav;
GRANT ALL ON boksinfo_id_seq TO group nav;
GRANT ALL ON gwport_id_seq TO group nav;
GRANT ALL ON prefiks_id_seq TO group nav;
GRANT ALL ON swport_id_seq TO group nav;
GRANT ALL ON swportvlan_id_seq TO group nav;

################################


