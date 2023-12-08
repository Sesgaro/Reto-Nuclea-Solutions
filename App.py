import flet as ft
from typing import Dict
import random
import pandas as pd



def main(page: ft.Page):

    #Carga de archivos
    def file_picker_result(event: ft.FilePickerResultEvent):
        btn_subir.current.disabled = True if event.files is None else False
        barras_progreso.clear()
        archivos.current.controls.clear()

        if event.files is not None:
            for f in event.files:
                pbr_archivo = ft.ProgressRing(value=0, bgcolor='#eeeeee', width=20, height=20)
                barras_progreso[f.name] = pbr_archivo
                archivo_seleccionado.value=f.name
                archivos.current.controls.append(ft.Row([pbr_archivo, ft.Text(f.name)]))
                # archivo_seleccionado.update()
        
        page.update()

    def on_upload_progress(event: ft.FilePickerUploadEvent):
        barras_progreso[event.file_name].value = event.progress
        barras_progreso[event.file_name].update()

        if barras_progreso[event.file_name].value==1:
            return(leer_resultados())
    
    file_picker = ft.FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(event):
        lista_archivos = []

        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                lista_archivos.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600)
                    )
                )
            
            file_picker.upload(lista_archivos)
    
    
    #Al momento de cargarse el archivo, se lee y se separan datos en diferentes listas
    def leer_resultados():        
        page.snack_bar = ft.SnackBar(ft.Text("Espera un momento, estamos analizando el archivo"))
        page.snack_bar.open = True
        page.update()
            
        try:
                
                datos=pd.read_excel(f"uploads/{archivo_seleccionado.value}")
                datos.sort_values(by=['ID','Fecha','Proyecto'], ascending=True, inplace=True)
                global dts_global,pos_id,lista_id,color_p_list,color_t_list,lista_id,lista_pro,lista_tl,lista_fecha,lista_sd_pro,lista_sd_tl
                dts_global=datos
                
                pos_id = []
                pos_pro=[]
                pos_fe=[]
                pos_tl=[]            
                
                lista_sd_id=[]
                lista_sd_pro=[]       
                lista_sd_pro_t=[]                
                     
                lista_sd_tl=[]                
                lista_sd_fe=[]
                color_t_list=[]
                color_p_list=[]
                
                lista_id=dts_global["ID"].tolist()
                lista_pro=dts_global["Proyecto"].tolist() 
                lista_tl=dts_global["Tool"].tolist()
                lista_fecha=dts_global['Fecha'].tolist()
                
                for i, x in enumerate(lista_id):
                    if x not in lista_sd_id:
                        lista_sd_id.append(x)
                        pos_id.append(i)
                        
                for i, x in enumerate(lista_pro):
                    if x not in lista_sd_pro:
                        lista_sd_pro.append(x)
                        pos_pro.append(i)
                        
                for i, x in enumerate(lista_tl):
                    if x not in lista_sd_tl:
                        lista_sd_tl.append(x)
                        pos_tl.append(i)
                        
                for i, x in enumerate(lista_fecha):
                        if x not in lista_sd_fe:
                            lista_sd_fe.append(x)
                            pos_fe.append(i)   
                            
                for i, x in enumerate(lista_sd_pro):
                    
                    color_ap = '#{:06X}'.format(random.randint(0, 0xFFFFFF))
                    color_p_list.append(color_ap)
                
                for i, x in enumerate(lista_sd_tl):
                    color_at = '#{:06X}'.format(random.randint(0, 0xFFFFFF))
                    if color_at not in color_t_list:
                        color_t_list.append(color_at)
                
                
                    
        except Exception as ex:
                t.value = str(ex)
                print(str(ex))
        t.update()
        grafica.visible=True
        

        proyectos.update()
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text("Listo!"))
        page.snack_bar.open = True
        return datas(None)
    
    #Se imprimen datos segun cada empleado
    def datas(e):
        grafica.visible=False
        grafica.update()
        carga.visible=True
        carga.update()
        t.visible=False
        t.update()
        magnitud=1
        fecha_t=[]
        proye_t=[]
        tool_t=[]
        fecha_t.append(lista_fecha[pos_id[b.data+1]])
        proye_t.append(lista_pro[pos_id[b.data+1]])
        tool_t.append(lista_tl[pos_id[b.data+1]])
        proyectos.rows.clear()
        proyectos.update()
        b.disabled=True
        b.update()
        try:
            
            if dts_global is not None:
                b.data=b.data+1
                
                if b.data == len(pos_id):
                    b.data=0
                
                for i in range(pos_id[b.data], pos_id[b.data+1]):
                                                
                    # fecha=ft.DataCell(ft.Text(lista_fecha[i]))
                    # proye=ft.DataCell(ft.Text(lista_pro[i])),
                    # tool=ft.DataCell(ft.Text(lista_tl[i]))
                    for z,x in enumerate(color_p_list):
                        if lista_pro[i] == lista_sd_pro[z]:
                            color_p=ft.DataCell(ft.Container(bgcolor=x))
                            break
                        else :
                            color_t=ft.DataCell(ft.Container(bgcolor='black'))
                    for z,x in enumerate(color_t_list):
                        if lista_tl[i] == lista_sd_tl[z]:
                            color_t=ft.DataCell(ft.Container(bgcolor=x))
                            break
                        else :
                            color_t=ft.DataCell(ft.Container(bgcolor='black'))

                    
                    if lista_fecha[i+1] in fecha_t and lista_pro[i+1] in proye_t and lista_tl[i+1] in tool_t:
                        magnitud=magnitud+1
                    else:
                        proyectos.rows.append(ft.DataRow(
                            cells=[
                            ft.DataCell(ft.Text(lista_fecha[i])),
                            ft.DataCell(ft.Text(lista_pro[i])),
                            color_p,
                            ft.DataCell(ft.Text(lista_tl[i])),
                            color_t,
                            ft.DataCell(ft.Text(magnitud)),
                                    ]
                                )
                            )
                        fecha_t=[]
                        proye_t=[]
                        tool_t=[]
                        fecha_t.append(lista_fecha[i+1])
                        proye_t.append(lista_pro[i+1])
                        tool_t.append(lista_tl[i+1])
                        magnitud=1
                
                
                t.value=lista_id[pos_id[b.data]]
                print(pos_id[b.data+1])
                print(b.data)
        
                b.disabled=False

                b.update()
                t.update()
                t.visible=True
                t.update()
                carga.visible=False
                carga.update()
                grafica.visible=True
                grafica.update()
                page.update()
        except Exception as ex:
            print(str(ex))
            b.disabled=True
            b.update()
            
            

    #   Se declaran las animaciones, columnas y botones

    b=ft.ElevatedButton(
        'Siguiente Empleado',
        icon=ft.icons.ARROW_BACK,
        on_click=datas,
        disabled=True,
        data=-1
    )
    
    page.scroll='auto'

    page.overlay.append(file_picker)

    barras_progreso: Dict[str, ft.ProgressRing] = {}

    archivos = ft.Ref[ft.Column]()
    
    btn_subir = ft.Ref[ft.ElevatedButton]()

    proyectos=ft.DataTable(
        border=ft.border.all(2, "#2f2f2f"),
        border_radius=10,
        divider_thickness=0,
        vertical_lines=ft.border.BorderSide(2, "#2f2f2f"),
        horizontal_lines=ft.border.BorderSide(1, "#2f2f2f"),
        column_spacing=10,
        columns=[
            ft.DataColumn(ft.Text('Fecha')),
            ft.DataColumn(ft.Text('Proyecto')),
            ft.DataColumn(ft.Text('Leyenda P')),
            ft.DataColumn(ft.Text('Herramienta')),
            ft.DataColumn(ft.Text('Leyenda H')),
            ft.DataColumn(ft.Text('Magnitud'))
        ],
        rows=[]
    )

    archivo_info = ft.FilePicker(on_result=leer_resultados)

    archivo_seleccionado = ft.Text()
    
    t=ft.Text()
    
    carga=ft.ProgressRing(visible=False)

    grafica=ft.Container(
        visible=False,
        alignment=ft.alignment.center,
        content=ft.Row([proyectos,carga,]),
        bgcolor='#212121',        
        )
    
    page.overlay.extend([archivo_info])
    
    #Se inicializa la ventana
    page.add(
        
        ft.Row(
            [
                ft.ElevatedButton(
            'Seleccionar archivos...',
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=False,allowed_extensions=["xls","xlsx"])
        ),
        ft.Column(ref=archivos),
            ft.ElevatedButton(
                    'Subir',
                    ref=btn_subir,
                    icon=ft.icons.UPLOAD,
                    on_click=upload_files,
                    disabled=True
                )
            ]
        ),
        ft.Row(
            [
                b,  
                t
            ],
        ),
        grafica,
        carga,
        ft.Column(
            [
            ]
        )
    )
ft.app(target=main, view=ft.AppView.WEB_BROWSER, web_renderer=ft.WebRenderer.HTML, upload_dir='uploads')
