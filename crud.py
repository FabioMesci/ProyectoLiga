from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'Proyecto_liga', 'secciones')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'edmundo'

# Ruta de la aplicacion


@app.route('/')
def Inicio():
    return redirect(url_for('MostrarTablaDePosiciones'))


# Interfaz para ver las opciones del admin
@app.route('/OpcionesAdmin')
def OpcionesAdmin():
    return render_template('opciones_admin.html')

# Interfaz para añadir posicion de club


@app.route('/EditarPosicionClub')
def EditarPosicionClub():
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre_club FROM club")
    nombre_clubes = [row[0] for row in cursor.fetchall()]

    cursor = db.database.cursor()
    cursor.execute("""SELECT t.*, c.nombre_club FROM tabla_posiciones AS t INNER JOIN club as c
                    ON idTabla_posiciones = fk_club_tabla_posiciones;""")
    myresult = cursor.fetchall()
    # convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()

    return render_template('editar_posicion_club.html', nombre_clubes=nombre_clubes, data=insertObject)


# Interfaz para ver los partidos
@app.route('/Partidos')
def Partidos():
    cursor = db.database.cursor()

    # Obtener datos de estadisticas, estadio, calendario_ligas y partido
    cursor.execute("""select estadisticas.* , partido.equipo_local, partido.equipo_visitante, 
                   calendario_ligas.fecha, estadio.* from estadisticas inner join partido 
                   ON estadisticas.idEstadisticas = partido.fk_idCalendario_Ligas inner join 
                   calendario_ligas on partido.fk_idCalendario_Ligas = calendario_ligas.idCalendario_Ligas 
                   inner join estadio on calendario_ligas.fk_idEstadio = estadio.idEstadio;""")
    partidos = cursor.fetchall()

    return render_template('partidos.html', partidos=partidos)

# Interfaz para ver los clubes


@app.route('/Club')
def Club():
    return render_template('club.html')


# Interfaz para iniciar sesion como administrador
@app.route('/LoginAdmin')
def LoginAdmin():
    return render_template('login.html')

# Interfaz para añadir jugador


@app.route('/AñadirJugador')
def AñadirJugador():
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre_club FROM club")
    nombre_clubes = [row[0] for row in cursor.fetchall()]

    cursor = db.database.cursor()
    cursor.execute("""SELECT j.idJugadores, j.nombre, j.apellido, j.edad, j.posicion, j.pais_de_origen, j.altura_cm, c.nombre_club FROM jugadores AS j INNER JOIN club AS c ON j.fk_nombre_Club = c.nombre_club;""")
    myresult = cursor.fetchall()
    # convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    return render_template('añadir_jugador.html', nombre_clubes=nombre_clubes, data=insertObject)

# Funcion para editar jugador


@app.route('/editJugador', methods=['POST', 'GET'])
def editJugador():
    id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    edad = request.form['edad']
    posicion = request.form['posicion']
    pais = request.form['pais']
    altura = request.form['altura']
    club = request.form['club']

    cursor = db.database.cursor()

    # Verificar si el jugador ya existe en la base de datos
    query_verificar = "SELECT * FROM jugadores WHERE idJugadores = %s"
    cursor.execute(query_verificar, (id,))
    jugador_actual = cursor.fetchone()

    if not jugador_actual:
        flash("El jugador no existe en la base de datos.", "error")
        return redirect(url_for('AñadirJugador'))

    # Verificar si el nombre y apellido han sido modificados
    if nombre != jugador_actual[1] or apellido != jugador_actual[2]:
        # Verificar si el nuevo nombre y apellido ya existen en la base de datos
        query_existente = "SELECT * FROM jugadores WHERE nombre = %s AND apellido = %s"
        cursor.execute(query_existente, (nombre, apellido))
        jugador_existente = cursor.fetchone()

        if jugador_existente:
            flash(
                "El jugador ya existe en la base de datos", "error")
            return redirect(url_for('AñadirJugador'))

    # Actualizamos los datos del jugador
    query_update_jugador = """UPDATE jugadores
                            SET nombre = %s, apellido = %s, edad = %s, posicion = %s, pais_de_origen = %s, altura_cm = %s, fk_nombre_Club = %s
                            WHERE idJugadores = %s"""
    values = (nombre, apellido, edad, posicion, pais, altura, club, id)
    cursor.execute(query_update_jugador, values)
    db.database.commit()

    return redirect(url_for('AñadirJugador'))

# funcion para eliminar jugador de la pestaña de administrador


@app.route('/deleteJugador/<string:id>', methods=['POST', 'GET'])
def deleteJugador(id):
    cursor = db.database.cursor()
    query = "DELETE FROM jugadores WHERE idJugadores=%s"
    data = (id,)
    cursor.execute(query, data)
    db.database.commit()
    return redirect(url_for('AñadirJugador'))


# Interfaz para añadir club
@app.route('/AñadirClub')
def AñadirClub():

    cursor = db.database.cursor()
    cursor.execute("""SELECT club.nombre_club, club.director_tecnico, club.año_fundacion, club.presidente_club, 
                    club.fk_club_tabla_posiciones, estadio.nombre, estadio.ubicación
                    FROM club
                    INNER JOIN estadio ON estadio.fk_nombre_club = club.nombre_club""")
    myresult = cursor.fetchall()
    # convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.execute("""SELECT nombre_club FROM club""")
    Nombres = cursor.fetchall()
    # convertir datos a diccionario
    Nombresclub = []
    nombres = [column[0] for column in cursor.description]
    for record in Nombres:
        Nombresclub.append(dict(zip(nombres, record)))
    cursor.close()

    return render_template('añadir_club.html', data=insertObject, Nombresclub=Nombresclub)

# Ruta para añadir club


@app.route('/addClub', methods=['POST'])
def addClub():
    nombre = request.form['nombre']
    tecnico = request.form['tecnico']
    añofundacion = request.form['añofundacion']
    presidente = request.form['presidente']
    estadio = request.form['estadio']
    ubicacion = request.form['ubicacion']

    if nombre and tecnico and añofundacion and presidente and estadio and ubicacion:

        cursor = db.database.cursor()

        # Verificar si el club ya existe
        select_query = "SELECT * FROM club WHERE nombre_club = %s"
        cursor.execute(select_query, (nombre,))
        result = cursor.fetchall()

        if result:
            # El dato ya existe en la base de datos, mostrar mensaje flash
            flash('El club ingresado ya existe', 'warning')

        else:
            # crear nueva fila en tabla de posiciones
            sql_posiciones = "INSERT INTO tabla_posiciones (puntaje) VALUES (0)"
            data = (0)
            cursor.execute(sql_posiciones, data)
            db.database.commit()

            dato_id = cursor.lastrowid

            # Insertar datos en la tabla Club
            sql_club = "INSERT INTO club (nombre_club, director_tecnico, año_fundacion, presidente_club, fk_club_tabla_posiciones) VALUES (%s, %s, %s, %s, %s)"
            data_club = (nombre, tecnico, añofundacion, presidente, dato_id)
            cursor.execute(sql_club, data_club)

            # Insertar datos en la tabla Estadio
            sql_estadio = "INSERT INTO estadio (nombre, ubicación, fk_nombre_club) VALUES (%s, %s, %s)"
            data_estadio = (estadio, ubicacion, nombre)
            cursor.execute(sql_estadio, data_estadio)

            db.database.commit()

    return redirect(url_for('AñadirClub'))

# Eliminar club


@app.route('/delete/<string:nombre_club>/<string:fk_club_tabla_posiciones>/<string:estadio>')
def delete(nombre_club, fk_club_tabla_posiciones, estadio):

    cursor = db.database.cursor()

    # Actualizar el campo de partido
    select_query = "SELECT idEstadio FROM estadio WHERE nombre = %s"
    cursor.execute(select_query, (estadio,))
    idestadio = cursor.fetchone()  # Usar fetchone() para obtener un solo resultado
    if idestadio:
        idestadio = idestadio[0]  # Extraer el valor correcto de la lista
        update_query = "UPDATE calendario_ligas SET fk_idEstadio = NULL WHERE fk_idEstadio = %s"
        cursor.execute(update_query, (idestadio,))
        db.database.commit()
    else:
        print("El estadio no fue encontrado.")

    # Actualizar el campo de la clave foránea (fk_nombre_club) en la tabla 'jugador'
    update_query = "UPDATE jugadores SET fk_nombre_club = NULL WHERE fk_nombre_club = %s"
    cursor.execute(update_query, (nombre_club,))
    db.database.commit()
    # Actualizar el campo de la clave foránea (equipo_local) en la tabla 'partidos'
    update_query = "UPDATE partido SET equipo_local = NULL WHERE equipo_local = %s"
    cursor.execute(update_query, (nombre_club,))
    db.database.commit()

    # Actualizar el campo de la clave foránea (equipo_visitante) en la tabla 'partidos'
    update_query = "UPDATE partido SET equipo_visitante = NULL WHERE equipo_visitante = %s"
    cursor.execute(update_query, (nombre_club,))
    db.database.commit()

    # Eliminar datos en la tabla Estadio
    sql_estadio = "DELETE FROM estadio WHERE fk_nombre_club = %s"
    cursor.execute(sql_estadio, (nombre_club,))
    db.database.commit()

    # Eliminar fila en la tabla Club
    sql_club = "DELETE FROM club WHERE nombre_club= %s"
    cursor.execute(sql_club, (nombre_club,))
    db.database.commit()

    # Eliminar fila en tabla de posiciones
    sql_posiciones = "DELETE FROM tabla_posiciones WHERE idTabla_posiciones= %s"
    cursor.execute(sql_posiciones, (fk_club_tabla_posiciones,))
    db.database.commit()

    return redirect(url_for('AñadirClub'))


@app.route('/edit/<string:fk_club_tabla_posiciones>', methods=['POST'])
def edit(fk_club_tabla_posiciones):
    nombre = request.form['nombre']
    tecnico = request.form['tecnico']
    añofundacion = request.form['añofundacion']
    presidente = request.form['presidente']
    estadio = request.form['estadio']
    ubicacion = request.form['ubicacion']

    if nombre and tecnico and añofundacion and presidente and estadio and ubicacion:
        cursor = db.database.cursor()

        # Verificar si el club ya existe
        select_query = "SELECT nombre_club FROM club WHERE fk_club_tabla_posiciones = %s"
        cursor.execute(select_query, (fk_club_tabla_posiciones,))
        result1 = cursor.fetchall()
        result = result1[0][0]
        print(result)
        if result == nombre:
            # el nombre del club se mantendra igual y se actualizaran los demás valores

            # Insertar datos en la tabla Estadio
            sql_estadio = "UPDATE estadio SET nombre=%s, ubicación=%s, fk_nombre_club=%s WHERE fk_nombre_club=%s"
            data_estadio = (estadio, ubicacion, nombre, nombre)
            cursor.execute(sql_estadio, data_estadio)
            db.database.commit()
            # Actualizar datos en la tabla Club
            sql_club = "UPDATE club SET nombre_club =%s, director_tecnico=%s, año_fundacion=%s, presidente_club=%s WHERE fk_club_tabla_posiciones=%s"
            data_club = (nombre, tecnico, añofundacion,
                         presidente, fk_club_tabla_posiciones)
            cursor.execute(sql_club, data_club)
            db.database.commit()

        else:
            # el nombre será actualizado
            # Verificar si el nuevo nombre del club ya existe
            select_query = "SELECT * FROM club WHERE nombre_club = %s"
            cursor.execute(select_query, (nombre,))
            result = cursor.fetchall()

            if result:
                # El dato ya existe en la base de datos, mostrar mensaje flash
                flash('El club ingresado ya existe', 'warning')
            else:
                # el nombre del club se actualizara junto a los demás valores
                # Actualizar datos en la tabla Club
                sql_club = "UPDATE club SET nombre_club =%s, director_tecnico=%s, año_fundacion=%s, presidente_club=%s WHERE fk_club_tabla_posiciones=%s"
                data_club = (nombre, tecnico, añofundacion,
                             presidente, fk_club_tabla_posiciones)
                cursor.execute(sql_club, data_club)
                db.database.commit()
                # Insertar datos en la tabla Estadio
                select_query = "SELECT nombre_club FROM club WHERE fk_club_tabla_posiciones = %s"
                cursor.execute(select_query, (fk_club_tabla_posiciones,))
                nombre_club = cursor.fetchone()  # Usar fetchone() para obtener un solo resultado
                if nombre_club:
                    # Extraer el valor correcto de la lista
                    nombre_club = nombre_club[0][0]
                    sql_estadio = "UPDATE estadio SET nombre=%s, ubicación=%s WHERE fk_nombre_club=%s"
                    data_estadio = (estadio, ubicacion, nombre_club)
                    cursor.execute(sql_estadio, data_estadio)
                    db.database.commit()

    return redirect(url_for('AñadirClub'))


# Interfaz para añadir partido
@app.route('/AñadirPartido')
def AñadirPartido():
    cursor = db.database.cursor()
    cursor.execute("""SELECT c.idCalendario_Ligas, p.equipo_local, p.equipo_visitante, c.fecha, es.nombre,
                    e.goleslocales, e.golesvisitantes, e.porcentaje_posesion_local, e.porcentaje_posesion_visitante, 
                    e.tiros_local, e.tiros_visitante, e.tirosapuerta_local, e.tirosapuerta_visitante, 
                    e.faltas_local, e.faltas_visitante, e.tarjetas_amarillas_local, e.tarjetas_amarillas_visitante,
                    e.offsite_local, e.offsite_visitante, e.corner_local, e.corner_visitante 
                   FROM estadio AS es 
                   JOIN calendario_ligas AS c ON es.idEstadio = c.fk_idEstadio 
                   JOIN partido AS p ON c.idCalendario_Ligas = p.fk_idCalendario_Ligas 
                   JOIN estadisticas AS e ON p.fk_idCalendario_Ligas = fk_Partido_idCalendario_Ligas""")
    myresult = cursor.fetchall()
    # convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    # Para mostrar los clubes existentes en la etiqueta de select
    cursor.execute("""SELECT nombre_club FROM club""")
    Nombres = cursor.fetchall()
    # convertir datos a diccionario
    Nombresclub = []
    nombres = [column[0] for column in cursor.description]
    for record in Nombres:
        Nombresclub.append(dict(zip(nombres, record)))

    # Para mostrar los estadios existentes en la etiqueta de select
    cursor.execute("""SELECT nombre FROM estadio""")
    Estadio = cursor.fetchall()
    # convertir datos a diccionario
    Nombreestadio = []
    Nombresta = [column[0] for column in cursor.description]
    for record in Estadio:
        Nombreestadio.append(dict(zip(Nombresta, record)))
    cursor.close()
    return render_template('añadir_partido.html', data=insertObject, Nombresclub=Nombresclub, Nombreestadio=Nombreestadio)

# Ruta para añadir partido


@app.route('/addPartido', methods=['POST'])
def addPartido():
    if request.method == "POST":

        equipo_local = request.form['equipo_local']
        equipo_visitante = request.form['equipo_visitante']
        fecha = request.form['fecha']
        estadio = request.form['estadio']
        gol_local = request.form['gol_local']
        gol_visitante = request.form['gol_visitante']
        posesion_local = request.form['posesion_local']
        posesion_visitante = request.form['posesion_visitante']
        tiros_local = request.form['tiros_local']
        tiros_visitante = request.form['tiros_visitante']
        tiros_puerta_local = request.form['tiros_puerta_local']
        tiros_puerta_visitante = request.form['tiros_puerta_visitante']
        faltas_local = request.form['faltas_local']
        faltas_visitante = request.form['faltas_visitante']
        tarjetas_amarillas_local = request.form['tarjetas_amarillas_local']
        tarjetas_amarillas_visitante = request.form['tarjetas_amarillas_visitante']
        offside_local = request.form['offside_local']
        offside_visitante = request.form['offside_visitante']
        corner_local = request.form['corner_local']
        corner_visitante = request.form['corner_visitante']

        if equipo_local == equipo_visitante:
            flash('Los equipos no pueden ser iguales')
        else:
            cursor = db.database.cursor()

            # Verificar si el partido ya existe
            select_query = """SELECT calendario.fecha, partido.equipo_local, partido.equipo_visitante 
                            FROM calendario_ligas calendario 
                            JOIN partido ON partido.fk_idCalendario_ligas = calendario.idCalendario_Ligas 
                            WHERE calendario.fecha= %s AND partido.equipo_local = %s AND partido.equipo_visitante = %s"""
            cursor.execute(
                select_query, (fecha, equipo_local, equipo_visitante))
            result1 = cursor.fetchall()
            select_query1 = """SELECT calendario.fecha, partido.equipo_local, partido.equipo_visitante 
                            FROM calendario_ligas calendario 
                            JOIN partido ON partido.fk_idCalendario_ligas = calendario.idCalendario_Ligas 
                            WHERE calendario.fecha= %s AND partido.equipo_local = %s AND partido.equipo_visitante = %s"""
            cursor.execute(
                select_query1, (fecha, equipo_visitante, equipo_local))
            result2 = cursor.fetchall()

            if result1 or result2:
                flash('El partido ya existe')
            else:
                # Seleccionar id del estadio
                select_query = "SELECT idEstadio FROM estadio WHERE nombre = %s"
                cursor.execute(select_query, (estadio,))
                result = cursor.fetchone()  # Usar fetchone() en lugar de fetchall()
                db.database.commit()
                # Obtener el valor del idEstadio desde la tupla result
                idestadio = result[0]

                # crear una nueva fecha
                sql_calendario = "INSERT INTO calendario_ligas (fecha, fk_IdEstadio) VALUES (%s, %s)"
                data = (fecha, idestadio)
                cursor.execute(sql_calendario, data)
                db.database.commit()
                idCalendario = cursor.lastrowid

                # Crear nuevo partido
                sql_partido = "INSERT INTO partido (fk_idCalendario_Ligas, equipo_local, equipo_visitante) VALUES (%s, %s, %s)"
                data1 = (idCalendario, equipo_local, equipo_visitante)
                cursor.execute(sql_partido, data1)
                db.database.commit()

                # Crear estadisticas
                sql_estadisticas = """INSERT INTO estadisticas (`goleslocales`, `golesvisitantes`, `porcentaje_posesion_local`, 
                `porcentaje_posesion_visitante`, `tiros_local`, `tiros_visitante`, `tirosapuerta_local`, `tirosapuerta_visitante`, 
                `faltas_local`, `faltas_visitante`, `tarjetas_amarillas_local`, `tarjetas_amarillas_visitante`, `offsite_local`, 
                `offsite_visitante`, `corner_local`, `corner_visitante`, `fk_Partido_idCalendario_Ligas`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                data2 = (gol_local, gol_visitante, posesion_local, posesion_visitante, tiros_local,
                         tiros_visitante, tiros_puerta_local, tiros_puerta_visitante, faltas_local,
                         faltas_visitante, tarjetas_amarillas_local, tarjetas_amarillas_visitante, offside_local,
                         offside_visitante, corner_local, corner_visitante, idCalendario)
                cursor.execute(sql_estadisticas, data2)
                db.database.commit()

    return redirect(url_for('AñadirPartido'))

# Editar partido


@app.route('/editPartido/<string:idCalendario_Ligas>', methods=['POST'])
def editPartido(idCalendario_Ligas):

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']
    fecha = request.form['fecha']
    estadio = request.form['estadio']
    gol_local = request.form['gol_local']
    gol_visitante = request.form['gol_visitante']
    posesion_local = request.form['posesion_local']
    posesion_visitante = request.form['posesion_visitante']
    tiros_local = request.form['tiros_local']
    tiros_visitante = request.form['tiros_visitante']
    tiros_puerta_local = request.form['tiros_puerta_local']
    tiros_puerta_visitante = request.form['tiros_puerta_visitante']
    faltas_local = request.form['faltas_local']
    faltas_visitante = request.form['faltas_visitante']
    tarjetas_amarillas_local = request.form['tarjetas_amarillas_local']
    tarjetas_amarillas_visitante = request.form['tarjetas_amarillas_visitante']
    offside_local = request.form['offside_local']
    offside_visitante = request.form['offside_visitante']
    corner_local = request.form['corner_local']
    corner_visitante = request.form['corner_visitante']

    cursor = db.database.cursor()

    # Verificar si el partido ya existe
    select_query = """SELECT calendario.fecha, partido.equipo_local, partido.equipo_visitante 
                        FROM calendario_ligas calendario 
                        JOIN partido ON partido.fk_idCalendario_ligas = calendario.idCalendario_Ligas 
                        WHERE calendario.fecha= %s AND partido.equipo_local = %s AND partido.equipo_visitante = %s"""
    cursor.execute(select_query, (fecha, equipo_local, equipo_visitante))
    result1 = cursor.fetchall()
    select_query1 = """SELECT calendario.fecha, partido.equipo_local, partido.equipo_visitante 
                        FROM calendario_ligas calendario 
                        JOIN partido ON partido.fk_idCalendario_ligas = calendario.idCalendario_Ligas 
                        WHERE calendario.fecha= %s AND partido.equipo_local = %s AND partido.equipo_visitante = %s"""
    cursor.execute(select_query1, (fecha, equipo_visitante, equipo_local))
    result2 = cursor.fetchall()

    if result1 or result2:
        # la fecha se mantendra igual y se actualizaran los demás valores

        # Insertar nombre de estadio en la tabla calendario liga
        # Seleccionar id del estadio
        select_query = "SELECT idEstadio FROM estadio WHERE nombre = %s"
        cursor.execute(select_query, (estadio,))
        result = cursor.fetchone()  # Usar fetchone() en lugar de fetchall()
        db.database.commit()
        # Obtener el valor del idEstadio desde la tupla result
        idestadio = result[0]

        sql_estadio = "UPDATE calendario_ligas SET fk_idEstadio=%s WHERE idCalendario_Ligas=%s"
        data_estadio = (idestadio, idCalendario_Ligas)
        cursor.execute(sql_estadio, data_estadio)
        db.database.commit()
        # Actualizar datos en la tabla Estadistica
        sql_estadisticas = """UPDATE estadisticas SET `goleslocales` = %s, `golesvisitantes`= %s, `porcentaje_posesion_local` = %s, 
                        `porcentaje_posesion_visitante` = %s, `tiros_local` = %s, `tiros_visitante` = %s, `tirosapuerta_local` = %s, `tirosapuerta_visitante` = %s, 
                        `faltas_local` = %s, `faltas_visitante` = %s, `tarjetas_amarillas_local` = %s, `tarjetas_amarillas_visitante` = %s, `offsite_local` = %s, 
                        `offsite_visitante` = %s, `corner_local` = %s, `corner_visitante` = %s WHERE `fk_Partido_idCalendario_Ligas` = %s
                        """
        data_estadisticas = (gol_local, gol_visitante, posesion_local, posesion_visitante, tiros_local,
                             tiros_visitante, tiros_puerta_local, tiros_puerta_visitante, faltas_local,
                             faltas_visitante, tarjetas_amarillas_local, tarjetas_amarillas_visitante, offside_local,
                             offside_visitante, corner_local, corner_visitante, idCalendario_Ligas)
        cursor.execute(sql_estadisticas, data_estadisticas)
        db.database.commit()

    else:
        # Se cambiara la fecha

        # Insertar nombre de estadio en la tabla calendario liga
        # Seleccionar id del estadio
        select_query = "SELECT idEstadio FROM estadio WHERE nombre = %s"
        cursor.execute(select_query, (estadio,))
        result = cursor.fetchone()  # Usar fetchone() en lugar de fetchall()
        db.database.commit()
        # Obtener el valor del idEstadio desde la tupla result
        idestadio = result[0]
        # Actualizar estadio y fecha
        sql_estadio = "UPDATE calendario_ligas SET fk_idEstadio=%s , fecha=%s WHERE idCalendario_Ligas=%s"
        data_estadio = (idestadio, fecha, idCalendario_Ligas)
        cursor.execute(sql_estadio, data_estadio)
        db.database.commit()

        # Actualizar datos en la tabla Estadistica
        sql_estadisticas = """UPDATE estadisticas SET `goleslocales` = %s, `golesvisitantes`= %s, `porcentaje_posesion_local` = %s, 
                        `porcentaje_posesion_visitante` = %s, `tiros_local` = %s, `tiros_visitante` = %s, `tirosapuerta_local` = %s, `tirosapuerta_visitante` = %s, 
                        `faltas_local` = %s, `faltas_visitante` = %s, `tarjetas_amarillas_local` = %s, `tarjetas_amarillas_visitante` = %s, `offsite_local` = %s, 
                        `offsite_visitante` = %s, `corner_local` = %s, `corner_visitante` = %s WHERE `fk_Partido_idCalendario_Ligas` = %s
                        """
        data_estadisticas = (gol_local, gol_visitante, posesion_local, posesion_visitante, tiros_local,
                             tiros_visitante, tiros_puerta_local, tiros_puerta_visitante, faltas_local,
                             faltas_visitante, tarjetas_amarillas_local, tarjetas_amarillas_visitante, offside_local,
                             offside_visitante, corner_local, corner_visitante, idCalendario_Ligas)
        cursor.execute(sql_estadisticas, data_estadisticas)
        db.database.commit()

    return redirect(url_for('AñadirPartido'))

# Eliminar partido


@app.route('/deletePartido/<string:idCalendario_Ligas>')
def deletePartido(idCalendario_Ligas):

    cursor = db.database.cursor()

    # Eliminar datos en la tabla Calendario Liga
    sql_estadio = "DELETE FROM calendario_ligas WHERE idCalendario_Ligas = %s"
    cursor.execute(sql_estadio, (idCalendario_Ligas,))
    db.database.commit()

    return redirect(url_for('AñadirPartido'))

# Interfaz para añadir jugador


@app.route("/AddJugador", methods=['POST', 'GET'])
def addJugador():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        posicion = request.form['posicion']
        pais = request.form['pais']
        altura = request.form['altura']
        club = request.form['club']

        cursor = db.database.cursor()

        # Verificar si el jugador ya existe en la base de datos
        query_verificar = "SELECT * FROM jugadores WHERE nombre = %s AND apellido = %s"
        cursor.execute(query_verificar, (nombre, apellido))
        jugador_existente = cursor.fetchone()

        if jugador_existente:
            # Si el jugador existe, verificamos si el club es diferente
            # Utilizar índice numérico 6 para obtener el valor de fk_nombre_Club
            if jugador_existente[7] != club:
                # Actualizamos el club del jugador existente en la base de datos
                query_update_club = """INSERT INTO jugadores (nombre, apellido, edad, posicion, pais_de_origen,
                                 altura_cm, fk_nombre_Club) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                values = (nombre, apellido, edad, posicion, pais, altura, club)
                # Utilizar índice numérico 0 para obtener el valor de idJugadores
                cursor.execute(query_update_club, values)
                db.database.commit()
            else:
                # Si el club es el mismo, mostramos un mensaje de error
                flash(
                    "El jugador ya existe en la base de datos con el mismo club.", "error")
                return redirect(url_for('AñadirJugador'))
        else:
            # Si el jugador no existe, agregarlo a la base de datos con el club seleccionado
            query_insertar = """INSERT INTO jugadores (nombre, apellido, edad, posicion, pais_de_origen, altura_cm, fk_nombre_Club)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) """
            values = (nombre, apellido, edad, posicion, pais, altura, club)
            cursor.execute(query_insertar, values)
            db.database.commit()

        return redirect(url_for('AñadirJugador'))

# Funcion para editar posicion de clubes


@app.route('/editPosicion', methods=['POST', 'GET'])
def editPosicion():
    if request.method == 'POST':
        # Obtener los datos enviados por el formulario
        id = request.form['id']
        partidos_jugados = request.form['partidos_jugados']
        victorias = request.form['victorias']
        derrotas = request.form['derrotas']
        empates = request.form['empates']
        gol_a_favor = request.form['gol_a_favor']
        gol_en_contra = request.form['gol_en_contra']
        puntaje = request.form['puntaje']

        # Insertar los datos en la tabla de posiciones
        cursor = db.database.cursor()
        query = """UPDATE tabla_posiciones
                SET partidos_jugados = %s, victorias = %s, derrotas = %s, empates = %s,
                gol_a_favor = %s, gol_en_contra = %s, puntaje = %s
                WHERE idTabla_posiciones = %s"""
        values = (partidos_jugados, victorias, derrotas, empates,
                  gol_a_favor, gol_en_contra, puntaje, id)
        cursor.execute(query, values)
        db.database.commit()

        return redirect(url_for('EditarPosicionClub'))


# funcion para iniciar sesion como administrador
@app.route("/Login", methods=["POST", "GET"])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.database.cursor()
        sql = "SELECT user, password FROM admin WHERE user=%s and password=%s"
        value = (username, password)
        cursor.execute(sql, value)

        # Verificar si el usuario y contraseña existe en la BDD
        result = cursor.fetchone()
        try:
            if result[0] == username and result[1] == password:
                return redirect(url_for('OpcionesAdmin'))
        except TypeError:
            flash('Usuario o Contraseña incorrectos')
            return render_template('login.html')


# Funcion para mostrar partidos y estadisticas en la interfaz de partidos
@app.route('/MostrarPartidos')
def MostrarPartidos():
    cursor = db.database.cursor()

    # Obtener datos de estadisticas, estadio, calendario_ligas y partido
    cursor.execute("""SELECT e.*, p.equipo_local, p.equipo_visitante, cl.fecha, es.nombre 
                    FROM calendario_ligas AS cl 
                    JOIN partido AS p ON cl.idCalendario_Ligas = p.fk_idCalendario_Ligas
                    JOIN estadio AS es ON es.idEstadio = cl.fk_idEstadio 
                    JOIN estadisticas AS e ON e.fk_Partido_idCalendario_Ligas = p.fk_idCalendario_Ligas
                    ORDER BY cl.fecha ASC;""")
    myresult = cursor.fetchall()
    # convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    return render_template('partidos.html', data=insertObject)


# Funcion para mostrar los clubes previamente ingresados a traves de tabla de posiciones
@app.route('/MostrarClubes/<club>')
def MostrarClubes(club):
    cursor = db.database.cursor()

    # Obtener datos de club, estadio y jugadores para el club seleccionado
    cursor.execute("""SELECT c.*, e.idEstadio, e.nombre AS nombre_estadio, e.ubicación, e.fk_nombre_club, j.* 
                   FROM club AS c 
                   INNER JOIN estadio AS e ON c.nombre_club = e.fk_nombre_club 
                   INNER JOIN jugadores AS j ON c.nombre_club = j.fk_nombre_Club
                   WHERE c.nombre_club = %s""", (club,))
    myresult = cursor.fetchall()

    if myresult:
        # Convertir datos a diccionario
        insertObject = []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        return render_template('club.html', data=insertObject)
    else:
        # Si el club no existe o no tiene jugadores, puedes mostrar un mensaje o redirigir a otra página
        flash("El club no existe o no tiene jugadores asociados.", "error")
        return redirect(url_for('MostrarTablaDePosiciones'))


# Interfaz para Mostrar tabla de posiciones
@app.route('/MostrarTablaDePosiciones')
def MostrarTablaDePosiciones():
    cursor = db.database.cursor()

    # Obtener datos de club y tabla_posiciones
    cursor.execute("""SELECT c.nombre_club, c.fk_club_tabla_posiciones, tp.* FROM club AS c 
                   INNER JOIN tabla_posiciones AS tp ON c.fk_club_tabla_posiciones = tp.idTabla_posiciones
                   ORDER BY tp.puntaje DESC;""")
    myresult = cursor.fetchall()
    # convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    return render_template('index.html', data=insertObject)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
