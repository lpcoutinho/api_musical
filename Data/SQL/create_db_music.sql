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
  "updated_at" timestamp
);

CREATE TABLE "tiny_stock" (
  "tiny_id" int,
  "nome" varchar(150),
  "sku_tiny" varchar(30),
  "unidade" varchar(10),
  "saldo_reservado" decimal,
  "deposito_nome" varchar(150),
  "deposito_desconsiderar" varchar(1),
  "deposito_saldo" decimal,
  "deposito_empresa" varchar(150),
  "created_at" timestamp DEFAULT (now() at time zone 'utc'),
  "updated_at" timestamp
);

CREATE TABLE "tiny_ml_codes" (
  "tiny_id" int,
  "ml_inventory_id" varchar(30),
  "created_at" timestamp DEFAULT (now() at time zone 'utc'),
  "updated_at" timestamp
);

CREATE TABLE "ml_fulfillment" (
  "tiny_id" int,
  "ml_inventory_id" varchar(30),
  "item_id" varchar(30),
  "type" varchar(30),
  "total" int,
  "available_quantity" int,
  "not_available_quantity" int,
  "created_at" timestamp DEFAULT (now() at time zone 'utc'),
  "updated_at" timestamp
);

ALTER TABLE "tiny_stock" ADD FOREIGN KEY ("tiny_id") REFERENCES "tiny_products" ("tiny_id");

ALTER TABLE "tiny_ml_codes" ADD FOREIGN KEY ("tiny_id") REFERENCES "tiny_products" ("tiny_id");

ALTER TABLE "tiny_ml_codes" ADD CONSTRAINT unique_ml_tiny_combination UNIQUE ("ml_inventory_id", "tiny_id");

ALTER TABLE "tiny_ml_codes" ADD CONSTRAINT unique_ml_inventory_id UNIQUE ("ml_inventory_id");

ALTER TABLE "ml_fulfillment" ADD FOREIGN KEY ("tiny_id") REFERENCES "tiny_products" ("tiny_id");

ALTER TABLE "ml_fulfillment" ADD FOREIGN KEY ("ml_inventory_id") REFERENCES "tiny_ml_codes" ("ml_inventory_id");

