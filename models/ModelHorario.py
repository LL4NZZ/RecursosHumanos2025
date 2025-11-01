from .entities.Horario import Horario

class ModelHorario:
    @classmethod
    def get_all(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT h.id, h.empleado_id, e.Nombre, h.dia_semana, h.hora_inicio, h.hora_fin
                     FROM horarios h
                     JOIN empleados e ON h.empleado_id = e.id"""
            cursor.execute(sql)
            data = cursor.fetchall()
            horarios = []
            for row in data:
                horario = {
                    'id': row[0],
                    'empleado_id': row[1],
                    'empleado_nombre': row[2],
                    'dia_semana': row[3],
                    'hora_inicio': str(row[4]),
                    'hora_fin': str(row[5])
                }
                horarios.append(horario)
            return horarios
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add(cls, db, horario: Horario):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO horarios (empleado_id, dia_semana, hora_inicio, hora_fin)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (horario.empleado_id, horario.dia_semana, horario.hora_inicio, horario.hora_fin))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM horarios WHERE id = %s"
            cursor.execute(sql, (id,))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
