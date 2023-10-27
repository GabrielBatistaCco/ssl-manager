CREATE DATABASE auto_inst;

CREATE TABLE `auto_inst`.`usuarios` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nome` varchar(150) NOT NULL,
  `data_cadastro` datetime NOT NULL,
  `ultimo_login` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `auto_inst`.`usuarios` (nome, data_cadastro, ultimo_login) VALUES ('Teste', NOW(), NOW());

CREATE TABLE `auto_inst`.`ssl_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `id_usuario` int(11) DEFAULT NULL,
  `dominio` varchar(80) DEFAULT NULL,
  `data_ativacao` datetime NOT NULL,
  `data_validade` datetime NOT NULL,
  `tipo` enum('Novo','Reativado','Reaproveitado','LetsEncrypt','Cliente') NOT NULL,
  `url_ssls` varchar(120),
  `produto` enum('IXCProvedor','IXCFranquia','SpeedTest','Cliente') NOT NULL,
  `obs` varchar(500),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

