<?php
	$usuario = $_POST['usuario'];
    $contrasenha = $_POST['contrasenha'];
    session_start();
	
	
	$conn_string = "dbname=hipsdb user='$usuario' password='$contrasenha'";
	$dbconn = pg_connect($conn_string);

	if (!$dbconn){
		echo "Error. No se pudo conectar la base de datos ";
		include("index.php");
        $_SESSION['INCORRECT'] = 1;

		exit;
	}else{
		echo "Conexión exitosa.";
        $_SESSION['usuario'] = $usuario;
		$_SESSION['CONN'] = $conn_string;
		unset($_SESSION['INCORRECT']);
		pg_close($dbconn);
		header("Location: ingreso.php");
	}
?>
