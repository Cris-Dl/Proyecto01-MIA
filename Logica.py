import json
import os

class GestorConfiguracion:
    def __init__(self, nombre_archivo="config.json"):
        self.nombre_archivo = nombre_archivo
        self.archivo_temporal = "config_temporal.json"
        self.archivo_respaldo = "config.bak"
        self.configuracion_defecto = {
            "nombre_usuario": "Estudiante",
            "tema_interfaz": "claro",
            "idioma": "es/es-ES",
            "tamanio_fuente": "12",
            "color_menu": "#EEEEEE",
            "color_letra": "#000000",
            "foto_perfil": ""
        }
        self.configuracion_actual = self.configuracion_defecto.copy()

    def cargar_configuracion(self):
        try:
            with open(self.nombre_archivo, "r", encoding="utf-8") as archivo:
                self.configuracion_actual = json.load(archivo)
            return self.configuracion_actual
        except (FileNotFoundError, json.JSONDecodeError):
            print("Archivo no encontrado o corrupto. Usando base por defecto.")
            self.configuracion_actual = self.configuracion_defecto.copy()
            return self.configuracion_actual

    def guardar_configuracion(self, datos_configuracion):
        try:
            if os.path.exists(self.nombre_archivo):
                with open(self.nombre_archivo, "r", encoding="utf-8") as original:
                    contenido_anterior = original.read()
                with open(self.archivo_respaldo, "w", encoding="utf-8") as respaldo:
                    respaldo.write(contenido_anterior)

            with open(self.archivo_temporal, "w", encoding="utf-8") as temporal:
                json.dump(
                    datos_configuracion,
                    temporal,
                    indent=4,
                    ensure_ascii=False
                )

            os.replace(self.archivo_temporal, self.nombre_archivo)
            self.configuracion_actual = datos_configuracion.copy()
            print("Configuración guardada exitosamente.")
            return True

        except Exception as e:
            print(f"Error al guardar: {e}")
            if os.path.exists(self.archivo_temporal):
                os.remove(self.archivo_temporal)
            return False