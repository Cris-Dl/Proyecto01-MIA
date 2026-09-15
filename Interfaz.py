import flet as ft
from Logica import GestorConfiguracion
import tkinter as tk
from tkinter import filedialog, colorchooser
import os
from typing import Any

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
        snack = ft.SnackBar(content=ft.Text(texto), bgcolor=color)
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()

    def pantalla_inicial(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.controls.clear()

        def abrir_selector():
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            ruta = filedialog.askopenfilename(
                title="Selecciona tu archivo de configuración",
                filetypes=[("Archivos JSON", "*.json")]
            )
            root.destroy()
            return ruta

        def procesar_archivo(ruta):
            if not ruta:
                return
            datos, estado = self.gestor.cargar_configuracion(ruta)

            if estado == "exito":
                self.configuracion_activa = datos
                self.mostrar_mensaje("¡Configuración cargada correctamente!", ft.Colors.GREEN_700)
                self.pantalla_principal()
            else:
                def accion_cancelar(e):
                    dlg_error.open = False
                    self.page.update()

                def accion_base(e):
                    dlg_error.open = False
                    self.configuracion_activa = self.gestor.configuracion_defecto.copy()
                    self.page.update()
                    self.mostrar_mensaje("Iniciando con configuración base.", ft.Colors.BLUE_700)
                    self.pantalla_principal()

                def accion_otro(e):
                    dlg_error.open = False
                    self.page.update()
                    nueva_ruta = abrir_selector()
                    procesar_archivo(nueva_ruta)

                dlg_error = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Archivo Corrupto o Inválido"),
                    content=ft.Text(
                        "El archivo seleccionado está corrupto o no tiene un formato válido de configuración para este programa.\n\n¿Qué deseas hacer?"),
                    actions=[
                        ft.TextButton("Cancelar", on_click=accion_cancelar),
                        ft.OutlinedButton("Cargar Base", on_click=accion_base),
                        ft.FilledButton("Cargar Otro", on_click=accion_otro)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                self.page.overlay.append(dlg_error)
                dlg_error.open = True
                self.page.update()

        def eleccion(e):
            if e.control.data == "defecto":
                self.configuracion_activa = self.gestor.configuracion_defecto.copy()
                self.mostrar_mensaje("Iniciando con configuración base.", ft.Colors.BLUE_700)
                self.pantalla_principal()

            elif e.control.data == "archivo":
                ruta_seleccionada = abrir_selector()
                procesar_archivo(ruta_seleccionada)

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
        nombre_usuario = self.configuracion_activa.get("nombre_usuario", "Usuario")
        ruta_foto = self.configuracion_activa.get("foto_perfil", "")
        color_texto = self.configuracion_activa.get("color_letra", "#000000")
        color_menu = self.configuracion_activa.get("color_menu", "#EEEEEE")
        try:
            tamanio_base = int(self.configuracion_activa.get("tamanio_fuente", 16))
        except ValueError:
            tamanio_base = 16

        self.menubar = ft.Row(
            controls=[
                ft.PopupMenuButton(
                    content=ft.Text("Archivo", color=color_texto),
                    items=[ft.PopupMenuItem(content=ft.Text("Opción simulada"))]
                ),
                ft.PopupMenuButton(
                    content=ft.Text("Edición", color=color_texto),
                    items=[ft.PopupMenuItem(content=ft.Text("Opción simulada"))]
                ),
                ft.PopupMenuButton(
                    content=ft.Text("Ver", color=color_texto),
                    items=[ft.PopupMenuItem(content=ft.Text("Opción simulada"))]
                ),
                ft.Container(width=10),
                ft.TextButton(
                    content=ft.Text("Settings", weight=ft.FontWeight.BOLD, color=color_texto),
                    on_click=self.abrir_configuracion
                )
            ],
            spacing=10
        )

        barra_superior = ft.Container(
            bgcolor=color_menu,
            padding=10,
            content=self.menubar,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.Colors.BLACK12)
        )

        controles_centro: list[Any] = [ft.Container(height=50)]

        if ruta_foto and os.path.exists(ruta_foto):
            controles_centro.append(
                ft.Image(
                    src=ruta_foto,
                    width=150,
                    height=150,
                    fit="cover",  # type: ignore
                    border_radius=75
                )
            )
        else:
            controles_centro.append(
                ft.Text("👤", size=100)
            )

        controles_centro.extend([
            ft.Container(height=20),
            ft.Text(f"Bienvenido al Sistema, {nombre_usuario}", size=tamanio_base, weight=ft.FontWeight.BOLD,
                    color=color_texto),
            ft.Text("El programa ha iniciado correctamente con la configuración elegida.", size=tamanio_base,
                    color=color_texto)
        ])

        self.main_content = ft.Column(
            controls=controles_centro,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.add(
            barra_superior,
            self.main_content
        )
        self.page.update()

    def abrir_configuracion(self, e):
        txt_nombre = ft.TextField(label="Nombre Usuario", value=self.configuracion_activa.get("nombre_usuario", ""))

        color_menu_actual = self.configuracion_activa.get("color_menu", "#EEEEEE")
        color_letra_actual = self.configuracion_activa.get("color_letra", "#000000")

        txt_color_menu = ft.TextField(label="Color de Menú", value=color_menu_actual, expand=True)
        txt_color_letra = ft.TextField(label="Color de Letra", value=color_letra_actual, expand=True)

        chk_sincronizar = ft.Checkbox(
            label="Sincronizar colores (letras y menú) con el tema",
            value=self.configuracion_activa.get("sincronizar_color", True)
        )

        def al_cambiar_tema(ev):
            if ev.control.value == "oscuro":
                self.page.theme_mode = ft.ThemeMode.DARK
                if chk_sincronizar.value:
                    txt_color_menu.value = "#222222"
                    txt_color_letra.value = "#FFFFFF"
            else:
                self.page.theme_mode = ft.ThemeMode.LIGHT
                if chk_sincronizar.value:
                    txt_color_menu.value = "#EEEEEE"
                    txt_color_letra.value = "#000000"

            txt_color_letra.update()
            txt_color_menu.update()

            btn_color_menu.bgcolor = txt_color_menu.value
            btn_color_letra.bgcolor = txt_color_letra.value
            btn_color_menu.update()
            btn_color_letra.update()
            self.page.update()

        dd_tema = ft.Dropdown(
            label="Tema Interfaz",
            options=[ft.dropdown.Option("claro"), ft.dropdown.Option("oscuro")],
            value=self.configuracion_activa.get("tema_interfaz", "claro"),
            on_select=al_cambiar_tema
        )

        def elegir_color_menu(ev):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            resultado = colorchooser.askcolor(title="Selecciona Color del Menú", initialcolor=txt_color_menu.value)
            root.destroy()
            if resultado and resultado[1]:
                color_hex = str(resultado[1])
                txt_color_menu.value = color_hex
                txt_color_menu.update()

                chk_sincronizar.value = False
                chk_sincronizar.update()

                ev.control.bgcolor = color_hex
                ev.control.update()

        def elegir_color_letra(ev):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            resultado = colorchooser.askcolor(title="Selecciona Color de Letra", initialcolor=txt_color_letra.value)
            root.destroy()
            if resultado and resultado[1]:
                color_hex = str(resultado[1])
                txt_color_letra.value = color_hex
                txt_color_letra.update()

                chk_sincronizar.value = False
                chk_sincronizar.update()

                ev.control.bgcolor = color_hex
                ev.control.update()

        btn_color_menu = ft.Container(
            content=ft.Text("🎨 Elegir", weight=ft.FontWeight.BOLD),
            bgcolor=color_menu_actual,
            padding=10,
            border_radius=5,
            ink=True,
            on_click=elegir_color_menu
        )

        btn_color_letra = ft.Container(
            content=ft.Text("🎨 Elegir", weight=ft.FontWeight.BOLD),
            bgcolor=color_letra_actual,
            padding=10,
            border_radius=5,
            ink=True,
            on_click=elegir_color_letra
        )

        dd_idioma = ft.Dropdown(
            label="Idioma",
            options=[ft.dropdown.Option("es/es-ES"), ft.dropdown.Option("en/en-US")],
            value=self.configuracion_activa.get("idioma", "es/es-ES")
        )

        txt_fuente = ft.TextField(label="Tamaño Fuente",
                                  value=str(self.configuracion_activa.get("tamanio_fuente", "16")))
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
                    ft.Row([txt_color_menu, btn_color_menu]),
                    ft.Row([txt_color_letra, btn_color_letra]),
                    chk_sincronizar,
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
                "foto_perfil": txt_ruta_foto.value,
                "sincronizar_color": chk_sincronizar.value
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
            tema_original = self.configuracion_activa.get("tema_interfaz", "claro")
            self.page.theme_mode = ft.ThemeMode.DARK if tema_original == "oscuro" else ft.ThemeMode.LIGHT
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