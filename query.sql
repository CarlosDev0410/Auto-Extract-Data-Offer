SELECT
    l.nome AS LOCAL_ESTOQUE,
    m.identificacao AS SKU,
    m.nome AS MATERIAL,
    -- Somamos o estoque e aplicamos a trava de negativo após a soma
    GREATEST(SUM(COALESCE(v.qtdedisponivel, 0)), 0) AS QTDE,
    m.valorvendaminimo AS CUSTO,
    m.precovendafantasia / 100 AS PRECO_DE,
    m.valorvenda AS PRECO_POR
FROM 
    material m
    LEFT JOIN ecommaterial e ON m.cdmaterial = e.cdmaterial
    LEFT JOIN vgerenciarmaterial v ON m.cdmaterial = v.cdmaterial 
    LEFT JOIN localarmazenagem l ON v.cdlocalarmazenagem = l.cdlocalarmazenagem 
WHERE
    m.produto = true
    AND m.ativo = true
    AND m.ecommerce = true
    AND l.cdlocalarmazenagem IN (34, 67, 397, 265, 506, 507)
GROUP BY
    l.nome, 
    m.identificacao, 
    m.nome, 
    m.valorvendaminimo, 
    m.precovendafantasia, 
    m.valorvenda
ORDER BY 
    l.nome ASC,
    m.nome ASC;