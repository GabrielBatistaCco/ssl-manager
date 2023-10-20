<?php
require_once 'inicia.php';

$id= isset ($_POST['id']) ? $_POST['id'] : null;
$produto = isset($_POST['produto'])?$_POST['produto'] : null;
$dominio = isset($_POST['dominio'])?$_POST['dominio'] : null;
// $data_ativacao = isset($_POST['data_ativacao'])?$_POST['data_ativacao'] : null;
// $data_validade = isset($_POST['data_validade'])?$_POST['data_validade'] : null;
$tipo = isset($_POST['tipo'])?$_POST['tipo'] : null;
$id_usuario = isset($_POST['id_usuario'])?$_POST['id_usuario'] : null;
// $preventivo = isset($_POST['preventivo'])?$_POST['preventivo'] : null;
$url_ssls = isset($_POST['url_ssls'])?$_POST['url_ssls'] : null;
$obs = isset($_POST['obs'])?$_POST['obs'] : null;

if(empty('produto')||empty('dominio')||empty('tipo')||empty('id_usuario')){
    echo 'Por favor preencha todos os campos do cadastro e tente novamente';
    exit;
}

$PDO = conecta_bd();
$sql=("UPDATE ssl_list SET produto=:produto,dominio=:dominio,tipo=:tipo,id_usuario=:id_usuario,url_ssls=:url_ssls,obs=:obs WHERE id=:id");
$stmt = $PDO->prepare($sql);
$stmt -> bindParam(':id', $id, PDO::PARAM_INT);
$stmt ->bindParam(':produto',$produto);
$stmt ->bindParam(':dominio',$dominio);
// $stmt ->bindParam(':data_ativacao',$data_ativacao);
// $stmt ->bindParam(':data_validade',$data_validade);
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
    echo "Falha ao atualizar cadastro!";
    print_r($stmt->errorInfo());
}

?>