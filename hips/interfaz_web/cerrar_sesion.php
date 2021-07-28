<?php
session_start();
if(isset($_SESSION['usuario']) && !empty($_SESSION['usuario'])&&isset($_POST['cerrar_sesion'])){
	unset($_SESSION['CONN']);
	unset($_SESSION['usuario']);
	unset($_POST['cerrar_sesion']);
	session_destroy();
}
header("Location: index.php");
?>