<?php
    require 'inicia.php';
    $id= isset ($_GET['id']) ? (int) $_GET['id'] : null;
    if(empty($id)){
        echo 'ID SSL não informado!';
        exit;  
    }
    $PDO = conecta_bd();
    $stmt = $PDO->prepare("SELECT * FROM ssl_list WHERE id=:id");
    $stmt -> bindParam(':id', $id, PDO::PARAM_INT);
    $stmt -> execute();
    $resultado =$stmt->fetch(PDO::FETCH_ASSOC);
    if(!is_array($resultado)){
        echo 'Cadastro não encontrado!';
        exit;
    }
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
        <h1>Alteração de cadastros</h1>
        <div class="main">
            <form action="altera.php" method="POST">
                <div>
                    <label for="id">ID: </label><br>
                    <input type="text" name="id" value="<?=$resultado['id'] ?>" readonly />
                </div>
                <div>
                    <label for='produto'>Produto: </label><br>            
                    <select name="produto" required value="<?=$resultado['produto'] ?>">
                        <option selected>---</option>
                        <option value="IXCProvedor">IXCProvedor</option>
                        <option value="SpeedTest">SpeedTest</option>
                        <option value="IXCFranquia">IXCFranquia</option>
                    </select>
                </div>
                <div>
                    <label for='dominio'>Dominio: </label><br>
                    <input type='text' name='dominio' required value="<?=$resultado['dominio'] ?>"/>
                </div>
                <!-- <div>
                    <label for="data_ativacao">Data de ativação: </label><br>
                    <input type='date' name='data_ativacao' value="<?=$resultado['data_ativacao'] ?>" required/>
                </div>
                <div>
                    <label for="data_validade">Data de validade: </label><br>
                    <input type='date' name='data_validade' value="<?=$resultado['data_validade'] ?>"/>
                </div> -->
                <div>
                    <label for='tipo'>Tipo: </label><br>
                    <select name="tipo" required value="<?=$resultado['tipo']?>">
                        <option selected>---</option>
                        <option value="Novo">Novo</option>
                        <option value="Reativado">Reativado</option>
                        <option value="Reaproveitado">Reaproveitado</option>
                        <option value="LetsEncrypt">Let's Encrypt</option>
                        <option value="Cliente">SSL cliente</option>
                    </select>
                </div>
                <div>
                    <label for='id_usuario'>Tecnico: </label><br>
                    <select name="id_usuario" required value="<?=$resultado['id_usuario'] ?>">
                        <option value="1" selected>Teste</option>
                        <option value="1">Teste</option>
                    </select>
                </div>
                <div>
                    <label for='preventivo'>Preventivo: </label><br>
                    <input type='checkbox' name='preventivo' value="<?=$resultado['preventivo'] ?>"/>
                </div>
                <div>
                    <label for='url_ssls'>URL: </label><br>
                    <input type='text' name='url_ssls' placeholder="Link SSL" value="<?=$resultado['url_ssls'] ?>"/>
                </div>
                <div>
                    <label for='obs'>OBS: </label><br>
                    <input type='text' name='obs' value="<?=$resultado['obs'] ?>"/>
                </div>
                <div>
                    <input type="submit" class="third" value="Alterar"/>
                </div>
            </form>
        </div>
        <div>
            <a href="index.php"><button class="third">Visualizar cadastros</button></a>
        </div>
    </body>
</html>
