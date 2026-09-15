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

        self.textos = {
            "es/es-ES": {
                "archivo": "Archivo",
                "edicion": "Edición",
                "ver": "Ver",
                "opc_simulada": "Opción simulada",
                "menu_descargar_bak": "Descargar configuración anterior (.bak)",
                "menu_info_guardado": "Estado de configuración actual",
                "settings": "Settings",
                "bienvenida": "Bienvenido al Sistema,",
                "mensaje_inicio": "El programa ha iniciado correctamente con la configuración elegida.",
                "lbl_nombre": "Nombre Usuario",
                "lbl_color_menu": "Color de Menú",
                "lbl_color_letra": "Color de Letra",
                "chk_sincronizar": "Sincronizar colores (letras y menú) con el tema",
                "lbl_tema": "Tema Interfaz",
                "lbl_idioma": "Idioma",
                "lbl_fuente": "Tamaño Fuente",
                "lbl_foto": "Ruta Foto de Perfil",
                "btn_buscar": "Buscar",
                "btn_elegir": "🎨 Elegir",
                "titulo_config": "Configuración de Usuario",
                "btn_cancelar": "Cancelar",
                "btn_guardar": "Guardar Configuración",
                "msg_exito": "¡Configuración guardada y archivo JSON actualizado!",
                "msg_error": "Error al guardar."
            },
            "en/en-US": {
                "archivo": "File",
                "edicion": "Edit",
                "ver": "View",
                "opc_simulada": "Simulated option",
                "menu_descargar_bak": "Download previous config (.bak)",
                "menu_info_guardado": "Current configuration status",
                "settings": "Settings",
                "bienvenida": "Welcome to the System,",
                "mensaje_inicio": "The program has started successfully with the chosen configuration.",
                "lbl_nombre": "Username",
                "lbl_color_menu": "Menu Color",
                "lbl_color_letra": "Font Color",
                "chk_sincronizar": "Sync colors (font & menu) with theme",
                "lbl_tema": "Interface Theme",
                "lbl_idioma": "Language",
                "lbl_fuente": "Font Size",
                "lbl_foto": "Profile Picture Path",
                "btn_buscar": "Browse",
                "btn_elegir": "🎨 Choose",
                "titulo_config": "User Settings",
                "btn_cancelar": "Cancel",
                "btn_guardar": "Save Settings",
                "msg_exito": "Configuration saved and JSON file updated!",
                "msg_error": "Error saving."
            }
        }

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

        def guardar_nuevo_selector():
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            ruta = filedialog.asksaveasfilename(
                title="Guardar nueva configuración como...",
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json")],
                initialfile="config.json"
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
                    self.page.update()
                    ruta_nueva = guardar_nuevo_selector()
                    if ruta_nueva:
                        self.gestor.nombre_archivo = ruta_nueva
                    self.configuracion_activa = self.gestor.configuracion_defecto.copy()
                    self.gestor.guardar_configuracion(self.configuracion_activa)
                    self.mostrar_mensaje("¡Archivo base creado e iniciado con éxito!", ft.Colors.BLUE_700)
                    self.pantalla_principal()

                def accion_otro(e):
                    dlg_error.open = False
                    self.page.update()
                    nueva_ruta = abrir_selector()
                    procesar_archivo(nueva_ruta)

                dlg_error = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Archivo Corrupto o Inválido"),
                    content=ft.Text("El archivo seleccionado está corrupto o no tiene un formato válido de configuración para este programa.\n\n¿Qué deseas hacer?"),
                    actions=[
                        ft.TextButton("Cancelar", on_click=accion_cancelar),
                        ft.OutlinedButton("Crear Base", on_click=accion_base),
                        ft.FilledButton("Cargar Otro", on_click=accion_otro)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                self.page.overlay.append(dlg_error)
                dlg_error.open = True
                self.page.update()

        def eleccion(e):
            if e.control.data == "defecto":
                ruta_nueva = guardar_nuevo_selector()
                if ruta_nueva:
                    self.gestor.nombre_archivo = ruta_nueva
                self.configuracion_activa = self.gestor.configuracion_defecto.copy()
                self.gestor.guardar_configuracion(self.configuracion_activa)
                self.mostrar_mensaje("¡Archivo base creado e iniciado con éxito!", ft.Colors.BLUE_700)
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
                                ft.TextButton("Crear Nueva Base", data="defecto", on_click=eleccion),
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
        idioma = self.configuracion_activa.get("idioma", "es/es-ES")
        t = self.textos.get(idioma, self.textos["es/es-ES"])
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

        def cerrar_dialogo(dlg):
            dlg.open = False
            self.page.update()

        def descargar_bak(e):
            if self.gestor.tiene_respaldo():
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                ruta = filedialog.asksaveasfilename(
                    title="Guardar respaldo anterior (.bak)",
                    defaultextension=".json",
                    filetypes=[("Archivos JSON", "*.json")],
                    initialfile="respaldo_anterior.json"
                )
                root.destroy()
                if ruta:
                    if self.gestor.exportar_respaldo(ruta):
                        self.mostrar_mensaje("¡Respaldo anterior descargado correctamente!", ft.Colors.GREEN_700)
                    else:
                        self.mostrar_mensaje("Hubo un error al exportar el respaldo.", ft.Colors.RED_700)
            else:
                self.mostrar_mensaje("Aún no existe una configuración anterior para respaldar.", ft.Colors.RED_700)

        def info_guardado(e):
            def confirmar_descarga_actual(ex):
                dlg_info.open = False
                self.page.update()
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                ruta = filedialog.asksaveasfilename(
                    title="Descargar copia de la configuración actual",
                    defaultextension=".json",
                    filetypes=[("Archivos JSON", "*.json")],
                    initialfile="copia_configuracion.json"
                )
                root.destroy()
                if ruta:
                    if self.gestor.exportar_configuracion_actual(ruta):
                        self.mostrar_mensaje("¡Copia de configuración actual descargada!", ft.Colors.GREEN_700)
                    else:
                        self.mostrar_mensaje("Hubo un error al descargar la copia.", ft.Colors.RED_700)

            texto_info = f"Todos los cambios se han guardado de forma segura en el archivo original:\n{self.gestor.nombre_archivo}\n\n(Se utilizó un archivo temporal de escritura para evitar corrupción de datos).\n\n¿Deseas descargar una copia extra de esta configuración?"
            if idioma == "en/en-US":
                texto_info = f"All changes have been securely saved to the original file:\n{self.gestor.nombre_archivo}\n\n(A temporary write file was used to prevent data corruption).\n\nWould you like to download an extra copy of this configuration?"

            dlg_info = ft.AlertDialog(
                title=ft.Text(t["menu_info_guardado"]),
                content=ft.Text(texto_info),
                actions=[
                    ft.TextButton(t["btn_cancelar"], on_click=lambda ex: cerrar_dialogo(dlg_info)),
                    ft.FilledButton(t["menu_descargar_bak"].split(' ')[0], on_click=confirmar_descarga_actual)
                ]
            )
            self.page.overlay.append(dlg_info)
            dlg_info.open = True
            self.page.update()

        self.menubar = ft.Row(
            controls=[
                ft.PopupMenuButton(
                    content=ft.Text(t["archivo"], color=color_texto),
                    items=[
                        ft.PopupMenuItem(content=ft.Text(t["menu_descargar_bak"]), on_click=descargar_bak),
                        ft.PopupMenuItem(content=ft.Text(t["menu_info_guardado"]), on_click=info_guardado)
                    ]
                ),
                ft.PopupMenuButton(
                    content=ft.Text(t["edicion"], color=color_texto),
                    items=[ft.PopupMenuItem(content=ft.Text(t["opc_simulada"]))]
                ),
                ft.PopupMenuButton(
                    content=ft.Text(t["ver"], color=color_texto),
                    items=[ft.PopupMenuItem(content=ft.Text(t["opc_simulada"]))]
                ),
                ft.Container(width=10),
                ft.TextButton(
                    content=ft.Text(t["settings"], weight=ft.FontWeight.BOLD, color=color_texto),
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
            ft.Text(f"{t['bienvenida']} {nombre_usuario}", size=tamanio_base, weight=ft.FontWeight.BOLD,
                    color=color_texto),
            ft.Text(t["mensaje_inicio"], size=tamanio_base, color=color_texto)
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
        idioma_actual = self.configuracion_activa.get("idioma", "es/es-ES")
        t = self.textos.get(idioma_actual, self.textos["es/es-ES"])
        txt_nombre = ft.TextField(label=t["lbl_nombre"], value=self.configuracion_activa.get("nombre_usuario", ""))
        color_menu_actual = self.configuracion_activa.get("color_menu", "#EEEEEE")
        color_letra_actual = self.configuracion_activa.get("color_letra", "#000000")
        txt_color_menu = ft.TextField(label=t["lbl_color_menu"], value=color_menu_actual, expand=True)
        txt_color_letra = ft.TextField(label=t["lbl_color_letra"], value=color_letra_actual, expand=True)
        chk_sincronizar = ft.Checkbox(
            label=t["chk_sincronizar"],
            value=True
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
            label=t["lbl_tema"],
            options=[ft.dropdown.Option("claro"), ft.dropdown.Option("oscuro")],
            value=self.configuracion_activa.get("tema_interfaz", "claro"),
            on_select=al_cambiar_tema
        )

        def elegir_color_menu(ev):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            resultado = colorchooser.askcolor(title=t["lbl_color_menu"], initialcolor=txt_color_menu.value)
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
            resultado = colorchooser.askcolor(title=t["lbl_color_letra"], initialcolor=txt_color_letra.value)
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
            content=ft.Text(t["btn_elegir"], weight=ft.FontWeight.BOLD),
            bgcolor=color_menu_actual,
            padding=10,
            border_radius=5,
            ink=True,
            on_click=elegir_color_menu
        )

        btn_color_letra = ft.Container(
            content=ft.Text(t["btn_elegir"], weight=ft.FontWeight.BOLD),
            bgcolor=color_letra_actual,
            padding=10,
            border_radius=5,
            ink=True,
            on_click=elegir_color_letra
        )

        dd_idioma = ft.Dropdown(
            label=t["lbl_idioma"],
            options=[ft.dropdown.Option("es/es-ES"), ft.dropdown.Option("en/en-US")],
            value=idioma_actual
        )

        txt_fuente = ft.TextField(label=t["lbl_fuente"],
                                  value=str(self.configuracion_activa.get("tamanio_fuente", "16")))
        txt_ruta_foto = ft.TextField(label=t["lbl_foto"], read_only=True, expand=True,
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

        boton_buscar = ft.FilledButton(t["btn_buscar"], on_click=seleccionar_foto_local)

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(t["titulo_config"]),
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
                "foto_perfil": txt_ruta_foto.value
            }

            if self.gestor.guardar_configuracion(nuevos_datos):
                self.configuracion_activa = nuevos_datos
                dialogo.open = False
                self.page.update()
                t_nuevo = self.textos.get(dd_idioma.value, self.textos["es/es-ES"])
                self.mostrar_mensaje(t_nuevo["msg_exito"], ft.Colors.GREEN_700)
                self.pantalla_principal()
            else:
                self.mostrar_mensaje(t["msg_error"], ft.Colors.RED_700)

        def cancelar_click(ev):
            tema_original = self.configuracion_activa.get("tema_interfaz", "claro")
            self.page.theme_mode = ft.ThemeMode.DARK if tema_original == "oscuro" else ft.ThemeMode.LIGHT
            dialogo.open = False
            self.page.update()

        dialogo.actions = [
            ft.TextButton(t["btn_cancelar"], on_click=cancelar_click),
            ft.FilledButton(t["btn_guardar"], on_click=guardar_click)
        ]
        dialogo.actions_alignment = ft.MainAxisAlignment.END

        self.page.overlay.append(dialogo)
        dialogo.open = True
        self.page.update()

def main(page: ft.Page):
    app = Interfaz(page)

if __name__ == "__main__":
    ft.run(main)