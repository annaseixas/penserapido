create database pense_rapido;
use pense_rapido;

create table perguntas (
id INT AUTO_INCREMENT PRIMARY KEY,
pergunta VARCHAR(512),
resposta text not null,
categoria varchar(255)
);

delete from perguntas where id = 1;

insert into perguntas (pergunta, resposta, categoria)
values ("Qual comando atualiza os dados em uma tabela?", "UPDATE","Banco de Dados");

select * from perguntas;
alter table perguntas modify categoria varchar(255) not null;


alter table perguntas add categoria varchar(255) not null;
describe perguntas;
