<?php
    require_once 'inicia.php';
    $produto = isset($_POST['produto'])?$_POST['produto'] : null;
    $dominio = isset($_POST['dominio'])?$_POST['dominio'] : null;
    $data_ativacao = isset($_POST['data_ativacao'])?$_POST['data_ativacao'] : null;
    $data_validade = isset($_POST['data_validade'])?$_POST['data_validade'] : null;
    $tipo = isset($_POST['tipo'])?$_POST['tipo'] : null;
    $id_usuario = isset($_POST['id_usuario'])?$_POST['id_usuario'] : null;
    $preventivo = isset($_POST['preventivo'])?$_POST['preventivo'] : null;
    $url_ssls = isset($_POST['url_ssls'])?$_POST['url_ssls'] : null;
    $obs = isset($_POST['obs'])?$_POST['obs'] : null;

    if(empty('produto')||empty('dominio')||empty('data_ativacao')||empty('tipo')||empty('id_usuario')){
        echo 'Por favor preencha todos os campos do cadastro e tente novamente';
        exit;
    }

    // Converte formato de data para inserção no banco de dados
    $dataAtivacao = date_create($data_ativacao)->format('Y-m-d H:i:s');
    $dataValidade = date_create($data_validade)->format('Y-m-d H:i:s');

    $PDO = conecta_bd();
    $sql = "INSERT INTO ssl_list(produto,dominio,data_ativacao,data_validade,tipo,id_usuario,url_ssls,obs) VALUES(:produto,:dominio,:data_ativacao,:data_validade,:tipo,:id_usuario,:url_ssls,:obs)";
    $stmt = $PDO->prepare($sql);
    $stmt ->bindParam(':produto',$produto);
    $stmt ->bindParam(':dominio',$dominio);
    $stmt ->bindParam(':data_ativacao',$dataAtivacao);
    $stmt ->bindParam(':data_validade',$dataValidade);
    $stmt ->bindParam(':tipo',$tipo);
    $stmt ->bindParam(':id_usuario',$id_usuario);
    // $stmt ->bindParam(':preventivo',$preventivo);
    $stmt ->bindParam(':url_ssls',$url_ssls);
    $stmt ->bindParam(':obs',$obs);

    if ($stmt->execute()){
        require_once 'verifica_ssl.php';
        header('Location: index.php');
    }
    else{
        echo "ocoreu um erro na inclusão o registro";
        print_r($stmt->errorInfo());
    }
?>