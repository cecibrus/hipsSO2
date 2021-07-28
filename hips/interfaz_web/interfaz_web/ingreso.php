<?php
	session_start();
	if(isset($_SESSION['usuario']) && !empty($_SESSION['usuario'])){
		$dbconn = pg_connect($_SESSION['CONN']);
		if (!$dbconn){
			echo "no se conecta";
			exit;
		}
	}
?>	
<html>
	<head>
    	<title>Sistema HIPS</title>
    	<link rel="stylesheet" href="style_ingreso.css">
		<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>

  	</head>
	<header>
		<h1>SISTEMA HIPS</h1>
	</header>
	<body>
		<div class="box">
			<form action="cerrar_sesion.php" method="post">
				<button type="submit" name="cerrar_sesion" class="logout">Cerrar sesión</button>
				<button type="submit" name="actualizar" onclick="window.location.reload();">Actualizar datos</button>
			</form>
		</div>
		
		<select id="tablabd" name="tabla" class="div-toggle" data-target=".my-info-1">
			<option value="ninguno" data-show=".ninguno">Ninguno</option>
			<option value="usuario_registro" data-show=".usuario_registro">Usuario Registro</option>
			<option value="cron" data-show=".cron">Cron</option>
			<option value="alarma" data-show=".alarma"> Reporte de Alarma</option>
			<option value="prevencion" data-show=".prevencion">Reporte de Prevencion</option>
			<option value="correo_config" data-show=".correo_config">Correos Registrados</option>
			<option value="hashes_archivos" data-show=".hashes_archivos">Hash</option>
			<option value="sniffers" data-show=".sniffers">Sniffers</option>
			<option value="correo_lista_negra" data-show=".correo_lista_negra">Correo en Lista Negra</option>


		</select>
		
		<div class="my-info-1">
			<div id="ninguno" class="ninguno hide"> </div>
			<div id="usuario_registro" class="usuario_registro hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'nombre_usuario'" name="nombre_usuario" required />
					<input type="text" placeholder="'ip_permitida'" name="ip_permitida" required />
					<input type="text" placeholder="'dias_permitidos'" name="dias_permitidos" required />
					<input type="text" placeholder="'rango_horario_permitido'" name="rango_horario_permitido" required />
					<button type="submit" name="addUsuarioRegistro" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'nombre_usuario'" name="nombre_usuario_d" required />
					<button type="submit" name="delUsuarioRegistro" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla usuario_registro</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>nombre_usuario</th>
						<th>ip_permitida</th>
						<th>dias_permitidos</th>
						<th>rango_horario_permitido</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM usuario_registro ORDER BY nombre_usuario;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>

			<div id="cron" class="cron hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'restriccion'" name="restriccion" required />
					<input type="text" placeholder="'config_cron'" name="config_cron" required />
					<input type="text" placeholder="'comando'" name="comando" required />
					<button type="submit" name="addCron" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'id_cron'" name="id_cron_d" required />

					<button type="submit" name="delCron" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla Cron</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>restriccion</th>
						<th>config_cron</th>
						<th>comando</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM cron;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>

			<div id="alarma" class= "alarma hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'fecha'" name="fecha" required/>
					<input type="text" placeholder="'mensaje'" name="mensaje" required/>
					<button type="submit" name="addAlarma">Agregar</button>
				</form>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'id_alarma'" name="id_alarma_d" required />
					<button type="submit" name="delAlarma" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla Alarma</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>id</th>
						<th>fecha</th>
						<th>mensaje</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM alarma ORDER BY id_alarma;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>

			<div id="prevencion" class="prevencion hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'fecha'" name="fecha" required />
					<input type="text" placeholder="'mensaje'" name="mensaje" required />
					<button type="submit" name="addPrevencion" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'id_prevencion'" name="id_prevencion_d" required />
					<button type="submit" name="delPrevencion" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla prevencion</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>id</th>
						<th>fecha</th>
						<th>mensaje</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM prevencion ORDER BY id_prevencion;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>

			<div id="correo_config" class="correo_config hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'usuario_nombre'" name="usuario_nombre" required />
					<input type="text" placeholder="'mail'" name="mail" required />
					<input type="text" placeholder="'passwd'" name="passwd" required />
					<button type="submit" name="addCorreoConfig" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'id_correo'" name="id_correo_d" required />
					<button type="submit" name="delConfigCorreo" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla correo_config</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>id_correo</th>
						<th>usuario_nombre</th>
						<th>mail</th>
						<th>passwd</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM correo_config ORDER BY id_correo;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>

			<div id="lista_negra_correo" class="lista_negra_correo hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'correo'" name="correo" required />
					<button type="submit" name="addCorreoListaNegra" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'correo'" name="correo_d" required />
					<button type="submit" name="delCorreoListaNegra" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla lista_negra_correo</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>correo</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM lista_negra_correo ;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>	

			<div id="hashes_archivos" class="hashes_archivos hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'nombre_archivo'" name="nombre_archivo" required />
					<input type="text" placeholder="'hash'" name="hash" required />

					<button type="submit" name="addHashes" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'id_hash'" name="id_hash_d" required />
					<button type="submit" name="delHash" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla hashes_archivos</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>id_hash</th>
						<th>nombre_archivo</th>
						<th>hash</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM hashes_archivos ;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>	
			<div id="sniffers" class="sniffers hide">
				<br/>
				<br/>
				<b>Agregar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'nombre'" name="nombre" required />

					<button type="submit" name="addSniffers" class="addButton">Agregar</button>
				</form>
				<br/>
				<b>Eliminar fila:</b>
				<br/>
				<br/>
				<form action="actualizar.php" method="post">
					<input type="text" placeholder="'id_sniffer'" name="id_sniffer_d" required />
					<button type="submit" name="delSniffers" class="deleteButton">Eliminar</button>
				</form>
				<br/>
				<br/>
				<br/>
				<h1>Tabla sniffers</h1>
				<table class="tablabd" style="width:100%">
					<tr>
						<th>id_sniffer</th>
						<th>nombre</th>
					</tr>
					<?php
						$result = pg_query($dbconn, "SELECT * FROM sniffers ;");
						if ($result){
							while($row = pg_fetch_row($result)){
								echo "<tr>";
								for($i=0; $i<pg_num_fields($result); $i++){
									echo "<td>".$row[$i]."</td>";
								}
								echo "</tr>";
							}
						}else{
							exit;
						}
					?>
				</table>	
			</div>	
		</div>
		<script>
			$(document).on('change', '.div-toggle', function() {
				var target = $(this).data('target');
				var show = $("option:selected", this).data('show');
				$(target).children().addClass('hide');
				$(show).removeClass('hide');
			});
			$(document).ready(function(){
				$('.div-toggle').trigger('change');
			});	
		</script>
	</body>
</html>

<?php
	pg_close($dbconn);
?>