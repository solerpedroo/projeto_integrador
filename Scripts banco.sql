show databases;

CREATE database ProjetoSustentabilidade;

USE ProjetoSustentabilidade;

show tables;

SELECT * FROM projetodesustentabilidade;

CREATE TABLE ProjetoDeSustentabilidade( 
  ID INT PRIMARY KEY AUTO_INCREMENT,
  DataEntrada DATE,
  LitrosConsumidos VARCHAR (50),
  KWHConsumido VARCHAR (50), 
  KgNaoReciclaveis VARCHAR (50), 
  PorcentagemResiduos VARCHAR (50), 
  MeioDeTransporte VARCHAR (50)
  );
