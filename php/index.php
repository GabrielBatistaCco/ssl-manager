<?php
    require_once 'inicia.php';
    $PDO = conecta_bd();
?>
<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="./estilizacoes.css"/>
        <title>SSL Instalação</title>
    </head>
    <body>
        <h1>Tabela de cadastros</h1>
        <?php
            $stmt_count=$PDO->prepare('SELECT COUNT(*) AS total FROM ssl_list');
            $stmt_count->execute();
            $stmt = $PDO->prepare('SELECT * FROM ssl_list ORDER BY id;');
            $stmt->execute();
            $total = $stmt_count->fetchColumn();
            if($total>0):
        ?>
            <div>
                <table border = 1>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Produto</th>
                            <th>Domínio</th>
                            <!-- <th>Data ativação</th> -->
                            <th>Tipo</th>
                            <th>Técnico</th>
                            <!-- <th>Preventivo</th> -->
                            <th>Validade SSL</th>
                            <th>SSLS</th>
                            <!-- <th>OBS</th> -->
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        while($resultado = $stmt->fetch(PDO::FETCH_ASSOC)):
                            $dataAtivacao = date_create($resultado['data_ativacao']);
                            $dataValidade = date_create($resultado['data_validade']);
                        ?>
                        <tr>
                            <td><?php echo $resultado['id']?></td>
                            <td><?php echo $resultado['produto']?></td>
                            <td>
                                <?php
                                    echo "<a href='https://".$resultado['dominio']."/adm.php' target='_BLANK'\>".$resultado['dominio']."</a>";
                                ?>
                            <!-- <td><?php echo $dataAtivacao->format('d/m/Y H:i:s')?></td> -->
                            <td><?php echo $resultado['tipo']?></td>
                            <td><?php echo $resultado['id_usuario']?></td>
                            <!-- <td><?php echo $resultado['preventivo']?></td> -->
                            <td><?php echo $dataValidade->format('d/m/Y H:i:s')?></td>
                            <td>
                                <?php
                                    if ($resultado['tipo']=='LetsEncrypt'){
                                        echo "";
                                    } else if (!empty($resultado['url_ssls'])) {
                                        echo "<a href=".$resultado['url_ssls']." target='_BLANK'>Acessar</a>";
                                    } else {
                                        echo "<a href=''>Acessar</a>";
                                    }
                                ?>
                            </td>
                            <!-- <td><?php echo $resultado['obs']?></td> -->
                            <td><a href="form_altera.php?id=<?php echo $resultado['id']?>"><button id="b1">Alterar</button></a>
                            <!-- <a href="verifica_ssl.php?id=<?php echo $resultado['id']?>"><button id="b1">Atualizar</button></a> -->
                            <a href="exclui.php?id=<?php echo $resultado['id']?>" onclick="return confirm('tem certeza que deseja deletar o registro?');"><button id="b2">Excluir</button></a>
                            </td>
                        </tr>
                        <?php endwhile;?>
                    </tbody>
                </table>
            </div>
            <div>
                <p>Total de cadastros: <?php echo $total ?></p>
            </div>
            <?php else: ?>
            <div>
                <p>Não ha SSLs cadastrados</p>
            </div>
            <?php endif; ?>
            <div>
                <a href="form_incluir.php"><button class="third">Cadastrar novo SSL</button></a>
            </div>
    </body>
</html>