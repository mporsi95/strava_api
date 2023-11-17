use db_strava;

drop table atletas;

create table atletas (
	id int,
    username varchar(255),
    estado_recurso int,
    nome varchar(255),
    biografia varchar(255),
    cidade varchar(255),
    estado varchar(255),
    pais varchar(255),
    sexo varchar(255),
    peso float,
    link_foto varchar(255),
    nu_seguidores int,
	nu_amigos int,
    pref_data varchar(255),
    pref_medidas varchar(255),
    ftp float,
    dh_criacao_perfil datetime,
    dh_atualizacao_perfil datetime,
    dh_ingestao datetime
);

select * from atletas;

alter table atletas rename column tkn_acesso_perfil to tkn_acesso_profile ;

truncate table atletas;

select * from atletas


