import flet as ft
from Logica import GestorConfiguracion
import tkinter as tk
from tkinter import filedialog

class Interfaz:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Manejo de Archivos - Proyecto 1"
        self.page.window_width = 900
        self.page.window_height = 600
        self.page.padding = 0
        self.gestor = GestorConfiguracion()
        self.configuracion_activa = {}
        self.pantalla_inicial()

    def mostrar_mensaje(self, texto, color):
        print(f"Notificación: {texto}")
        snack = ft.SnackBar(content=ft.Text(texto), bgcolor=color)
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()

    def pantalla_inicial(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.controls.clear()

        def eleccion(e):
            if e.control.data == "defecto":
                self.configuracion_activa = self.gestor.configuracion_defecto.copy()
                self.mostrar_mensaje("Iniciando con configuración base.", ft.Colors.BLUE_700)
                self.pantalla_principal()

            elif e.control.data == "archivo":
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                ruta = filedialog.askopenfilename(
                    title="Selecciona tu archivo de configuración",
                    filetypes=[("Archivos JSON", "*.json")]
                )
                root.destroy()

                if ruta:
                    datos, estado = self.gestor.cargar_configuracion(ruta)
                    self.configuracion_activa = datos

                    if estado == "exito":
                        self.mostrar_mensaje("¡Configuración cargada correctamente!", ft.Colors.GREEN_700)
                    elif estado == "invalido":
                        self.mostrar_mensaje("Error: Archivo corrupto. Usando base.", ft.Colors.RED_700)
                    elif estado == "no_encontrado":
                        self.mostrar_mensaje("Error: Archivo no encontrado. Usando base.", ft.Colors.ORANGE_700)

                    self.pantalla_principal()

        startup_card = ft.Card(
            elevation=10,
            content=ft.Container(
                padding=30,
                content=ft.Column(
                    controls=[
                        ft.Text("Configuración Inicial", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("¿Qué configuración deseas usar para iniciar el programa?", size=16),
                        ft.Container(height=10),
                        ft.Row(
                            controls=[
                                ft.TextButton("Usar Base por Defecto", data="defecto", on_click=eleccion),
                                ft.FilledButton("Cargar Archivo", data="archivo", on_click=eleccion),
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    tight=True
                )
            )
        )
        self.page.add(startup_card)
        self.page.update()

    def pantalla_principal(self):
        self.page.controls.clear()
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        tema = self.configuracion_activa.get("tema_interfaz", "claro")
        if tema == "oscuro":
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        self.menubar = ft.MenuBar(
            expand=True,
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("Archivo"),
                    controls=[ft.MenuItemButton(content=ft.Text("Opción simulada", color=ft.Colors.GREY_500))]),
                ft.SubmenuButton(
                    content=ft.Text("Edición"),
                    controls=[ft.MenuItemButton(content=ft.Text("Opción simulada", color=ft.Colors.GREY_500))]),
                ft.SubmenuButton(
                    content=ft.Text("Ver"),
                    controls=[ft.MenuItemButton(content=ft.Text("Opción simulada", color=ft.Colors.GREY_500))])
            ]
        )

        btn_settings = ft.TextButton(
            content=ft.Text("Settings", weight=ft.FontWeight.BOLD),
            on_click=self.abrir_configuracion
        )

        nombre_usuario = self.configuracion_activa.get("nombre_usuario", "Usuario")

        self.main_content = ft.Column(
            controls=[
                ft.Container(height=50),
                ft.Text(f"Bienvenido al Sistema, {nombre_usuario}", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("El programa ha iniciado correctamente con la configuración elegida.", size=16)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[self.menubar, btn_settings],
                alignment=ft.MainAxisAlignment.START,
            ),
            self.main_content
        )
        self.page.update()

    def abrir_configuracion(self, e):
        print("Abriendo ventana de Settings...")
        txt_nombre = ft.TextField(label="Nombre Usuario", value=self.configuracion_activa.get("nombre_usuario", ""))
        dd_tema = ft.Dropdown(
            label="Tema Interfaz",
            options=[ft.dropdown.Option("claro"), ft.dropdown.Option("oscuro")],
            value=self.configuracion_activa.get("tema_interfaz", "claro")
        )
        dd_idioma = ft.Dropdown(
            label="Idioma",
            options=[ft.dropdown.Option("es/es-ES"), ft.dropdown.Option("en/en-US")],
            value=self.configuracion_activa.get("idioma", "es/es-ES")
        )
        txt_fuente = ft.TextField(label="Tamaño Fuente",
                                  value=str(self.configuracion_activa.get("tamanio_fuente", "12")))
        txt_color_menu = ft.TextField(label="Color de Menú", value=self.configuracion_activa.get("color_menu", ""))
        txt_color_letra = ft.TextField(label="Color de Letra", value=self.configuracion_activa.get("color_letra", ""))
        txt_ruta_foto = ft.TextField(label="Ruta Foto de Perfil", read_only=True, expand=True,
                                     value=self.configuracion_activa.get("foto_perfil", ""))

        def seleccionar_foto_local(ev):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
            root.destroy()
            if ruta:
                txt_ruta_foto.value = ruta
                txt_ruta_foto.update()
        boton_buscar = ft.FilledButton("Buscar", on_click=seleccionar_foto_local)
        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Configuración de Usuario"),
            content=ft.Column(
                controls=[
                    txt_nombre,
                    ft.Row([dd_tema, dd_idioma]),
                    txt_fuente,
                    ft.Row([txt_color_menu, txt_color_letra]),
                    ft.Row([txt_ruta_foto, boton_buscar])
                ],
                width=550,
                tight=True,
            )
        )

        def guardar_click(ev):
            nuevos_datos = {
                "nombre_usuario": txt_nombre.value,
                "tema_interfaz": dd_tema.value,
                "idioma": dd_idioma.value,
                "tamanio_fuente": txt_fuente.value,
                "color_menu": txt_color_menu.value,
                "color_letra": txt_color_letra.value,
                "foto_perfil": txt_ruta_foto.value
            }

            if self.gestor.guardar_configuracion(nuevos_datos):
                self.configuracion_activa = nuevos_datos
                dialogo.open = False
                self.page.update()
                self.mostrar_mensaje("¡Configuración guardada y archivo JSON creado!", ft.Colors.GREEN_700)
                self.pantalla_principal()
            else:
                self.mostrar_mensaje("Error al guardar.", ft.Colors.RED_700)

        def cancelar_click(ev):
            dialogo.open = False
            self.page.update()

        dialogo.actions = [
            ft.TextButton("Cancelar", on_click=cancelar_click),
            ft.FilledButton("Guardar Configuración", on_click=guardar_click)
        ]
        dialogo.actions_alignment = ft.MainAxisAlignment.END
        self.page.overlay.append(dialogo)
        dialogo.open = True
        self.page.update()


def main(page: ft.Page):
    app = Interfaz(page)


if __name__ == "__main__":
    ft.run(main)