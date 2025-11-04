# --- INICIO DEL ARCHIVO: models/ModelUser.py ---

# 🌟 CORRECCIÓN 1: Asegurar que la librería se importa correctamente aquí 🌟
import MySQLdb.cursors 
from models.entities.User import User 
# También necesitas importar la referencia a la clase User si no lo has hecho ya

class ModelUser(object):
    
    # ----------------------------------------------------
    # 1. FUNCIÓN DE CARGA POR ID (usada por Flask-Login)
    # ----------------------------------------------------
    @classmethod
    def get_by_id(cls, db, IdUsuario):
        try:
            # Uso correcto del DictCursor
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            
            sql = """
                SELECT 
                    u.*, 
                    r.NombreRol as NombreRol  
                FROM 
                    usuario u 
                JOIN 
                    rol r ON u.IdRol = r.IdRol 
                WHERE 
                    u.IdUsuario = %s
            """
            cur.execute(sql, (IdUsuario,))
            row = cur.fetchone() 

            if row is not None:
                # Se pasan los 14 argumentos (12 + Estado + NombreRol)
                user = User(
                    row['IdUsuario'], 
                    row['IdRol'],
                    row['Nombres'], 
                    row['Apellidos'], 
                    row['TipoDocumento'], 
                    row['Documento'], 
                    row['Correo'], 
                    row['CorreoCorporativo'], 
                    row['FechaContratacion'], 
                    row['FechaNacimiento'], 
                    row['Telefono'], 
                    row['Contrasena'], 
                    row['Estado'],          # Campo 13: Estado
                    row['NombreRol']        # Campo 14: NombreRol
                )
                return user
            return None
        except Exception as ex:
            raise Exception(ex)

    # ----------------------------------------------------
    # 2. FUNCIÓN DE LOGIN (usada al iniciar sesión)
    # ----------------------------------------------------
    @classmethod
    def login(cls, db, user):
        try:
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            
            sql = """
                SELECT 
                    u.*, 
                    r.NombreRol as NombreRol  
                FROM 
                    usuario u 
                JOIN 
                    rol r ON u.IdRol = r.IdRol 
                WHERE 
                    u.Correo = %s
            """
            cur.execute(sql, (user.Correo,))
            row = cur.fetchone()

            if row is not None:
                # Se pasan los 14 argumentos
                logged_user = User(
                    row['IdUsuario'], 
                    row['IdRol'],
                    row['Nombres'], 
                    row['Apellidos'], 
                    row['TipoDocumento'], 
                    row['Documento'], 
                    row['Correo'], 
                    row['CorreoCorporativo'], 
                    row['FechaContratacion'], 
                    row['FechaNacimiento'], 
                    row['Telefono'], 
                    row['Contrasena'], 
                    row['Estado'],          # Campo 13: Estado
                    row['NombreRol']        # Campo 14: NombreRol
                )
                
                # 🌟 CORRECCIÓN 2: Llama al método de clase sin problemas (asumiendo User.py ya fue corregido a 'cls')
                if User.check_password(row['Contrasena'], user.Contrasena):
                    return logged_user
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

# --- FIN DEL ARCHIVO: models/ModelUser.py ---