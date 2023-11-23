import flet as ft
import pandas as pd

def main(page: ft.Page):
    def leer_resultados(event: ft.FilePickerResultEvent):
        if event.files:
            archivo_seleccionado.value = ', '.join(map(lambda f: f.name,event.files))
        else:
            archivo_seleccionado.value = 'CANCELADO'
    
        archivo_seleccionado.update()

    def datas(e):
        if archivo_seleccionado.value != 'CANCELADO':
            try:
                datos=pd.read_excel(archivo_seleccionado.value)
                datos.sort_values(by=['ID','TimeStamp'], ascending=True, inplace=True)
                lista=datos["ID"].tolist()
                i=lista[1]
                t.value=lista[1]
            except Exception as ex:
                t.value = str(ex)

        t.update()
        page.update()

    def carga_archivo(e):
        archivo_info.pick_files(allow_multiple=False,allowed_extensions=["xls","xlsx"])

    archivo_info = ft.FilePicker(on_result=leer_resultados)
    archivo_seleccionado = ft.Text()
    t=ft.Text()

    page.overlay.extend([archivo_info])

    b=ft.ElevatedButton(
                    'Inicia',
                    icon=ft.icons.MOUSE,
                    on_click=datas
                )

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    'Carga tu archivo',
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=carga_archivo
                ),
                archivo_seleccionado,
            ]
        ),
        ft.Row(
            [
                b,  
                t
            ]
        )
    )

ft.app(target=main)