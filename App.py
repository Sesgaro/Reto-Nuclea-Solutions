import flet as ft
import flet.canvas as cv

from typing import Dict
import random
import pandas as pd
import math

emp=1

def main(page: ft.Page):
    page.bgcolor="#1f262f"
    page.vertical_alignment="center"
    page.horizontal_alignment="center"

    #Carga de archivos
    def file_picker_result(event: ft.FilePickerResultEvent):
        # btn_subir.current.disabled = True if event.files is None else False
        barras_progreso.clear()
        archivos.current.controls.clear()

        if event.files is not None:
            for f in event.files:
                pbr_archivo = ft.ProgressRing(value=0, bgcolor='#eeeeee', width=20, height=20)
                barras_progreso[f.name] = pbr_archivo
                archivo_seleccionado.value=f.name
                items=[pbr_archivo, ft.Text(f.name)]
                archivos.current.controls.append(ft.Row(items,alignment=ft.MainAxisAlignment.CENTER))
                # archivo_seleccionado.update()
        
        page.update()
        return (upload_files(None))

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
                
                global dts_global,pos_id,lista_id,color_p_list,color_t_list,lista_id,lista_pro,lista_tl,lista_fecha,lista_sd_pro,lista_sd_tl,mg_list
                dts_global=datos
                
                pos_id = []
                pos_pro=[]
                pos_fe=[]
                pos_tl=[]            
                
                mg_list=[]

                lista_sd_id=[]
                lista_sd_pro=[]      
                     
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

                for i, x in enumerate(pos_id):
                    if i!=len(pos_id)-1:
                        difer=pos_id[i+1]-pos_id[i]
                        mg_list.append(difer)
                    else:
                        break

                print(mg_list,"\n")
                ver_emp.disabled=False
                
                
                    
        except Exception as ex:
                t.value = str(ex)
                print(str(ex))

        t.update()
        
        proyectos.update()
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text("Listo!"))
        page.snack_bar.open = True
        page.update()

    
    #Se imprimen datos segun cada empleado
    def datas(e: ft.ContainerTapEvent):
        global emp
        for i in range(3):
            try: 
                if e.control == flecha_superior:
                    emp = emp+1
                    if emp == -1:
                        emp = emp+1

                else:
                    emp = emp-1
                    if emp == -1:
                        emp = emp-1

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

                fecha_t.append(lista_fecha[pos_id[emp]])
                proye_t.append(lista_pro[pos_id[emp]])
                tool_t.append(lista_tl[pos_id[emp]])
                
                proyectos.rows.clear()
                proyectos.update()   
                
                if dts_global is not None:

                    if emp == len(pos_id)-1:
                        emp=0
                    
                    for i in range(pos_id[emp], pos_id[emp+1]):

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
                    
                    
                    t.value=f"ID: {lista_id[pos_id[emp]]}"
                    print(pos_id[emp])
                    print(emp,"\n")
            
                    t.update()
                    t.visible=True
                    t.update()
                    carga.visible=False
                    carga.update()
                    grafica.visible=True
                    grafica.update()
                    ver_emp.visible=False
                    page.update()
                    break
            except Exception as ex:
                print(str(ex))
                emp=1
            
            

    #   Se declaran las animaciones, columnas y botones
    
    page.scroll='auto'

    page.overlay.append(file_picker)

    barras_progreso: Dict[str, ft.ProgressRing] = {}

    archivos = ft.Ref[ft.Column]()

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
    
    t=ft.Text(size=30)
    
    carga=ft.ProgressRing(visible=False)
    
    select_btn = ft.ElevatedButton('Selecciona un archivo', icon=ft.icons.FOLDER_OPEN, on_click=lambda _: file_picker.pick_files(allow_multiple=False,allowed_extensions=["xls","xlsx"]))
    
    columna_archivos = ft.Column(ref=archivos,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    concarga=ft.Container(alignment=ft.alignment.center,height=300,content=carga)

    triangulo = cv.Canvas([
        cv.Path(
                [   
                    ft.canvas.Path.MoveTo(40, 0),
                    ft.canvas.Path.LineTo(0,50),
                    ft.canvas.Path.LineTo(80,50),
                    cv.Path.Close(),
                ],
                paint=ft.Paint(
                stroke_width=4,
                style=ft.PaintingStyle.STROKE,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.Alignment(0,30),
                    colors=[
                        "#5a5bf3",
                        "#91e7d9",
                    ],
                    tile_mode=ft.GradientTileMode.MIRROR,
                ),
                ),
            ),
        ],
        width=80,
        height=50,
    )

    
    flecha_superior = ft.Container(triangulo, width=80, height=50, on_click=datas,rotate=ft.Rotate(angle=math.pi/2))

    items_grafica=[ft.Container(triangulo, width=80, height=50, rotate=ft.Rotate(angle=-math.pi/2), on_click=datas),proyectos,flecha_superior]

    ver_emp=ft.ElevatedButton('Ver empleados',disabled=True,on_click=datas)

    grafica=ft.Container(
        visible=False,
        alignment=ft.alignment.center,
        content=ft.Row(items_grafica,alignment=ft.MainAxisAlignment.CENTER)  
        )
    
    best_txt=ft.Text()

    best_emp=ft.Container(opacity=0,content=best_txt
                          )
    col = ft.Column(spacing=10,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[select_btn, columna_archivos, ver_emp, t, grafica, concarga])

    contenedor = ft.Container(col, alignment=ft.alignment.center, margin=0,)
    
    #Se inicializa la ventana
    page.add(
        contenedor
    )
ft.app(target=main, view=ft.AppView.WEB_BROWSER, upload_dir='uploads')
