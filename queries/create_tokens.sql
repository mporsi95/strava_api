use db_strava;

drop table tokens;

create table tokens (
	id_atleta int,
    tkn_acesso_perfil varchar(255),
    dh_expiracao_tkn_perfil datetime,
    tkn_acesso_atividade varchar(255),
    dh_expiracao_tkn_atividade datetime,
    tkn_atualizacao varchar(255)
);
