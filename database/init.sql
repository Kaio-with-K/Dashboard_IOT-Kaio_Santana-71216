-- Criação da tabela
CREATE TABLE IF NOT EXISTS temperaturas (
    modelo VARCHAR(10),
    data_registro TIMESTAMP,
    temperatura INT,
    direcao VARCHAR(10)
);

-- View 1: Temperaturas por modelo
CREATE OR REPLACE VIEW vw_temperaturas_por_modelo AS
SELECT modelo, data_registro, temperatura, direcao
FROM temperaturas;

-- View 2: Média geral
CREATE OR REPLACE VIEW vw_media_temperatura_por_modelo AS
SELECT 'Média de temperaturas' AS modelo, ROUND(AVG(temperatura)) AS media_de_temperaturas
FROM temperaturas;

-- View 3: Temperatura mínima
CREATE OR REPLACE VIEW vw_min_temp_por_modelo AS
SELECT modelo, MIN(temperatura) AS menor_temperatura
FROM temperaturas
GROUP BY modelo
ORDER BY menor_temperatura ASC
LIMIT 1;

-- View 4: Temperatura máxima
CREATE OR REPLACE VIEW vw_max_temp_por_modelo AS
SELECT modelo, MAX(temperatura) AS maior_temperatura
FROM temperaturas
GROUP BY modelo
ORDER BY maior_temperatura DESC
LIMIT 1;