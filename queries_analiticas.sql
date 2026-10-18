SELECT 
    dt_posicao,
    vl_taxa_selic,
    ROUND(
        AVG(vl_taxa_selic) OVER (
            ORDER BY dt_posicao 
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        )::numeric, 
        2
    ) AS media_movel_12m
FROM tb_taxa_selic
ORDER BY dt_posicao DESC;

SELECT 
    dt_posicao,
    vl_taxa_selic AS selic_atual,
    LAG(vl_taxa_selic, 1) OVER (ORDER BY dt_posicao) AS selic_mes_anterior,
    ROUND(
        (vl_taxa_selic - LAG(vl_taxa_selic, 1) OVER (ORDER BY dt_posicao))::numeric, 
        2
    ) AS variacao_absoluta
FROM tb_taxa_selic
ORDER BY dt_posicao DESC;

WITH selic_ranqueada AS (
    SELECT 
        EXTRACT(YEAR FROM dt_posicao) AS ano_referencia,
        dt_posicao,
        vl_taxa_selic,
        DENSE_RANK() OVER (
            PARTITION BY EXTRACT(YEAR FROM dt_posicao) 
            ORDER BY vl_taxa_selic DESC
        ) AS rank_no_ano
    FROM tb_taxa_selic
)
SELECT 
    ano_referencia,
    dt_posicao,
    vl_taxa_selic AS maior_taxa_do_ano
FROM selic_ranqueada
WHERE rank_no_ano = 1
ORDER BY ano_referencia DESC;