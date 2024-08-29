-- Candidatos a prefeitura de João Pessoa
SELECT NM_CANDIDATO, NR_CANDIDATO, SG_PARTIDO, DS_GRAU_INSTRUCAO, DS_OCUPACAO FROM tb_candidaturas
WHERE NM_UE = 'JOÃO PESSOA' AND (DS_CARGO='PREFEITO' OR DS_CARGO='VICE-PREFEITO');


-- Ver a representatividade dentro dos partidos, tentando verificar aqueles mais progressitas.
with tb_candidates_jp as (
	select SQ_CANDIDATO,
		SG_UF,
		DS_CARGO,	
		SG_PARTIDO,
		NM_PARTIDO,
		DT_NASCIMENTO,
		DS_GENERO,
		DS_GRAU_INSTRUCAO,
		DS_COR_RACA,
		DS_OCUPACAO,
		NM_UE,
		NM_CANDIDATO
	from tb_candidaturas 
	where NM_UE = 'JOÃO PESSOA'
),
tb_total_bem_candidates_jp as (
select SQ_CANDIDATO,
	sum(cast(replace(VR_BEM_CANDIDATO,',', '.') as DECIMAL(15,2))) as total_bens
from tb_bens tb 
group by 1
)

select t1.*, COALESCE(t2.total_bens, 0) as total_bens
from tb_candidates_jp as t1
left join tb_total_bem_candidates_jp as t2
on t1.SQ_CANDIDATO = t2.SQ_CANDIDATO;
