CREATE DATABASE IF NOT EXISTS db_pedidos;

USE db_pedidos;

-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS tb_clientes (
    cli_id INT AUTO_INCREMENT PRIMARY KEY,
    cli_nome VARCHAR(100) NOT NULL,
    cli_email VARCHAR(255) NOT NULL UNIQUE,
    cli_telefone VARCHAR(15) NOT NULL,
    cli_endereco TEXT NOT NULL
);

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS tb_produtos (
    pro_id INT AUTO_INCREMENT PRIMARY KEY,
    pro_nome VARCHAR(200) NOT NULL,
    pro_desc TEXT NOT NULL,
    pro_quantidade INT NOT NULL,
    pro_preco DECIMAL(10,2) NOT NULL
);

-- Tabela de Pedidos (corrigida)
CREATE TABLE IF NOT EXISTS tb_pedidos (
    ped_id INT AUTO_INCREMENT PRIMARY KEY,
    ped_cli_id INT NOT NULL, -- A coluna foi renomeada para ped_cli_id
    ped_data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ped_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ped_cli_id) REFERENCES tb_clientes(cli_id) ON DELETE CASCADE
);

-- Tabela de Produtos por Pedido
CREATE TABLE IF NOT EXISTS tb_proPed (
    proPed_id INT AUTO_INCREMENT PRIMARY KEY,
    proPed_ped_id INT NOT NULL,
    proPed_pro_id INT NOT NULL,
    proPed_qdproduto INT NOT NULL,
    proPed_subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (proPed_ped_id) REFERENCES tb_pedidos(ped_id),
    FOREIGN KEY (proPed_pro_id) REFERENCES tb_produtos(pro_id)
);

CREATE TABLE IF NOT EXISTS tb_usuarios(
    usu_id INT AUTO_INCREMENT PRIMARY KEY,
    usu_nome VARCHAR(150) NOT NULL,
    usu_email VARCHAR(150) NOT NULL,
    usu_senha VARCHAR(500) NOT NULL
);
