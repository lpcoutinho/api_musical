CREATE TABLE "tiny_products" (
  "tiny_id" int PRIMARY KEY,
  "data_criacao" varchar(19),
  "nome" varchar(150),
  "sku_tiny" varchar(30),
  "unidade" varchar(10),
  "preco" decimal,
  "ncm" varchar(10),
  "origem" varchar(1),
  "gtin" varchar(14),
  "peso_bruto" decimal DEFAULT null,
  "estoque_minimo" decimal DEFAULT null,
  "estoque_maximo" decimal DEFAULT null,
  "id_fornecedor" int,
  "nome_fornecedor" varchar(150),
  "codigo_pelo_fornecedor" varchar(20),
  "preco_custo" decimal,
  "preco_custo_medio" decimal,
  "situacao" varchar(1),
  "tipo" varchar(1),
  "cest" varchar(9),
  "marca" varchar(150),
  "tipo_embalagem" int,
  "altura_embalagem" decimal,
  "comprimento_embalagem" decimal,
  "largura_embalagem" decimal,
  "diametro_embalagem" decimal,
  "qtd_volumes" decimal,
  "categoria" varchar(255),
  "created_at" timestamp DEFAULT (now() at time zone 'utc'),
  "updated_at" timestamp DEFAULT (now() at time zone 'utc')
);


CREATE TABLE "tiny_stock" (
  "tiny_id" int,
  "nome" varchar(150),
  "sku_tiny" varchar(30),
  "unidade" varchar(10),
  "saldo_reservado" decimal,
  "deposito.nome" varchar(150),
  "deposito.desconsiderar" varchar(1),
  "deposito.saldo" decimal,
  "deposito.empresa" varchar(150),
  "created_at" timestamp DEFAULT (now() at time zone 'utc'),
  "updated_at" timestamp DEFAULT (now() at time zone 'utc')
); 

ALTER TABLE "tiny_stock" ADD FOREIGN KEY ("tiny_id") REFERENCES "tiny_products" ("tiny_id");