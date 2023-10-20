<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SSL Instalação</title>
        <link rel="stylesheet" href="./estilizacoes.css"/>
    </head>
    <body>
        <h1>Cadatro de novo usuario</h1>
        <div class="main">
            <form method="POST" action="incluir.php">
                <div>
                    <label for='produto'>Produto: </label><br>            
                    <select name="produto" required>
                        <option selected>---</option>
                        <option value="IXCProvedor">IXCProvedor</option>
                        <option value="SpeedTest">SpeedTest</option>
                        <option value="IXCFranquia">IXCFranquia</option>
                    </select>
                </div>
                <div>
                    <label for='dominio'>Dominio: </label><br>
                    <input type='text' name='dominio' required placeholder="dominio.com"/>
                </div>
                <!-- <div>
                    <label for="data_ativacao">Data de ativação: </label><br>
                    <input type='date' name='data_ativacao' required/>
                </div>
                <div>
                    <label for="data_validade">Data de validade: </label><br>
                    <input type='date' name='data_validade'/>
                </div> -->
                <div>
                    <label for='tipo'>Tipo: </label><br>
                    <select name="tipo" required>
                        <option selected>---</option>
                        <option value="Novo">Novo</option>
                        <option value="Reativado">Reativado</option>
                        <option value="Reaproveitado">Reaproveitado</option>
                        <option value="LetsEncrypt">Let's Encrypt</option>
                        <option value="Cliente">SSL cliente</option>
                    </select>
                </div>
                <div>
                    <label for='id_usuario'>Id usuário: </label><br>
                    <select name="id_usuario" required>
                        <option value="1" selected>Teste</option>
                        <option value="1">Teste</option>
                    </select>
                </div>
                <div>
                    <label for='preventivo'>Preventivo: </label><br>
                    <input type='checkbox' name='preventivo'/>
                </div>
                <div>
                    <label for='url_ssls'>URL: </label><br>
                    <input type='text' name='url_ssls' placeholder="Link SSL"/>
                </div>
                <div>
                    <label for='obs'>OBS: </label><br>
                    <input type='text' name='obs' placeholder="OBS"/>
                </div>
                <div>
                    <input type="submit" class="third"/>
                </div>
            </form>
        </div>
        <div>
            <a href="index.php"><button class="third">Visualizar cadastros</button></a>
        </div>
    </body>
</html>
