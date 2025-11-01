from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, IdUsuario, IdRol, Nombres, Apellidos, TipoDocumento, Documento, Correo,
                 CorreoCorporativo, FechaContratacion, FechaNacimiento, Telefono, Contrasena, Estado):
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

    def get_id(self):
        return str(self.IdUsuario)

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
