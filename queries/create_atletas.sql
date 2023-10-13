use db_strava;

create table atletas (
	id varchar(255),
    username varchar(255),
    estado_recurso int,
    nome varchar(255),
    biografia varchar(255),
    cidade varchar(255),
    estado varchar(255),
    pais varchar(255),
    sexo varchar(255),
    dh_criacao datetime,
    dh_atualizacao datetime,
    peso float,
    link_foto varchar(255),
    bloqueado boolean,
    nu_seguidores int,
	nu_amigos int,
    pref_data varchar(255),
    pref_medidas varchar(255),
    ftp float,
    tkn_acesso_perfil varchar(255),
    tkn_acesso_atividade varchar(255)
);

select * from atletas;

alter table atletas rename column tkn_acesso_perfil to tkn_acesso_profile ;

truncate table atletas;

select * from atletas


