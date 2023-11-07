# API Musical

## Instalações
Para iniciar o projeto é preciso ter o Python e algumas bibliotecas instaladas
Certifique-se de ter o Python Instalado e execute o comando no terminal:
```
pip install -r requirements.txt
```

## O banco de dados
O banco de dados é construido em PostgreSQL e hospedado em uma instância RDS do tipo {editar}.

Para acessar a base de dados certifique-se de ter em mãos as credenciais corretas. Você pode utilizar softwares como `dbeaver` ou `beekeeper` para realizar consultas.

### A tabela "tiny_products"
A tabela de produtos é construida inicialmente com base nos produtos cadastrados na Tiny. Realizamos filtros e definimos que esta tabela conteria apenas algumas das features disponíveis na plataforma.

Para esta consulta foi utilizado o endpoint:
`https://api.tiny.com.br/api2/produto.obter.php`

### A tabela "tiny_stock"
Retorna todo estoque disponível e fornecido pela API Tiny.
Para esta consulta foi utilizado o endpoint:
`https://api.tiny.com.br/api2/produto.obter.estoque.php`
