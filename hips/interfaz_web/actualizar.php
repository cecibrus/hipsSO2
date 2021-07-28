<?php
	session_start();
	if(isset($_SESSION['usuario']) && !empty($_SESSION['usuario'])){
		$dbconn = pg_connect($_SESSION['CONN']);
		if (!$dbconn){
			echo "no se conecta";
			exit;
		}
	}
	$query = '';
	$result = '';
	if(isset($_POST['addUsuarioRegistro'])){
		$nombre_usuario = $_POST['nombre_usuario'];
		$ip_permitida = $_POST['ip_permitida'];
		$dias_permitidos = $_POST['dias_permitidos'];
		$rango_horario_permitido = $_POST['rango_horario_permitido'];

		$query = "INSERT INTO usuario_registro(nombre_usuario, ip_permitida, dias_permitidos, rango_horario_permitido) VALUES ('$nombre_usuario','$ip_permitida','$dias_permitidos','$rango_horario_permitido');";
		unset($_POST['addUsuarioRegistro']);
		echo "Nuevo usuario registrado";

	}elseif(isset($_POST['addCron'])){
		$restriccion = $_POST['restriccion'];
		$config_cron = $_POST['config_cron'];
		$comando = $_POST['comando'];
		$query = "INSERT INTO cron(restriccion,config_cron,comando) VALUES ('$restriccion','$config_cron','$comando');";
		unset($_POST['addCron']);
		echo "Nuevo Crontab registrado";

	}elseif(isset($_POST['addAlarma'])){
		$fecha = $_POST['fecha'];
		$mensaje = $_POST['mensaje'];
		
		$query = "INSERT INTO alarma(fecha,mensaje) VALUES ('$fecha','$mensaje');";
		unset($_POST['addAlarma']);
		echo "Nuevo reporte de alarma registrado";

	}elseif(isset($_POST['addPrevencion'])){
		$fecha = $_POST['fecha'];
		$mensaje = $_POST['mensaje'];
		
		$query = "INSERT INTO prevencion(fecha,mensaje) VALUES ('$fecha','$mensaje');";
		unset($_POST['addPrevencion']);
		echo "Nuevo reporte de prevencion registrado";

	}elseif(isset($_POST['addCorreoConfig'])){
		$fecha = $_POST['usuario_nombre'];
		$mensaje = $_POST['mail'];
		$mensaje = $_POST['passwd'];

		$query = "INSERT INTO correo_config(usuario_nombre,mail,passwd) VALUES ('$usuario_nombre','$mail','$passwd');";
		unset($_POST['addCorreoConfig']);
		echo "Nuevo registro de configuracion de correo registrado";

	}elseif(isset($_POST['lista_negra_correo'])){
		$fecha = $_POST['correo'];

		$query = "INSERT INTO lista_negra_correo(correo) VALUES ('$correo');";
		unset($_POST['addCorreoListaNegra']);
		echo "Nuevo registro de correo en lista negra registrado";

	}elseif(isset($_POST['delUsuarioRegistro'])){
		$nombre_usuario_d = $_POST['nombre_usuario_d'];
		$query = "DELETE FROM usuario_registro WHERE nombre_usuario = '$nombre_usuario_d';";
		unset($_POST['delUsuarioRegistro']);
		echo "Registro de usuario_registro eliminado correctamente.";

	}elseif(isset($_POST['delCron'])){
		$id_cron_d = $_POST['id_cron_d'];
		$query = "DELETE FROM cron WHERE id_cron = '$id_cron_d';";
		unset($_POST['delCron']);
		echo "Registro de cron eliminado correctamente.";

	}elseif(isset($_POST['delAlarma'])){
		$id_alarma_d = $_POST['id_alarma_d'];
		$query = "DELETE FROM alarma WHERE id_alarma = '$id_alarma_d';";
		unset($_POST['delAlarma']);
		echo "Registro de alarma eliminado correctamente.";

	}elseif(isset($_POST['delPrevencion'])){
		$id_prevencion_d = $_POST['id_prevencion_d'];
		$query = "DELETE FROM prevencion WHERE id_prevencion = '$id_prevencion_d';";
		unset($_POST['delPrevencion']);
		echo "Registro de prevencion eliminado correctamente.";

	}elseif(isset($_POST['delConfigCorreo'])){
		$id_correo_d = $_POST['id_correo_d'];
		$query = "DELETE FROM correo_config WHERE id_correo = '$id_correo_d';";
		unset($_POST['delConfigCorreo']);
		echo "Registro de correo_config eliminado correctamente.";

		
	}elseif(isset($_POST['delCorreoListaNegra'])){
		$correo_d = $_POST['correo_d'];
		$query = "DELETE FROM lista_negra_correo WHERE correo = '$correo_d';";
		unset($_POST['delCorreoListaNegra']);
		echo "Registro de lista_negra_correo eliminado correctamente.";
	}else{
		echo "Error inesperado. Intente de nuevo ";
		exit;
	}

	$result = pg_query($dbconn, $query);
	if (!$result){
		echo "Error. No se pudo realizar la consulta.\n";
		exit;
	}
	pg_close($dbconn);
	header("Location: ingreso.php");
?>