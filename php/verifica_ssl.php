<?php

function varifica_registro_dominio($dominio){
    if (checkdnsrr($dominio, 'ANY') && gethostbyname($dominio) != $dominio){
        // Retorna true se o domínio estiver registrado
        return true;
    } else {
        // Retorna false se o domínio NÃO estiver registrado
        return false;
    }
}

require 'inicia.php';

if (!isset($id)){
    if (isset($_GET['id'])){
        $id=(int) $_GET['id'];
    } else { 
        $stmt = $PDO->prepare('SELECT id FROM ssl_list WHERE dominio=:dominio;');
        $stmt ->bindParam(':dominio',$dominio);
        $stmt->execute();
        $resultado = $stmt->fetch(PDO::FETCH_ASSOC);
        $id = $resultado['id'];
    }
}

if(empty($id)){
    echo 'Codigo do cliente não definido!';
    exit;
}

$PDO = conecta_bd();
$stmt = $PDO->prepare("SELECT dominio FROM ssl_list WHERE id=:id");
$stmt -> bindParam(':id', $id, PDO::PARAM_INT);
$stmt -> execute();
$resultado =$stmt->fetch(PDO::FETCH_ASSOC);
if(!is_array($resultado)){
    echo 'Registro não encontrado!';
    exit;
}

if (varifica_registro_dominio($resultado['dominio'])){

    // $url = "https://".$resultado['dominio'];
    // $orignal_parse = parse_url($url, PHP_URL_HOST);
    $get = stream_context_create(array("ssl" => [
        'allow_self_signed' => true,
        'verify_peer' => false,
        'verify_peer_name' => false,
        'capture_peer_cert' => true]));
    $read = stream_socket_client(
        "ssl://".$resultado['dominio'].":443",
        $errno,
        $errstr,
        10,
        STREAM_CLIENT_ASYNC_CONNECT,
        $get);
    if ($read){
        $cert = stream_context_get_params($read);
        $certinfo = openssl_x509_parse($cert['options']['ssl']['peer_certificate']);

        // Convercao datas de ativacao e validade
        $dtA = DateTime::createFromFormat('ymdHise', $certinfo['validFrom']);
        $dtV = DateTime::createFromFormat('ymdHise', $certinfo['validTo']);
        $data_ativacao = $dtA->format('Y-m-d H:i:s');
        $data_validade = $dtV->format('Y-m-d H:i:s');

        $PDO = conecta_bd();
        $sql=("UPDATE ssl_list SET data_ativacao=:data_ativacao,data_validade=:data_validade WHERE id=:id");
        $stmt = $PDO->prepare($sql);
        $stmt -> bindParam(':id', $id, PDO::PARAM_INT);
        $stmt ->bindParam(':data_ativacao',$data_ativacao);
        $stmt ->bindParam(':data_validade',$data_validade);

        if ($stmt->execute()){
            header('Location: index.php');
        }
    }
    // echo "Dominio: $dominio\nAtivacao: $data_ativacao\nValidade: $data_validade\n";

} else {
    echo "Domínio \"$dominio\" não está registrado!\n";
}


