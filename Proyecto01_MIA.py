import flet as ft

class Interfaz:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Manejo de Archivos - Proyecto 1"
        self.page.window_width = 900
        self.page.window_height = 600
        self.page.padding = 0
        self.pantalla_inicial()

    def pantalla_inicial(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.controls.clear()

        def eleccion(e):
            if e.control.data == "defecto":
                print("Lógica: Cargando configuración base...")
            elif e.control.data == "archivo":
                print("Lógica: Cargando archivo JSON del usuario...")
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
                    controls=[ft.MenuItemButton(content=ft.Text("Opción simulada", color=ft.Colors.GREY_500))]),
                ft.MenuItemButton(
                    content=ft.Text("Settings", weight=ft.FontWeight.BOLD),
                    on_click=self.abrir_configuracion
                )
            ]
        )

        self.main_content = ft.Column(
            controls=[
                ft.Container(height=50),
                ft.Text("Bienvenido al Sistema", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("El programa ha iniciado correctamente con la configuración elegida.", size=16)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row([self.menubar]),
            self.main_content
        )
        self.page.update()

    def abrir_configuracion(self, e):
        print("Abriendo ventana de Settings...")


def main(page: ft.Page):
    app = Interfaz(page)

if __name__ == "__main__":
    ft.run(main)