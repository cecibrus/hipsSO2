<?php
	session_start();
	if(isset($_SESSION['usuario']) && !empty($_SESSION['usuario'])):
		$dbconn = pg_connect($_SESSION['CONN']);
?>	

<html>
	<div class="box">
		<form action="cerrar_sesion.php" method="post">
			<button type="submit" name="cerrar_sesion" class="warnbtn">Cerrar sesión</button>
			<button type="submit" name="actualizar" onclick="window.location.reload();">Actualizar datos</button>
		</form>
	</div>


	<select id="tablabd" name="tabla" onchange="changeView()">
		<option value="usuario_registro">Usuario Registro</option>
		<option value="cron">Cron</option>
		<option value="alarma"> Reporte de Alarma</option>
		<option value="prevencion">Reporte de Prevencion</option>
		<option value="correo">Correos Registrados</option>
		<option value="correo_lista_negra">Correo no Deseado</option>
	</select>
	<div id="usuarioRegistro">
		<br/>
		<br/>
		<b>Agregar fila:</b>
		<br/>
		<br/>
		<form action="update.php" method="post">
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
		<form action="update.php" method="post">
			<input type="text" placeholder="'nombre_usuario'" name="nombre_usuario" required />
			<input type="text" placeholder="'ip_permitida'" name="ip_permitida" required />
			<input type="text" placeholder="'dias_permitidos'" name="dias_permitidos" required />
			<input type="text" placeholder="'rango_horario_permitido'" name="rango_horario_permitido" required />

			<button type="submit" name="delUsuarioRegistro" class="deleteButton">Eliminar</button>
		</form>
		<br/>
		<br/>
		<br/>
		<tr>
			<th>Tabla Usuario Registro</th>
		</tr>
		<?php
			$result = pg_query($dbconn, "SELECT * FROM usuario_registro ORDER BY usuario_registro;");
			if (!$result){echo "1";}
			while ($row = pg_fetch_row($result)){
				echo "<tr><td>".$row[0]."</td></tr>";
			}
		?>
    </div>

	<div id="cron" style="display:none">
		<br/>
		<br/>
		<b>Agregar fila:</b>
		<br/>
		<br/>
		<form action="update.php" method="post">
			<input type="text" placeholder="'restriccion'" name="restriccion" required />
			<input type="text" placeholder="'config_cron'" name="config_cron" required />
			<input type="text" placeholder="'comando'" name="comando" required />
			<button type="submit" name="addCron" class="addButton">Agregar</button>
		</form>
		<br/>
		<b>Eliminar fila:</b>
		<br/>
		<br/>
		<form action="update.php" method="post">
			<input type="text" placeholder="'restriccion'" name="restriccion" required />
			<input type="text" placeholder="'config_cron'" name="config_cron" required />
			<input type="text" placeholder="'comando'" name="comando" required />
			<button type="submit" name="delCron" class="deleteButton">Eliminar</button>
		</form>
		<br/>
		<br/>
		<br/>
		<table style="width:100%">
			<tr>
				<th>Process Name</th>
				<th>Max CPU %</th>
				<th>Max RAM %</th>
				<th>Max Runtime(ms)</th>
			</tr>
		<?php
			$result = pg_query($dbconn, "SELECT * FROM processlimits ORDER BY name ASC;");
			if (!$result){echo "2";}
			while ($row = pg_fetch_row($result)){
				echo "<tr><td>".$row[0]."</td><td>".$row[1]."</td><td>".$row[2]."</td><td>".$row[3]."</td></tr>";
			}
		?>
		</table>

	</div>

	<div id="alarma" style="display:none">
		<br/>
		<br/>
		<b>Update Info:</b>
		<br/>
		<br/>
		<form action="update.php" method="post">
			<input type="text" placeholder="'fecha'" name="fecha" required/>
			<input type="text" placeholder="'mensaje'" name="mensaje" required/>
			<button type="submit" name="addAlarma">Agregar</button>
		</form>
		</form>
		<br/>
		<b>Eliminar fila:</b>
		<br/>
		<br/>
		<form action="update.php" method="post">
			<input type="text" placeholder="'id'" name="delId" required />
			<button type="submit" name="delAlarma" class="deleteButton">Eliminar</button>
		</form>
		<br/>
		<br/>
		<br/>
		<tr>
			<th>My IPv4</th>
			<th>Admin Email</th>
			<th>Admin Email Password</th>
		</tr>
		<?php
			$result = pg_query($dbconn, "SELECT * FROM alarma;");
			if (!$result){echo "3";}
			while ($row = pg_fetch_row($result)){
				echo "<tr><td>".$row[0]."</td><td>".$row[2]."</td><td>".$row[3]."</td></tr>";
			}
		?>
		</div>

		<div id="prevencion" style="display:none">
			<br/>
			<br/>
			<b>Agregar fila:</b>
			<br/>
			<br/>
			<form action="update.php" method="post">
				<input type="text" placeholder="'fecha'" name="fecha" required />
				<input type="text" placeholder="'mensaje'" name="mensaje" />
				<button type="submit" name="addPrevencion" class="addButton">Agregar</button>
				<br/>
			</form>
			<br/>
			<b>Eliminar fila:</b>
			<br/>
			<br/>
			<form action="update.php" method="post">
				<input type="text" placeholder="'fecha'" name="delFecha" required />
				<button type="submit" name="delPrevencion" class="deleteButton">Eliminar</button>
			</form>
			<br/>
			<br/>
			<br/>
			<table style="width:100%">
				<tr>
					<th>File Absolute Path</th>
					<th>MD5SUM Generated Hash</th>
				</tr>
			<?php
				$result = pg_query($dbconn, "SELECT * FROM md5sum ORDER BY dir ASC;");
				if (!$result){echo "4";}
				while ($row = pg_fetch_row($result)){
					//echo "<br> <b>File Absolute Path:</b> ".$row[0]." <b>Hash:</b> ".$row[1]."<br>";
					echo "<tr><td>".$row[0]."</td><td>".$row[1]."</td></tr>";
				}
			?>
			</table>

		</div>

		<div id="correo_config" style="display:none">
			<br/>
			<br/>
			<b>Agregar fila:</b>
			<br/>
			<br/>
			<form action="update.php" method="post">_
				<input type="text" placeholder="'usuario_nombre'" name="usuario_nombre" required />
				<input type="text" placeholder="'mail'" name="mail" />
				<input type="text" placeholder="'passwd'" name="passwd" />
				<button type="submit" name="addCorreoConfig" class="addButton">Agregar</button>
				<br/>
			</form>
			<br/>
			<b>Eliminar fila:</b>
			<br/>
			<br/>
			<form action="update.php" method="post">
				<input type="text" placeholder="'usuario_nombre'" name="usuario_nombre" required />
				<input type="text" placeholder="'mail'" name="mail" required />
				<input type="text" placeholder="'passwd'" name="passwd" required />

				<button type="submit" name="delConfigCorreo" class="deleteButton">Eliminar</button>
			</form>
			<br/>
			<br/>
			<br/>
			<table style="width:100%">
				<tr>
					<th>File Absolute Path</th>
					<th>MD5SUM Generated Hash</th>
				</tr>
			<?php
				$result = pg_query($dbconn, "SELECT * FROM md5sum ORDER BY dir ASC;");
				if (!$result){echo "4";}
				while ($row = pg_fetch_row($result)){
					echo "<tr><td>".$row[0]."</td><td>".$row[1]."</td></tr>";
				}
			?>
			</table>

		</div>


		<div id="lista_negra_correo" style="display:none">
			<br/>
			<br/>
			<b>Agregar fila:</b>
			<br/>
			<br/>
			<form action="update.php" method="post">_
				<input type="text" placeholder="'correo'" name="usuario_nombre" required />
				<button type="submit" name="addCorreListaNegra" class="addButton">Agregar</button>
				<br/>
			</form>
			<br/>
			<b>Eliminar fila:</b>
			<br/>
			<br/>
			<form action="update.php" method="post">
				<input type="text" placeholder="'correo'" name="usuario_nombre" required />
				<button type="submit" name="delCorreoListaNegra" class="deleteButton">Eliminar</button>
			</form>
			<br/>
			<br/>
			<br/>
			<table style="width:100%">
				<tr>
					<th>File Absolute Path</th>
					<th>MD5SUM Generated Hash</th>
				</tr>
			<?php
				$result = pg_query($dbconn, "SELECT * FROM md5sum ORDER BY dir ASC;");
				if (!$result){echo "4";}
				while ($row = pg_fetch_row($result)){
					echo "<tr><td>".$row[0]."</td><td>".$row[1]."</td></tr>";
				}
			?>
			</table>

		</div>


	

		

<?php else: 
	echo "no session";
	header("Location: index.php");
?>
<?php endif;?>
</html>

<script>
	$(document).on('change', '.tablabd', function() {
		var target = $(this).data('target');
		var show = $("option:selected", this).data('show');
		$(target).children().addClass('hide');
		$(show).removeClass('hide');
	});
	$(document).ready(function(){
		$('.tablabd').trigger('change');
	});
</script>	
<script>
	function changeView(){
		var dbtable = document.getElementById("dbtable");
		var selectedDiv = dbtable.options[dbtable.selectedIndex].value + "Div";
		for(var i=0; i<dbtable.length; i++){
			var divId = dbtable.options[i].value + "Div";
			document.getElementById(divId).style.display = "none";
		}
		document.getElementById(selectedDiv).style.display = "block";
		sessionStorage.setItem("currentSelection",dbtable.options[dbtable.selectedIndex].value);
	};
	
</script>

<script>
	//document.getElementById("dbtable").onchange = changeView();
	var selStor = sessionStorage.getItem("currentSelection");
	if (selStor != null){
		document.getElementById("dbtable").value = selStor;
		//window.alert(selStor);
		changeView();
	}
</script>

<?php
pg_close($dbconn);
?>