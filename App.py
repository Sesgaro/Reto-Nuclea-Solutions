import flet as ft
import pandas as pd

def main(page: ft.Page):
    
    def carga_archivo(e):
        archivo_info.pick_files(allow_multiple=False,allowed_extensions=["xls","xlsx"])
        
    def leer_resultados(event: ft.FilePickerResultEvent):        
        if event.files:
            archivo_seleccionado.value = ', '.join(map(lambda f: f.name,event.files))
        else:
            archivo_seleccionado.value = 'CANCELADO'
    
        archivo_seleccionado.update()
        page.snack_bar = ft.SnackBar(ft.Text("Espera un momento, estamos analizando el archivo"))
        page.snack_bar.open = True

        page.update()
        if archivo_seleccionado.value!='CANCELADO':
            try:
                datos=pd.read_excel(archivo_seleccionado.value)
                datos.sort_values(by=['ID','TimeStamp'], ascending=True, inplace=True)
                global dts_global,posiciones,lista_id
                dts_global=datos
                posiciones = []
                lista_sin_duplicados=[]
                lista_id=dts_global["ID"].tolist()            
                
                for i, elemento in enumerate(lista_id):
                    if elemento not in lista_sin_duplicados:
                        lista_sin_duplicados.append(elemento)
                        posiciones.append(i)
                b.disabled=False
            except Exception as ex:
                t.value = str(ex)
        t.update()
        page.snack_bar = ft.SnackBar(ft.Text("Listo!"))
        page.snack_bar.open = True
        # page.update()
        return datas(None)

    def datas(e):
        if dts_global is not None:
            if b.data >= len(posiciones):
                b.data=0
            t.value=lista_id[posiciones[b.data]]
            print(posiciones[b.data])
            b.data=b.data+1
            print(b.data)
            b.update()
            t.update()
            page.update()

    archivo_info = ft.FilePicker(on_result=leer_resultados)
    archivo_seleccionado = ft.Text()
    t=ft.Text()

    page.overlay.extend([archivo_info])

    b=ft.ElevatedButton(
                    'Siguiente Empleado',
                    icon=ft.icons.ARROW_BACK,
                    on_click=datas,
                    disabled=True,
                    data=0
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
            ],
        ),
        ft.Column(
            [
            
            ]
        )
    )
    
ft.app(target=main)