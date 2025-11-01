from .entities.User import User

class ModelUser:

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT IdUsuario, IdRol, Nombres, Apellidos, TipoDocumento, Documento, Correo,
                     CorreoCorporativo, FechaContratacion, FechaNacimiento, Telefono, Contrasena, Estado
                     FROM usuario WHERE Correo = %s"""
            cursor.execute(sql, (user.Correo,))
            row = cursor.fetchone()

            if row:
                return User(row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT IdUsuario, IdRol, Nombres, Apellidos, TipoDocumento, Documento, Correo,
                     CorreoCorporativo, FechaContratacion, FechaNacimiento, Telefono, Estado
                     FROM usuario WHERE IdUsuario = %s"""
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                return User(row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6], row[7], row[8], row[9], row[10], None, row[11])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
