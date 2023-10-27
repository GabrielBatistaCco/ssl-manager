<?php
    require_once 'inicia.php';
    $id = isset ($_GET['id']) ?$_GET['id'] : null;
    if(empty($id)){
        echo 'ID não definido para alteração';
        exit;
    }

    $PDO = conecta_bd();
    $sql = "DELETE FROM ssl_list WHERE id=:id";
    $stmt = $PDO->prepare($sql);
    $stmt -> bindParam(':id', $id, PDO::PARAM_INT);
    if ($stmt->execute()){
        header('Location: index.php');
    }
    else{
        echo "Falha ao excluir registro!";
        print_r($stmt->errorInfo());
    }
?>