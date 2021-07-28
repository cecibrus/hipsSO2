<?php
	session_start();
	if(isset($_SESSION['usuario']) && !empty($_SESSION['usuario'])){
    header("Location: ingreso.php");
  }
?>

<!DOCTYPE html>
<html>
  <head>
    <title>Sistema HIPS</title>
    <link rel="stylesheet" href="style_index.css">
  </head>
  <body>
    <form action="validacion.php" method="POST">
      <div class="login-box">
        <img src="user.png" class="avatar" alt="Avatar Image">
        <h1>Iniciar Sesión</h1>
        <form>
          <!-- USERNAME INPUT -->
          <label for="text">Usuario</label>
          <input type="text" placeholder="Ingrese el nombre de usuario" name="usuario">
          <!-- PASSWORD INPUT -->
          <label for="password">Contraseña</label>
          <input type="password" placeholder="Ingrese la contraseña" name="contrasenha">
          <input type="submit" value="Ingresar">
          <div class="IngresoFallido">
				    <?php if(isset($_SESSION['INCORRECT'])){
              echo "Usuario o contraseña incorrecta.";
            }
            ?>		
		      </div>
        </form>
      </div>
    </form>
  </body>
</html>