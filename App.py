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
                # t.value=lista[1]
                # for i in lista:
                    
            except Exception as ex:
                t.value = str(ex)
        # t.update()
        # page.update()

    def datas(e):
        if dts_global is not None:
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
            ]
        )
    )
    
ft.app(target=main)