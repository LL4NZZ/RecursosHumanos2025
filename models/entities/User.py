from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
<<<<<<< HEAD
    def __init__(self, IdUsuario, IdRol, Nombres, Apellidos, TipoDocumento, Documento, Correo, CorreoCorporativo, FechaContratacion, FechaNacimiento, Telefono, Contrasena, Estado, NombreRol):
        
        # Asignación de atributos
=======
    def __init__(self, IdUsuario, IdRol, Nombres, Apellidos, TipoDocumento, Documento, Correo,
                 CorreoCorporativo, FechaContratacion, FechaNacimiento, Telefono, Contrasena, Estado):
>>>>>>> 851cf041461ac8b5ee8a6c766ed25477410b4757
        self.IdUsuario = IdUsuario
        self.IdRol = IdRol
        self.Nombres = Nombres
        self.Apellidos = Apellidos
        self.TipoDocumento = TipoDocumento
        self.Documento = Documento
        self.Correo = Correo
        self.CorreoCorporativo = CorreoCorporativo
        self.FechaContratacion = FechaContratacion
        self.FechaNacimiento = FechaNacimiento
        self.Telefono = Telefono
        self.Contrasena = Contrasena
        self.Estado = Estado
<<<<<<< HEAD
        self.NombreRol = NombreRol 

    # 🌟 CORRECCIÓN 1: La propiedad 'id' debe estar DECORADA e indentada DENTRO de la clase.
    @property
    def id(self):
        """Retorna el IdUsuario (como string), cumpliendo con el requisito de Flask-Login (propiedad 'id')."""
        return str(self.IdUsuario)

    # Nota: Flask-Login usa la propiedad 'id', pero 'get_id' es el método heredado de UserMixin.
    # Es redundante si 'id' existe, pero se mantiene si se usa en otro lugar.
    def get_id(self):
        """Método heredado de UserMixin."""
        return str(self.IdUsuario)

    @staticmethod
    def check_password(hashed_password, password): 
        """Verifica que la contraseña proporcionada coincida con el hash almacenado.
        
        Nota: Se usa @staticmethod porque no necesita acceder a 'self' (instancia) ni a 'cls' (clase).
        """
        return check_password_hash(hashed_password, password)

    def is_admin(self):
        """Método auxiliar para verificar si el usuario es administrador."""
        return self.IdRol == 9
=======

    def get_id(self):
        return str(self.IdUsuario)

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
>>>>>>> 851cf041461ac8b5ee8a6c766ed25477410b4757
