from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_mysqldb import MySQL
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import make_response, Flask, render_template, request, redirect, url_for, flash
from flask import request, redirect, url_for, render_template, flash, Response
from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
import csv
from datetime import datetime, timedelta 
import uuid
import datetime
from flask_mail import Mail, Message
from flask import request, redirect, url_for, flash, render_template
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import string
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User
from flask import jsonify
import re
from werkzeug.security import generate_password_hash
from datetime import datetime

def date_format(value, format='%Y-%m-%d'):
    """Formatea un objeto de fecha o cadena a un formato específico."""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value.split()[0], '%Y-%m-%d')
        except ValueError:
            return value 
    
    if isinstance(value, datetime):
        return value.strftime(format)
    
    return value

def format_currency(value):
    """Formatea un número como moneda (ej: 1234.56 -> 1,234.56)."""
    try:
        return "{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value

app = Flask(__name__)
app.config.from_object(config['development'])
csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'
app.jinja_env.filters['format_currency'] = format_currency 
app.jinja_env.filters['date_format'] = date_format

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 's.ll4nzz@gmail.com' # ⬅️ Tu email
app.config['MAIL_PASSWORD'] = '' # ⬅️ Contraseña de aplicación
app.config['MAIL_DEFAULT_SENDER'] = 'tu_correo_de_envio@gmail.com'

mail = Mail(app)

@login_manager_app.user_loader
def load_user(IdUsuario):
    return ModelUser.get_by_id(db, IdUsuario)

def redirigir_a_dashboard_rol(IdRol):
    """Retorna el endpoint del dashboard basado en el IdRol."""
    if IdRol == 9: 
        return 'dashboard_admin'
    elif IdRol == 11: 
        return 'dashboard_vendedora'
    elif IdRol == 12: 
        return 'dashboard_contadora'
    elif IdRol == 13: 
        return 'dashboard_bodega'
    elif IdRol == 14: 
        return 'dashboard_dentista'
    return 'login'

def redirigir_error_rol():
    """Redirige a un usuario sin permisos al dashboard que le corresponde."""
    endpoint = redirigir_a_dashboard_rol(current_user.IdRol)
    
    if endpoint == 'login':
        flash("Rol no reconocido o acceso denegado.", "danger")
        return redirect(url_for('login'))
        
    return redirect(url_for(endpoint))

def format_currency(value):
    """Formatea un número como moneda (ej: 1234.56 -> 1,234.56)."""
    try:
        return "{:,.2f}".format(float(value)) 
    except (ValueError, TypeError):
        return value

def get_filtered_asistencias(cur, usuario_id, fecha_inicio, fecha_fin):
    """Genera y ejecuta la consulta SQL filtrada."""

    start_date = fecha_inicio if fecha_inicio and fecha_inicio != '1900-01-01' else '1900-01-01'
    end_date = fecha_fin if fecha_fin and fecha_fin != '2100-12-31' else '2100-12-31'

    sql_query = """
        SELECT a.*, u.Nombres, u.Apellidos, u.IdUsuario
        FROM asistencia a
        JOIN usuario u ON a.IdUsuario = u.IdUsuario
        WHERE a.Fecha BETWEEN %s AND %s 
    """
    params = [start_date, end_date]

    if usuario_id and usuario_id.isdigit():
        sql_query += " AND a.IdUsuario = %s"
        params.append(usuario_id)
        
    sql_query += " ORDER BY a.Fecha DESC, a.HoraEntrada DESC"
    
    cur.execute(sql_query, tuple(params))
    return cur.fetchall()

def format_currency(value):
    """Formatea un número como moneda (ej: 1234.56 -> 1,234.56)."""
    try:
        return "{:,.2f}".format(float(value)) 
    except (ValueError, TypeError):
        return value

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        get_flashed_messages() 
        return render_template('auth/login.html')

    else:
        correo = request.form['username']
        password = request.form['password']
        
        user = User(
            0,            # IdUsuario
            0,            # IdRol
            "",           # Nombres
            "",           # Apellidos
            "",           # TipoDocumento
            "",           # Documento
            correo,       # Correo
            "",           # CorreoCorporativo
            "",           # FechaContratacion
            "",           # FechaNacimiento
            "",           # Telefono
            password,     # Contrasena
            0,            # Estado
            ""            # NombreRol
        )
        
        logged_user = ModelUser.login(db, user) 
        
        if logged_user is not None:
            login_user(logged_user)
            
            if logged_user.IdRol == 9:      # Admin
                return redirect(url_for('dashboard_admin'))
            elif logged_user.IdRol == 11:    # Vendedora
                return redirect(url_for('dashboard_vendedora'))
            elif logged_user.IdRol == 12:    # Contadora
                return redirect(url_for('dashboard_contadora'))
            elif logged_user.IdRol == 13:    # Bodega
                return redirect(url_for('dashboard_bodega'))
            elif logged_user.IdRol == 14:    # Dentista
                return redirect(url_for('dashboard_dentista'))
            else:
                flash("Rol no reconocido. Contacte al administrador.", 'danger')
                return redirect(url_for('login'))
        else:
            flash("Credenciales inválidas o el usuario no existe.", 'danger')

        return redirect(url_for('login'))

@app.route('/olvide-password', methods=['GET', 'POST'])
def olvide_password():
    if request.method == 'POST':
        email = request.form.get('email')
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cur.execute("SELECT IdUsuario, Nombres FROM Usuario WHERE Correo = %s", (email,))
        usuario = cur.fetchone()
        cur.close()

        if usuario:
            token = str(uuid.uuid4())
            expiracion = datetime.now() + timedelta(hours=1) 
            
            cur = db.connection.cursor()
            cur.execute("UPDATE Usuario SET ResetToken = %s, ResetExpiracion = %s WHERE IdUsuario = %s", 
                        (token, expiracion, usuario['IdUsuario']))
            db.connection.commit()
            cur.close()

            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Aquí va tu llamada a la función real de envío de email:
            # send_email_reset(usuario['Nombres'], email, reset_url)
            
            flash("Si el email está registrado, recibirás un enlace para restablecer tu contraseña en breve.", "info")
            return redirect(url_for('login'))
        else:
            flash("Si el email está registrado, recibirás un enlace para restablecer tu contraseña en breve.", "info")
            return redirect(url_for('olvide_password'))
            
    return render_template('auth/olvide_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cur.execute("SELECT IdUsuario, ResetExpiracion FROM Usuario WHERE ResetToken = %s", (token,))
    usuario = cur.fetchone()
    cur.close()

    # Usar datetime.now() sin prefijo
    if not usuario or usuario['ResetExpiracion'] < datetime.now():
        flash("El enlace de restablecimiento es inválido o ha expirado.", "danger")
        return redirect(url_for('olvide_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template('auth/reset_password.html', token=token)
            
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
            return render_template('auth/reset_password.html', token=token)

        hashed_password = generate_password_hash(password)

        cur = db.connection.cursor()
        cur.execute("""
            UPDATE Usuario 
            SET Password = %s, ResetToken = NULL, ResetExpiracion = NULL 
            WHERE IdUsuario = %s
        """, (hashed_password, usuario['IdUsuario']))
        db.connection.commit()
        cur.close()

        flash("Tu contraseña ha sido restablecida exitosamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))

    return render_template('auth/reset_password.html', token=token)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard/admin')
@login_required
def dashboard_admin():
    if current_user.IdRol != 9:
        return redirigir_error_rol() 
        
    cur = db.connection.cursor()

    try:
        cur.execute("""
            SELECT COUNT(IdUsuario) 
            FROM usuario 
            WHERE FechaRegistro >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        """)
        nuevos_usuarios = cur.fetchone()[0] 
    except Exception as e:
        print(f"Error al contar nuevos usuarios: {e}")
        nuevos_usuarios = 0

    try:
        cur.execute("""
            SELECT COUNT(IdAsistencia) 
            FROM asistencia 
            WHERE Fecha = CURDATE() AND HoraEntrada IS NOT NULL
        """)
        asistencias_dia = cur.fetchone()[0]
    except Exception as e:
        print(f"Error al contar asistencias: {e}")
        asistencias_dia = 0

    try:
        cur.execute("""
            SELECT COUNT(IdDenuncia) 
            FROM denuncia 
            WHERE Estado = 'Pendiente'
        """)
        solicitudes_pendientes = cur.fetchone()[0]
    except Exception as e:
        print(f"Error al contar solicitudes: {e}")
        solicitudes_pendientes = 0

    try:
        cur.execute("SELECT COUNT(IdAsistencia) FROM asistencia")
        reportes_generados = cur.fetchone()[0]
    except Exception as e:
        print(f"Error al contar reportes generados: {e}")
        reportes_generados = 0

    cur.close()
    
    return render_template('dashboard_admin.html',
                           nuevos_usuarios=nuevos_usuarios,
                           asistencias_dia=asistencias_dia,
                           solicitudes_pendientes=solicitudes_pendientes,
                           reportes_generados=reportes_generados)

@app.route('/dashboard/vendedora')
@login_required
def dashboard_vendedora():
    if current_user.IdRol != 11:
        flash("No tienes permisos para acceder a este panel.", 'danger')
        return redirigir_error_rol()

    cur = db.connection.cursor()
    vendedora_id = current_user.IdUsuario

    try:
        cur.execute("""
            SELECT SUM(TotalVenta) 
            FROM venta 
            WHERE IdUsuario = %s 
            AND MONTH(FechaVenta) = MONTH(CURDATE()) 
            AND YEAR(FechaVenta) = YEAR(CURDATE())
        """, (vendedora_id,))
        ventas_mes_actual = cur.fetchone()[0] or 0.00
    except Exception as e:
        print(f"Error al calcular ventas del mes: {e}")
        ventas_mes_actual = 0.00
    
    try:
        cur.execute("""
            SELECT COUNT(IdCliente) 
            FROM cliente 
            WHERE IdUsuarioAsignado = %s 
            AND MONTH(FechaRegistro) = MONTH(CURDATE()) 
            AND YEAR(FechaRegistro) = YEAR(CURDATE())
        """, (vendedora_id,))
        clientes_nuevos_mes = cur.fetchone()[0]
    except Exception as e:
        print(f"Error al contar clientes nuevos: {e}")
        clientes_nuevos_mes = 0

    try:
        cur.execute("""
            SELECT COUNT(IdAsistencia) 
            FROM asistencia 
            WHERE IdUsuario = %s AND Fecha = CURDATE() AND HoraEntrada IS NOT NULL
        """, (vendedora_id,))
        asistencia_hoy = cur.fetchone()[0]
    except Exception as e:
        print(f"Error al verificar asistencia: {e}")
        asistencia_hoy = 0
        
    cur.close()

    ventas_mes_formateadas = f"${ventas_mes_actual:,.2f}"

    response = make_response(render_template(
        'dashboard_vendedora.html', 
        usuario=current_user,
        ventas_mes_actual=ventas_mes_formateadas,
        clientes_nuevos_mes=clientes_nuevos_mes,
        asistencia_hoy=asistencia_hoy
    ))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/dashboard/bodega')
@login_required
def dashboard_bodega():
    if current_user.IdRol != 13:
        flash("No tienes permisos para acceder a este panel.")
        return redirect(url_for('dashboard_admin'))

    response = make_response(render_template('dashboard_bodega.html', usuario=current_user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/dashboard/dentista')
@login_required
def dashboard_dentista():
    if current_user.IdRol != 14:
        flash("No tienes permisos para acceder a este panel.")
        return redirect(url_for('dashboard_admin'))

    response = make_response(render_template('dashboard_dentista.html', usuario=current_user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/usuarios')
@login_required
def usuarios():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM usuario")
    data = cur.fetchall()
    return render_template('usuarios/usuarios.html', usuarios=data)

@app.route('/usuarios/add', methods=['GET', 'POST'])
@login_required
def add_usuario():
    def load_roles():
        try:
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT IdRol, NombreRol FROM rol ORDER BY NombreRol")
            roles = cur.fetchall()
            cur.close()
            return roles
        except Exception as e:
            print(f"Error al cargar roles: {e}")
            return []

    if request.method == 'POST':
        id_rol = request.form.get('idRol') 
        nombres = request.form.get('nombres', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        documento = request.form.get('documento')
        contrasena_plana = request.form.get('contrasena')

        required_fields = {
            'idRol': id_rol, 
            'nombres': nombres, 
            'apellidos': apellidos,
            'documento': documento, 
            'correo': request.form.get('correo'),
            'contrasena': contrasena_plana
        }
        
        if any(not value for value in required_fields.values()):
            flash("Error: Todos los campos marcados como obligatorios (*) deben ser completados.", 'danger')
            roles = load_roles()
            return render_template('usuarios/agregar_usuario.html', roles=roles) 

        contrasena_hash = generate_password_hash(contrasena_plana)
        
        try:
            cur = db.connection.cursor()

            cur.execute("SELECT Documento FROM usuario WHERE Documento = %s", (documento,))
            existing_user = cur.fetchone()
            
            if existing_user:
                flash("Error: El número de documento ya está registrado.", 'danger')
                roles = load_roles() 
                cur.close()
                return render_template('usuarios/agregar_usuario.html', roles=roles)

            cur.execute("""
                INSERT INTO usuario (IdRol, Nombres, Apellidos, TipoDocumento, Documento, Correo,
                CorreoCorporativo, FechaContratacion, FechaNacimiento, Telefono, Contrasena, estado)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                int(id_rol),
                nombres,
                apellidos,
                request.form.get('tipoDocumento'),
                documento,
                request.form.get('correo'),
                request.form.get('correo_corporativo'),
                request.form.get('fechaContratacion') or None, # Manejo de NULL
                request.form.get('fechaNacimiento') or None,   # Manejo de NULL
                request.form.get('telefono'),
                contrasena_hash,
                1 
            ))

            db.connection.commit() 
            cur.close() 
            
            flash("Usuario agregado correctamente.", 'success')
            return redirect(url_for('usuarios')) 
            
        except Exception as e:
            print(f"ERROR CRÍTICO EN INSERCIÓN SQL: {e}") 
            
            db.connection.rollback()
            flash(f"Ocurrió un error al agregar el usuario: {e}", 'danger')
            
            roles = load_roles()
            return render_template('usuarios/agregar_usuario.html', roles=roles) 

    roles = load_roles()
    return render_template('usuarios/agregar_usuario.html', roles=roles)

@app.route('/usuarios/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_usuario(id):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        try:
            id_rol = request.form.get('idRol')
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            tipo_documento = request.form.get('tipoDocumento')
            documento = request.form.get('documento')
            correo = request.form.get('correo')
            correo_corporativo = request.form.get('correo_corporativo')
            telefono = request.form.get('telefono')
            
            fecha_contratacion = request.form.get('fechaContratacion') or None
            fecha_nacimiento = request.form.get('fechaNacimiento') or None
            
            contrasena_plana = request.form.get('contrasena', '').strip()
            
            
            fields = [
                'IdRol', 'Nombres', 'Apellidos', 'TipoDocumento', 'Documento',
                'Correo', 'CorreoCorporativo', 'FechaContratacion', 'FechaNacimiento', 
                'Telefono'
            ]
            
            values = [
                int(id_rol), nombres, apellidos, tipo_documento, documento,
                correo, correo_corporativo, fecha_contratacion, fecha_nacimiento,
                telefono
            ]

            if contrasena_plana:
                contrasena_hash = generate_password_hash(contrasena_plana)
                fields.append('Contrasena')
                values.append(contrasena_hash)
            
            set_clause = ', '.join([f'{field}=%s' for field in fields])
            
            sql_query = f"UPDATE usuario SET {set_clause} WHERE IdUsuario=%s"
            
            params = tuple(values) + (id,) 

            cur.execute(sql_query, params)
            db.connection.commit()
            cur.close()
            
            flash("Usuario actualizado correctamente.", 'success')
            return redirect(url_for('usuarios'))
            
        except Exception as e:
            db.connection.rollback()
            cur.close()
            print(f"ERROR CRÍTICO al actualizar usuario {id}: {e}") 
            flash(f"Ocurrió un error al actualizar el usuario: {e}", 'danger')
            return redirect(url_for('edit_usuario', id=id))

    
    try:
        cur.execute("SELECT IdRol, NombreRol FROM rol ORDER BY NombreRol")
        roles = cur.fetchall() 
        
        cur.execute("SELECT * FROM usuario WHERE IdUsuario=%s", (id,))
        usuario = cur.fetchone()

        if not usuario:
            flash(f"Usuario con ID {id} no encontrado.", 'danger')
            cur.close()
            return redirect(url_for('usuarios'))
        
        cur.execute("SELECT * FROM horario WHERE IdUsuario=%s", (id,))
        horarios = cur.fetchall()
        cur.close()
        
    except Exception as e:
        print(f"ERROR al cargar datos del formulario de edición: {e}")
        flash("Error al cargar los datos necesarios para la edición.", 'danger')
        if cur and not cur.closed:
            cur.close()
        return redirect(url_for('usuarios'))

    return render_template('usuarios/editar_usuario.html',
                           usuario=usuario,
                           horarios=horarios,
                           roles=roles, 
                         )

@app.route('/usuarios/delete/<int:id>')
@login_required
def delete_usuario(id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM usuario WHERE IdUsuario=%s", (id,))
    db.connection.commit()
    flash("Usuario eliminado correctamente.")
    return redirect(url_for('usuarios'))

@app.route('/perfil')
@login_required 
def perfil():
    if current_user.is_authenticated:
        datos_usuario = {
            'nombre_completo': f"{current_user.Nombres} {current_user.Apellidos}", 
            'email': current_user.Correo,
            'rol': current_user.NombreRol,
            'telefono': current_user.Telefono if hasattr(current_user, 'Telefono') else 'N/A',
            'ultima_actividad': 'Hoy, 5:45 PM', 
        }
        
        encuestas_pendientes = [
            {'titulo': 'Encuesta de Clima Laboral', 'fecha_limite': '2025-10-15'},
            {'titulo': 'Evaluación de Desempeño', 'fecha_limite': '2025-11-30'}
        ]
        
        return render_template(
            'usuario/perfil.html',  
            title='Mi Perfil', 
            usuario=datos_usuario,
            pendientes=encuestas_pendientes
        )
        
    else:
        flash('Necesitas iniciar sesión para ver tu perfil.', 'warning')
        return redirect(url_for('login'))

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            correo = request.form.get('correo')
            telefono = request.form.get('telefono')
            fecha_nacimiento = request.form.get('fechaNacimiento') or None 
            
            contrasena_plana = request.form.get('contrasena', '').strip()
            
            cur = db.connection.cursor()
            
            fields = ['Nombres', 'Apellidos', 'Correo', 'Telefono', 'FechaNacimiento']
            values = [nombres, apellidos, correo, telefono, fecha_nacimiento]

            if contrasena_plana:
                contrasena_hash = generate_password_hash(contrasena_plana)
                fields.append('Contrasena')
                values.append(contrasena_hash)
            
            set_clause = ', '.join([f'{field}=%s' for field in fields])
            
            sql_query = f"UPDATE usuario SET {set_clause} WHERE IdUsuario=%s"
            
            params = tuple(values) + (current_user.IdUsuario,)

            cur.execute(sql_query, params)
            db.connection.commit()
            cur.close()
            
            flash("Tu perfil ha sido actualizado correctamente.", 'success')
            return redirect(url_for('perfil'))
            
        except Exception as e:
            db.connection.rollback()
            if 'cur' in locals() and not cur.closed:
                cur.close()
            print(f"ERROR CRÍTICO al actualizar perfil: {e}")
            flash(f"Ocurrió un error al guardar los cambios: {e}", 'danger')
            return redirect(url_for('editar_perfil'))

    return render_template(
        'usuario/editar_perfil.html', 
        title='Editar Mi Perfil',
        usuario=current_user 
    )

@app.route('/horarios')
@login_required
def lista_horarios():
    try:
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("""
            SELECT 
                h.*,
                u.Nombres,
                u.Apellidos
            FROM 
                horario h
            JOIN 
                usuario u ON h.IdUsuario = u.IdUsuario
            ORDER BY 
                h.FechaInicio DESC
        """)
        horarios = cur.fetchall()
        cur.close()

        for h in horarios:
            h['NombreUsuario'] = f"{h['Nombres']} {h['Apellidos']}"
            
        return render_template('horarios/gestion_horarios.html', horarios=horarios)
        
    except Exception as e:
        print(f"Error al cargar horarios: {e}")
        flash("Ocurrió un error al cargar la lista de horarios.", 'danger')
        return render_template('horarios/list_horarios.html', horarios=horarios)
    
@app.route('/horarios/add', methods=['GET', 'POST'])
@login_required
def add_horario():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        cur.execute("""
            INSERT INTO horario (IdUsuario, FechaInicio, FechaFin, HoraEntradaP, HoraSalidaP, DescansoP, TipoJornada)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form['IdUsuario'], request.form['FechaInicio'], request.form['FechaFin'],
            request.form['HoraEntradaP'], request.form['HoraSalidaP'],
            request.form['DescansoP'], request.form['TipoJornada']
        ))
        db.connection.commit()
        flash("Horario agregado correctamente.")
        return redirect(url_for('lista_horarios'))
    cur.execute("SELECT IdUsuario, Nombres, Apellidos FROM usuario")
    usuarios_registrados = cur.fetchall()
    return render_template('horarios/add_horario.html', usuarios=usuarios_registrados)

@app.route('/horarios/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_horario(id):
    if current_user.IdRol != 9:
        flash("Acceso denegado. Solo administradores pueden editar horarios.", "danger")
        return redirigir_error_rol()
        
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        try:
            id_usuario = request.form['IdUsuario']
            fecha_inicio = request.form['FechaInicio']
            fecha_fin = request.form['FechaFin']
            hora_entrada = request.form['HoraEntradaP']
            hora_salida = request.form['HoraSalidaP']
            descanso = request.form['DescansoP']
            tipo_jornada = request.form['TipoJornada']

            cur.execute("""
                UPDATE horario SET IdUsuario=%s, FechaInicio=%s, FechaFin=%s, HoraEntradaP=%s, HoraSalidaP=%s,
                DescansoP=%s, TipoJornada=%s WHERE IdHorario=%s
            """, (
                id_usuario, fecha_inicio, fecha_fin, hora_entrada, hora_salida,
                descanso, tipo_jornada, id
            ))
            db.connection.commit()
            flash(f"Horario ID {id} actualizado correctamente.", 'success')
            return redirect(url_for('lista_horarios'))
        except Exception as e:
            flash(f"Error al actualizar el horario: {e}", 'danger')
            return redirect(url_for('edit_horario', id=id)) 
            
    cur.execute("""
        SELECT h.*, u.Nombres, u.Apellidos 
        FROM horario h 
        JOIN usuario u ON h.IdUsuario = u.IdUsuario
        WHERE h.IdHorario=%s
    """, (id,))
    horario = cur.fetchone()
    cur.close()

    if horario is None:
        flash("El horario no existe.", 'danger')
        return redirect(url_for('lista_horarios'))

    return render_template('horarios/edit_horario.html', horario=horario)

@app.route('/horarios/delete/<int:id>')
@login_required
def delete_horario(id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM horario WHERE IdHorario=%s", (id,))
    db.connection.commit()
    flash("Horario eliminado correctamente.")
    return redirect(url_for('lista_horarios'))

@app.route('/horarios/empleado')
@login_required
def horarios_empleado():
    if current_user.IdRol == 9:
         return redirect(url_for('horarios_admin'))
         
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM horario WHERE IdUsuario=%s", (current_user.IdUsuario,))
    data = cur.fetchall()
    return render_template('horarios/horarios_empleado.html', horarios=data)

@app.route('/horarios/admin')
@login_required
def horarios_admin():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT h.*, u.Nombres, u.Apellidos FROM horario h JOIN usuario u ON h.IdUsuario=u.IdUsuario")
    data = cur.fetchall()
    return render_template('horarios/horarios_admin.html', horarios=data)

@app.route('/asistencia')
@login_required
def lista_asistencia():
    cur = None
    
    if current_user.IdRol != 9:
        return redirect(url_for('historial_asistencia_empleado')) 

    try:
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT a.*, u.Nombres, u.Apellidos 
            FROM asistencia a
            LEFT JOIN usuario u ON a.IdUsuario = u.IdUsuario
            ORDER BY a.Fecha DESC, a.HoraEntrada DESC
        """
        cur.execute(query)
        data = cur.fetchall()
        
        print(f"DEBUG: Asistencias ADMIN encontradas: {len(data)}")
        
        return render_template('asistencia/lista_asistencia_admin.html', asistencias=data)
        
    except Exception as e:
        print(f"Error al cargar lista de asistencia para admin: {e}")
        flash("Error al cargar la lista de asistencias.", 'danger')
        return render_template('asistencia/lista_asistencia_admin.html', asistencias=[])
    finally:
        if cur is not None:
            try:
                cur.close() 
            except Exception as e_close:
                print(f"Advertencia: Error al intentar cerrar el cursor: {e_close}")

@app.route('/asistencia/historial')
@login_required
def historial_asistencia_empleado():
    cur = None
    try:
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        
        query = """
            SELECT * FROM asistencia 
            WHERE IdUsuario = %s 
            ORDER BY Fecha DESC, HoraEntrada DESC
        """
        user_id = current_user.IdUsuario
        
        cur.execute(query, (user_id,))  
        historial = cur.fetchall()
        
        print(f"DEBUG: Consultando asistencias para IdUsuario: {user_id}")
        print(f"DEBUG: Registros de historial encontrados: {len(historial)}")
        
        return render_template('asistencia/empleado_historial_asistencia.html', 
                               historial=historial)
                                
    except Exception as e:
        print(f"Error al cargar historial de asistencia del empleado {current_user.IdUsuario}: {e}")
        flash("Ocurrió un error al cargar tu historial de asistencia.", 'danger')
        return render_template('asistencia/empleado_historial_asistencia.html', historial=[])
    finally:
        if cur is not None:
            try:
                cur.close() 
            except Exception as e_close:
                print(f"Advertencia: Error al intentar cerrar el cursor: {e_close}")
    
@app.route('/asistencia/add', methods=['GET', 'POST'])
@login_required
def add_asistencia():
    if request.method == 'POST':
        cur = None
        try:
            cur = db.connection.cursor()
            
            id_usuario = current_user.IdUsuario
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora_entrada = datetime.now().strftime('%H:%M:%S')
            hora_salida = None
            descanso = None
            estado = 'Entrada Registrada'

            cur.execute(
                "SELECT IdAsistencia FROM asistencia WHERE IdUsuario = %s AND Fecha = %s AND HoraEntrada IS NOT NULL",
                (id_usuario, fecha)
            )
            if cur.fetchone():
                flash("Ya has registrado tu entrada el día de hoy.", 'warning')
                return redirect(url_for('historial_asistencia_empleado'))

            cur.execute("""
                INSERT INTO asistencia (IdUsuario, Fecha, HoraEntrada, HoraSalida, Descanso, Estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_usuario, fecha, hora_entrada, hora_salida, descanso, estado
            ))
            
            db.connection.commit()
            flash("Entrada registrada correctamente.", 'success')
            return redirect(url_for('historial_asistencia_empleado'))
            
        except Exception as e:
            print(f"ERROR al registrar asistencia: {e}")
            flash("Ocurrió un error al registrar la asistencia.", 'danger')
            return redirect(url_for('historial_asistencia_empleado'))
            
        finally:
            if cur is not None:
                cur.close()

    return render_template('asistencia/add_asistencia.html')

@app.route('/asistencia/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asistencia(id):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        cur.execute("""
            UPDATE asistencia SET Fecha=%s, HoraEntrada=%s, HoraSalida=%s, Descanso=%s, Estado=%s
            WHERE IdAsistencia=%s
        """, (
            request.form['Fecha'], request.form['HoraEntrada'],
            request.form['HoraSalida'], request.form['Descanso'], request.form['Estado'], id
        ))
        db.connection.commit()
        flash("Asistencia actualizada correctamente.")
        return redirect(url_for('lista_asistencia'))
    cur.execute("SELECT * FROM asistencia WHERE IdAsistencia=%s", (id,))
    asistencia = cur.fetchone()
    return render_template('asistencia/edit_asistencia.html', asistencia=asistencia)

@app.route('/asistencia/delete/<int:id>')
@login_required
def delete_asistencia(id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM asistencia WHERE IdAsistencia=%s", (id,))
    db.connection.commit()
    flash("Asistencia eliminada correctamente.")
    return redirect(url_for('lista_asistencia'))

@app.route('/reportes/asistencia', methods=['GET'])
@login_required
def reportes_asistencia():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    usuario_id = request.args.get('usuario_id')
    fecha_inicio_html = request.args.get('fecha_inicio') 
    fecha_fin_html = request.args.get('fecha_fin') 

    try:
        asistencias = get_filtered_asistencias(cur, usuario_id, fecha_inicio_html, fecha_fin_html)
    except Exception as e:
        flash("Error al generar el reporte de asistencias.", 'danger')
        print(f"ERROR: {e}")
        asistencias = []

    try:
        cur.execute("SELECT IdUsuario, Nombres, Apellidos FROM usuario ORDER BY Apellidos, Nombres")
        all_users = cur.fetchall()
    except Exception as e:
        print(f"Error al cargar la lista de usuarios para el filtro: {e}")
        all_users = []

    estados = {'Presente': len(asistencias), 'Falta': 0} 
    horas = {'Empleado A': 8, 'Empleado B': 7.5}
    por_dia = {'2025-01-01': 5, '2025-01-02': 7}
    
    cur.close()

    return render_template('reportes/reportes_asistencia.html', 
                           asistencias=asistencias,
                           all_users=all_users,
                           current_user_id=usuario_id,
                           fecha_inicio=fecha_inicio_html,
                           fecha_fin=fecha_fin_html,
                           estados=estados,
                           horas=horas,
                           por_dia=por_dia
                          )

@app.route('/reportes/asistencia/csv')
@login_required
def export_csv():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    usuario_id = request.args.get('usuario_id')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    try:
        data = get_filtered_asistencias(cur, usuario_id, fecha_inicio, fecha_fin)
    except Exception as e:
        flash("Error al generar el CSV.", 'danger')
        print(f"ERROR CSV: {e}")
        return redirect(url_for('reportes_asistencia'))
        
    cur.close()
    
    if not data:
        flash("No hay datos filtrados para exportar en CSV.", 'info')
        return redirect(url_for('reportes_asistencia'))

    output = io.StringIO()
    writer = csv.writer(output)
    
    header = ['ID Asistencia', 'Fecha', 'Hora Entrada', 'Hora Salida', 'Descanso', 'Estado', 'ID Empleado', 'Nombres', 'Apellidos']
    writer.writerow(header)
    
    for row in data:
        writer.writerow([
            row['IdAsistencia'],
            row['Fecha'],
            row['HoraEntrada'],
            row['HoraSalida'],
            row['Descanso'],
            row['Estado'],
            row['IdUsuario'],
            row['Nombres'],
            row['Apellidos']
        ])
        
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=asistencia_reporte_filtrado.csv'
    return response


@app.route('/reportes/asistencia/pdf')
@login_required
def export_pdf():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    usuario_id = request.args.get('usuario_id')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    try:
        data = get_filtered_asistencias(cur, usuario_id, fecha_inicio, fecha_fin)
    except Exception as e:
        flash("Error al generar el PDF.", 'danger')
        print(f"ERROR PDF: {e}")
        return redirect(url_for('reportes_asistencia'))
        
    cur.close()
    
    if not data:
        flash("No hay datos filtrados para exportar en PDF.", 'info')
        return redirect(url_for('reportes_asistencia'))

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.drawString(50, 750, "REPORTE DE ASISTENCIA FILTRADO")
    p.drawString(50, 735, f"Filtro: Usuario ID={usuario_id or 'Todos'}, Desde={fecha_inicio or 'Inicio'}, Hasta={fecha_fin or 'Fin'}")

    headers = ["ID", "Empleado", "Fecha", "Entrada", "Salida", "Estado"]
    col_widths = [50, 150, 70, 70, 70, 100]
    x_pos = 50
    y = 700
    
    for i, header in enumerate(headers):
        p.drawString(x_pos, y, header)
        x_pos += col_widths[i]
    
    y -= 15
    p.line(50, y, sum(col_widths) + 50, y) 
    y -= 15

    for row in data:
        if y < 50: 
            p.showPage()
            y = 750
            p.drawString(50, 735, "Continuación del Reporte")
            y = 700
            
        x_pos = 50
        p.drawString(x_pos, y, str(row['IdAsistencia']))
        x_pos += col_widths[0]
        p.drawString(x_pos, y, f"{row['Nombres']} {row['Apellidos']}")
        x_pos += col_widths[1]
        p.drawString(x_pos, y, str(row['Fecha']))
        x_pos += col_widths[2]
        p.drawString(x_pos, y, str(row['HoraEntrada']))
        x_pos += col_widths[3]
        p.drawString(x_pos, y, str(row['HoraSalida']))
        x_pos += col_widths[4]
        p.drawString(x_pos, y, row['Estado'])
        
        y -= 15
        
    p.save()
    buffer.seek(0)
    
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "attachment;filename=asistencia_reporte_filtrado.pdf"})

@app.route('/notificaciones')
def notificaciones():
    return render_template('notificaciones/notificaciones.html')

@app.route('/solicitudes')
@login_required
def solicitudes():
    """
    Redirige al usuario a la vista de Solicitudes según su Rol.
    Rol 9 (Admin) -> Aprobación/Gestión.
    Cualquier otro rol (Empleados) -> Envío/Historial.
    """
    if current_user.IdRol == 9:
        return redirect(url_for('aprobar_solicitudes_proceso'))
        
    elif current_user.IdRol >= 10: 
        return redirect(url_for('enviar_solicitudes_proceso'))
        
    return redirect(url_for('login'))

@app.route('/uploads/solicitudes/<filename>')
def descargar_adjunto(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/solicitudes/enviar', methods=['GET', 'POST'])
@login_required
def enviar_solicitudes_proceso():
    if request.method == 'POST':
        id_tipo_solicitud = request.form.get('id_tipo_solicitud')
        justificacion = request.form.get('justificacion')
        fecha_inicio = request.form.get('fecha_inicio')
        hora_inicio = request.form.get('hora_inicio')
        fecha_fin = request.form.get('fecha_fin')
        hora_fin = request.form.get('hora_fin')
        
        if not id_tipo_solicitud:
            flash("Debe seleccionar un tipo de solicitud.", "danger")
            return render_template('solicitudes/solicitud_permisos.html')

        dias_solicitados = None
        if fecha_inicio and fecha_fin:
             try:
                 fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                 fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                 dias_solicitados = (fecha_fin_dt - fecha_inicio_dt).days + 1
             except ValueError:
                 flash("Formato de fecha inválido.", "danger")
                 return render_template('solicitudes/solicitud_permisos.html')

        nombre_adjunto = None
        if 'adjunto' in request.files:
            file = request.files['adjunto']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config.get('UPLOAD_FOLDER', 'uploads'), filename)) 
                nombre_adjunto = filename

        cur = db.connection.cursor()
        cur.execute("""
             INSERT INTO solicitud (
                 IdUsuario, IdTipoSolicitud, FechaSolicitud, FechaInicio, HoraInicio,
                 FechaFin, HoraFin, DiasSolicitados, Justificacion, RutaAdjunto, Estado
             )
             VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, 'Pendiente')
        """, (
             current_user.IdUsuario, id_tipo_solicitud, fecha_inicio, hora_inicio, fecha_fin,
             hora_fin, dias_solicitados, justificacion, nombre_adjunto
        ))
        db.connection.commit()
        flash("Solicitud enviada correctamente.", "success")
        return redirect(url_for('historial_solicitudes'))

    return render_template('solicitudes/solicitud_permisos.html')

@app.route('/solicitudes/historial')
@login_required
def historial_solicitudes():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("""
            SELECT 
                s.FechaSolicitud, s.FechaInicio, s.FechaFin, s.DiasSolicitados,
                s.Justificacion, s.Estado, s.RutaAdjunto, s.IdSolicitud, s.IdUsuario, 
                ts.Nombre AS Tipo  -- Forzamos el alias como el último campo
            FROM solicitud s
            LEFT JOIN tiposolicitud ts ON ts.IdTipoSolicitud = s.IdTipoSolicitud
            WHERE s.IdUsuario = %s 
            ORDER BY s.FechaSolicitud DESC
        """, (current_user.IdUsuario,))
        historial = cur.fetchall()
    except Exception as e:
        print(f"Error al cargar historial: {e}")
        historial = []
    finally:
        cur.close()
        
    return render_template('solicitudes/historial.html', historial=historial)

@app.route('/solicitudes/aprobar', methods=['GET', 'POST'])
@login_required
def aprobar_solicitudes_proceso():
    if current_user.IdRol != 9:
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirigir_error_rol() 
        
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    solicitud_id = request.args.get('id')
    accion = request.args.get('accion')
    
    if solicitud_id and accion:
        try:
            estado = 'Aprobada' if accion == 'aprobar' else 'Rechazada'
            cur.execute("UPDATE solicitud SET Estado = %s WHERE IdSolicitud = %s", (estado, solicitud_id))
            db.connection.commit()
            flash(f"Solicitud {estado.lower()} correctamente.", "success")
        except Exception as e:
            flash(f"Error al procesar la solicitud: {e}", "danger")
        return redirect(url_for('aprobar_solicitudes_proceso'))

    cur.execute("""
        SELECT
            s.IdSolicitud, s.IdUsuario, s.FechaInicio, s.FechaFin, s.DiasSolicitados,
            s.Justificacion, s.RutaAdjunto, s.Estado, s.FechaSolicitud, 
            u.Nombres,
            u.Apellidos,
            ts.Nombre AS Tipo  -- Asegúrate de que este alias sea correcto
        FROM solicitud s
        JOIN usuario u ON u.IdUsuario = s.IdUsuario
        LEFT JOIN tiposolicitud ts ON ts.IdTipoSolicitud = s.IdTipoSolicitud
        WHERE s.Estado = 'Pendiente'
        ORDER BY s.FechaSolicitud DESC
    """)
    pendientes = cur.fetchall()
    cur.close()
    return render_template('solicitudes/aprobacion.html', pendientes=pendientes)

@app.route('/solicitudes/reportes')
@login_required
def reportes_solicitudes():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT s.*, u.Nombres, u.Apellidos FROM solicitud s JOIN usuario u ON s.IdUsuario = u.IdUsuario")
    todas_solicitudes = cur.fetchall()
    return render_template('solicitudes/reportes.html', todas_solicitudes=todas_solicitudes)

@app.route('/denuncias')
@login_required
def denuncias():
    if current_user.IdRol != 9:
        flash("Acceso denegado. No tienes permisos de administrador.", "danger")
        return redirigir_error_rol() 
        
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cur.execute("""
            SELECT d.*, u.Nombres, u.Apellidos 
            FROM denuncia d
            JOIN usuario u ON d.IdUsuario = u.IdUsuarioReportado
            ORDER BY d.FechaDenuncia DESC
        """)
        lista_denuncias = cur.fetchall()
    except Exception as e:
        flash("Error al cargar la lista de denuncias.", "danger")
        print(f"Error al cargar denuncias: {e}")
        lista_denuncias = []

    cur.close()

    return render_template('denuncias/denuncias.html', 
                           denuncias=lista_denuncias)

@app.route('/documentos')
def documentacion():
    return render_template('documentacion/documentacion.html')

@app.route('/admin/documentos/gestion') 
@login_required
def documentacion_admin():
    if current_user.IdRol != 9:
        flash("Acceso denegado.", "danger")
        return redirigir_error_rol()
        
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT COUNT(*) AS total_pendientes FROM documento WHERE EstadoAprobacion = 'Pendiente'")
    conteo_pendientes = cur.fetchone()['total_pendientes']
    
    cur.execute("""
        SELECT d.*, u.Nombres, u.Apellidos 
        FROM documento d
        JOIN usuario u ON d.IdUsuario = u.IdUsuario
        WHERE d.EstadoAprobacion = 'Pendiente'
        ORDER BY d.FechaSubida DESC
    """)
    documentos_pendientes = cur.fetchall()
    
    cur.close()

    return render_template('documentacion/documentacion_admin.html', 
                            documentos_pendientes=documentos_pendientes,
                            conteo_pendientes=conteo_pendientes)

@app.route('/documentos/aprobar_proceso', methods=['GET', 'POST'])
@login_required
def aprobar_documento_proceso():
    if current_user.IdRol != 9:
        flash("Acceso denegado. No tienes permisos de gestión de documentos.", "danger")
        return redirigir_error_rol()

    cur = db.connection.cursor()
    documento_id = request.form.get('id')
    accion = request.form.get('accion')
    justificacion = request.form.get('justificacion')

    if documento_id and accion:
        try:
            estado = 'Aprobado' if accion == 'aprobar' else 'Rechazado'

            cur.execute("""
                UPDATE documento 
                SET EstadoAprobacion = %s, JustificacionAdmin = %s
                WHERE IdDocumento = %s
            """, (estado, justificacion, documento_id))
            
            db.connection.commit()
            flash(f"Documento procesado: {estado}.", "success")
            
        except Exception as e:
            db.connection.rollback()
            flash(f"Error al procesar el documento: {e}", "danger")
            
        return redirect(url_for('documentacion_admin')) 

    flash("Acción inválida o incompleta.", "warning")
    return redirect(url_for('documentacion_admin'))

@app.route('/canal/procesar', methods=['POST'])
@login_required
def procesar_publicacion():
    if current_user.IdRol != 9:
        flash("Acceso denegado. No tienes permisos para gestionar publicaciones.", "danger")
        return redirect(url_for('canal_admin'))

    id_publicacion = request.form.get('id_publicacion') 
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    fecha_publicacion = request.form.get('fecha_publicacion')
    fecha_vigencia = request.form.get('fecha_vigencia')
    estado = request.form.get('estado')
    
    id_usuario_autor = current_user.IdUsuario

    if not titulo or not contenido or not estado:
        flash("Faltan datos obligatorios (Título, Contenido, Estado).", "danger")
        return redirect(url_for('canal_admin'))

    cur = db.connection.cursor()
    
    try:
        if id_publicacion:
            cur.execute("""
                UPDATE noticia  
                SET 
                    Titulo = %s, 
                    Contenido = %s, 
                    FechaPublicacion = %s,
                    FechaVigencia = %s,
                    Estado = %s,
                    FechaModificacion = NOW()
                WHERE IdNoticia = %s
            """, (titulo, contenido, fecha_publicacion or None, fecha_vigencia or None, estado, id_publicacion))
            
            db.connection.commit()
            flash(f"Publicación '{titulo}' actualizada correctamente.", "success")
            
        else:
            cur.execute("""
                INSERT INTO noticia  
                    (IdUsuario, Titulo, Contenido, FechaPublicacion, FechaVigencia, Estado, FechaCreacion)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, NOW())
            """, (id_usuario_autor, titulo, contenido, fecha_publicacion or None, fecha_vigencia or None, estado))
            
            db.connection.commit()
            flash(f"Publicación '{titulo}' creada exitosamente. Estado: {estado}.", "success")

    except Exception as e:
        db.connection.rollback()
        flash(f"Error al procesar la publicación: {e}", "danger")
        
    return redirect(url_for('canal_admin'))

@app.route('/canal/eliminar', methods=['GET'])
@login_required
def eliminar_publicacion(): 

    if current_user.IdRol != 9:
        flash("Acceso denegado. No tienes permisos para eliminar publicaciones.", "danger")
        return redirect(url_for('canal_admin'))

    publicacion_id = request.args.get('id')
    
    if publicacion_id:
        try:
            cur = db.connection.cursor()
            
            cur.execute("DELETE FROM noticia WHERE IdNoticia = %s", (publicacion_id,)) 

            db.connection.commit()
            flash(f"Publicación #{publicacion_id} eliminada definitivamente.", "success")
            
        except Exception as e:
            db.connection.rollback()
            flash(f"Error al intentar eliminar la publicación: {e}", "danger")
    else:
        flash("ID de publicación no proporcionado.", "warning")
        
    return redirect(url_for('canal_admin'))

@app.route('/canal/admin')
@login_required
def canal_admin():
    if current_user.IdRol != 9:
        flash("Acceso denegado.", "danger")
        return redirect(url_for('ver_noticias_vendedora'))

    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    query = """
        SELECT n.IdNoticia, n.Titulo, n.Contenido, n.FechaPublicacion, n.FechaVigencia, n.Estado, 
               u.Nombres AS Autor, n.FechaCreacion, n.FechaModificacion
        FROM noticia n
        JOIN Usuario u ON n.IdUsuario = u.IdUsuario
        ORDER BY n.FechaCreacion DESC
    """
    cur.execute(query)
    publicaciones = cur.fetchall()
    cur.close()

    activas = [p for p in publicaciones if p['Estado'] == 'Activa']
    borradores = [p for p in publicaciones if p['Estado'] == 'Borrador']
    archivadas = [p for p in publicaciones if p['Estado'] == 'Archivada']

    return render_template('noticias/canal_admin.html',
                           publicaciones_activas=activas,
                           publicaciones_borradores=borradores,
                           publicaciones_archivadas=archivadas)

@app.route('/noticias') 
@login_required
def ver_noticias_vendedora():
    ADMIN_ROLE_ID = 9 

    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    query = """
        SELECT n.Titulo, n.Contenido, DATE_FORMAT(n.FechaPublicacion, '%%d-%m-%Y') AS FechaPublicacion
        FROM noticia n
        JOIN Usuario u ON n.IdUsuario = u.IdUsuario
        WHERE n.Estado = 'Activa' 
        AND u.IdRol = %s 
        ORDER BY n.FechaPublicacion DESC
    """
    cur.execute(query, (ADMIN_ROLE_ID,))
    noticias_activas = cur.fetchall()
    cur.close()

    return render_template('gestion_noticias_vendedora.html', noticias_activas=noticias_activas)

from flask import render_template, session, redirect, url_for, flash

@app.route('/canal-de-noticias-vendedora') 
def canal():

    if 'rol' not in session or session.get('rol') != 'Vendedora':
        flash('Acceso no autorizado.', 'warning')
        return redirect(url_for('login'))

    return render_template('canal_admin.html')

@app.route('/cartera/registrar_pago', methods=['POST'])
@login_required
def registrar_pago_proceso():
    """Procesa el formulario del modal para registrar el pago de una cuenta pendiente."""

    if current_user.IdRol not in [9, 12]: 
        flash("Acceso denegado. No tienes permisos para registrar pagos.", "danger")
        return redirigir_error_rol()

    id_factura = request.form.get('id_factura')
    monto_pagado = request.form.get('monto_pagado')
    metodo_pago = request.form.get('metodo_pago')
    referencia = request.form.get('referencia')
    
    if not id_factura or not monto_pagado or not metodo_pago:
        flash("Faltan datos obligatorios para registrar el pago.", "danger")
        return redirect(url_for('gestion_cobro'))

    try:
        cur = db.connection.cursor()
        
        cur.execute("""
            UPDATE pedido 
            SET 
                EstadoPago = 'Pagado',
                FechaPago = NOW(),
                MontoPagado = %s,
                MetodoPago = %s,
                ReferenciaPago = %s
            WHERE IdPedido = %s
        """, (monto_pagado, metodo_pago, referencia, id_factura))
        
        db.connection.commit()
        flash(f"Pago registrado correctamente para el Pedido/Factura #{id_factura}.", "success")
        
    except Exception as e:
        db.connection.rollback()
        flash(f"Error al registrar el pago: {e}", "danger")

    return redirect(url_for('gestion_cobro'))


@app.route('/gestion_cobro')
@login_required
def gestion_cobro():
    cur = None

    es_admin_o_contadora = current_user.IdRol in [9, 12]

    base_query = """
        SELECT * FROM pedido p
        WHERE p.EstadoPago != 'Pagado'
    """
    
    params = ()

    if es_admin_o_contadora:
        query = base_query + " ORDER BY p.FechaPedido DESC"
        template_name = 'cartera/cobro_cartera_admin.html'
        
    elif current_user.IdRol == 11:
        query = base_query + " AND p.IdUsuarioVendedora_ERROR = %s ORDER BY p.FechaPedido DESC" 
        params = (current_user.IdUsuario,) 
        template_name = 'cartera/cobro_cartera_vendedora.html'
        
    else:
        flash("No tienes permiso para acceder a esta sección de cartera.", "danger")
        return redirigir_error_rol()

    try:
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query, params)
        cartera_cobro = cur.fetchall()

        return render_template(template_name, cartera=cartera_cobro)
        
    except Exception as e:
        print(f"--- ERROR CRÍTICO AL CARGAR CARTERA (Rol {current_user.IdRol}) ---")
        print(f"Consulta ejecutada: {query}")
        print(f"Error detallado: {e}")
        print("-----------------------------------------------------------------")
        
        flash("Error al cargar la cartera de cobro. Verifique la conexión o el nombre de columna.", "danger")
        
        if current_user.IdRol == 11:
            return render_template('cartera/cobro_cartera_vendedora.html', cartera=[])
        else:
            return render_template('cartera/cobro_cartera_admin.html', cartera=[])
            
    finally:
        if cur is not None:
            try: cur.close() 
            except Exception: pass

@app.route('/manual')
def manual():
    return render_template('manual/manual.html')

@app.route('/reglas')
def reglas():
    return render_template('reglas/reglas.html')

@app.route('/admin/monitoreo') 
@login_required
def monitoreo():
    """Renderiza el dashboard de monitoreo para el administrador."""
    if current_user.IdRol != 9:
        flash("Acceso denegado.", "danger")
        return redirigir_error_rol()

    return render_template('monitoreo/monitoreo.html') 

@app.route('/api/monitoreo_data', methods=['GET'])
@login_required
def monitoreo_data():
    """Consulta datos clave de la DB y los retorna como JSON."""
    if current_user.IdRol != 9:
        return jsonify({"error": "Acceso denegado"}), 403

    try:
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("SELECT COUNT(IdUsuario) AS total_usuarios FROM usuario WHERE Activo = TRUE") 
        usuarios_activos = cur.fetchone()['total_usuarios']

        cur.execute("SELECT COUNT(*) AS total_pendientes FROM documento WHERE Estado = 'Pendiente'")
        documentos_pendientes = cur.fetchone()['total_pendientes']

        cur.execute("SELECT COUNT(*) AS total_solicitudes FROM solicitud WHERE Estado = 'Pendiente'")
        solicitudes_pendientes = cur.fetchone()['total_solicitudes']

        cur.execute("""
            SELECT 
                s.IdSolicitud, u.Nombres, u.Apellidos, s.FechaSolicitud, s.Justificacion 
            FROM solicitud s
            JOIN usuario u ON u.IdUsuario = s.IdUsuario
            WHERE s.Estado = 'Pendiente'
            ORDER BY s.FechaSolicitud DESC
            LIMIT 5
        """)
        logs_pendientes = cur.fetchall()

        data = {
            "usuarios_activos": usuarios_activos,
            "documentos_pendientes": documentos_pendientes,
            "solicitudes_pendientes": solicitudes_pendientes,
            "logs_pendientes": logs_pendientes
        }
        
        cur.close()
        
        return jsonify(data)

    except Exception as e:
        print(f"Error al obtener datos de monitoreo: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
    
@app.route('/horas_extra')
def horas_extra():
    return render_template('extras/horas_extra.html')

@app.route('/historial_asistencia')
@login_required
def historial_asistencia():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM asistencia WHERE IdUsuario = %s ORDER BY Fecha DESC, HoraEntrada DESC", (current_user.IdUsuario,))
    historial_asistencia = cur.fetchall()
    if current_user.IdRol != 10:
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for('dashboard_admin'))
    return render_template('extras/historial_asistencia.html', asistencias=historial_asistencia)

@app.route('/cartera')
@login_required
def cartera():
    return render_template('cartera/cartera.html')

@app.route('/pedidos_pagos')
@login_required
def pedidos_pagos():
    return render_template('pedidos/pedidos_pagos.html')

@app.route('/encuestas/crear', methods=['GET', 'POST'])
def crear_encuesta():
    """Maneja la creación y configuración de la estructura de la encuesta."""
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombreEncuesta')
            descripcion = request.form.get('descripcionEncuesta')
            tipo = request.form.get('tipoEncuesta')
            fecha_cierre_str = request.form.get('fechaLimite')

            if not nombre or not tipo:
                flash('El nombre y el tipo de encuesta son obligatorios.', 'danger')
                return redirect(url_for('crear_encuesta'))

            fecha_cierre = None
            if fecha_cierre_str:
                 fecha_cierre = datetime.strptime(fecha_cierre_str, '%Y-%m-%d').date()

            preguntas_procesadas = {}

            for key, value in request.form.items():
                if key.startswith('questions['):

                    try:
                        q_id = key.split('[')[1].split(']')[0] 
                        
                        if q_id not in preguntas_procesadas:
                            preguntas_procesadas[q_id] = {'options': []}
                            
                        if key.endswith('[options][]'):
                            preguntas_procesadas[q_id]['options'].append(value)
                        else:
                            field = key.split('[')[2].split(']')[0]
                            preguntas_procesadas[q_id][field] = value
                    except IndexError:
                        continue

            print(f"DEBUG: Guardando Encuesta '{nombre}'. Preguntas: {len(preguntas_procesadas)}")

            flash(f'Encuesta "{nombre}" creada con éxito. Ahora puedes asignarla.', 'success')

            return redirect(url_for('asignar_encuesta'))

        except Exception as e:
            print(f"ERROR: Falló el guardado de la encuesta: {e}")
            flash('Error grave al procesar y guardar la encuesta. Revisa los logs del servidor.', 'danger')
            return redirect(url_for('crear_encuesta'))

    return render_template('encuestas/crear_encuesta.html', title='Crear Encuesta', base='base_admin.html')

@app.route('/encuestas/asignar', methods=['GET', 'POST'])
def asignar_encuesta():
    """Maneja la asignación de encuestas a usuarios."""

    if request.method == 'POST':
        try:
            encuesta_id = request.form.get('encuesta_seleccionada')
            usuarios_ids = request.form.getlist('usuarios_a_asignar') 
            grupos_ids = request.form.getlist('grupos_a_asignar')     

            if not encuesta_id:
                flash('Debe seleccionar una encuesta para asignar.', 'danger')
                return redirect(url_for('asignar_encuesta'))
            
            if not usuarios_ids and not grupos_ids:
                flash('Debe seleccionar al menos un usuario o un grupo.', 'danger')
                return redirect(url_for('asignar_encuesta'))

            print(f"DEBUG: Asignando Encuesta ID {encuesta_id} a {len(usuarios_ids)} usuarios y {len(grupos_ids)} grupos.")

            flash('Encuesta asignada y notificaciones enviadas con éxito.', 'success')

            return redirect(url_for('dashboard_admin')) 

        except Exception as e:
            print(f"ERROR: Falló la asignación de la encuesta: {e}")
            flash('Error al asignar la encuesta. Inténtalo de nuevo.', 'danger')
            return redirect(url_for('asignar_encuesta'))
    
    try:
        encuestas = [
            {'id': 1, 'nombre': 'Clima Laboral Q4'}, 
            {'id': 2, 'nombre': 'Desempeño Anual'}
        ]
        empleados = [
            {'id': 101, 'nombre': 'Juan Pérez (Ventas)'}, 
            {'id': 102, 'nombre': 'Ana Gómez (Marketing)'}
        ]
        grupos = [
            {'id': 1, 'nombre': 'Departamento de IT'}, 
            {'id': 2, 'nombre': 'Equipo Directivo'}
        ]
        
    except Exception as e:
        print(f"ERROR al cargar datos para asignación: {e}")
        flash('No se pudieron cargar los datos necesarios para la asignación.', 'danger')
        return redirect(url_for('dashboard_admin'))

    return render_template(
        'encuestas/asignar_encuesta.html', 
        title='Asignar Encuestas', 
        base='base_admin.html',
        encuestas=encuestas,
        empleados=empleados,
        grupos=grupos
    )

@app.route('/encuestas/revision', methods=['GET'])
def revision_encuestas():
    """Permite al Admin/Supervisor revisar encuestas completadas y añadir comentarios."""
    return render_template('encuestas/revision_encuestas.html', title='Revisión de Encuestas', base='base_admin.html')

@app.route('/mis_encuestas')
@login_required
def mis_encuestas():
    if current_user.IdRol == 9:
        base_template = 'base_admin.html'
    else:
        base_template = 'base_vendedora.html' 
        
    if not current_user.is_authenticated:
        flash('Necesitas iniciar sesión para ver tus encuestas.', 'warning')
        return redirect(url_for('login'))

    cur = None
    datos_asignacion = []

    try:
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        
        query = """
            SELECT e.NombreEncuesta, ea.Estado, ea.FechaLimite, ea.IdAsignacion
            FROM encuesta_asignacion ea
            JOIN encuesta e ON ea.IdEncuesta = e.IdEncuesta
            WHERE ea.IdUsuario = %s
            ORDER BY ea.Estado, ea.FechaLimite DESC
        """
        
        cur.execute(query, (current_user.IdUsuario,))
        datos_asignacion_raw = cur.fetchall()
        
        datos_asignacion = [
            {'id': r['IdAsignacion'], 
             'nombre_encuesta': r['NombreEncuesta'], 
             'estado': r['Estado'], 
             'fecha_limite': r['FechaLimite'], 
             'url_responder': url_for('responder_encuesta', asignacion_id=r['IdAsignacion'])}
            for r in datos_asignacion_raw
        ]
        
        encuestas = {
            'pendientes': [e for e in datos_asignacion if e['estado'] == 'Pendiente'],
            'en_curso': [e for e in datos_asignacion if e['estado'] == 'En Curso'],
            'completadas': [e for e in datos_asignacion if e['estado'] == 'Completada'],
        }
        
    except Exception as e:
        print(f"ERROR: Falló la consulta de encuestas asignadas: {e}")
        flash('No pudimos cargar tu lista de encuestas. Inténtalo más tarde.', 'danger')
        encuestas = {'pendientes': [], 'en_curso': [], 'completadas': []}
    
    finally:
        if cur is not None:
            cur.close()
            
    return render_template(
        'encuestas/mis_encuestas.html', 
        title='Mis Encuestas',
        encuestas=encuestas,
        total_pendientes=len(encuestas['pendientes']),
        base=base_template
    )

def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404
if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)