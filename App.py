import flet as ft
import random
import pandas as pd

def main(page: ft.Page):
    
    def carga_archivo(e):
        archivo_info.pick_files(allow_multiple=False,allowed_extensions=["xls","xlsx"])
        
    def leer_resultados(event: ft.FilePickerResultEvent):        
        if event.files:
            archivo_seleccionado.value = ', '.join(map(lambda f: f.name,event.files))
        else:
            archivo_seleccionado.value = 'CANCELADO'
            page.snack_bar = ft.SnackBar(ft.Text("Error, archivo no cargado"))
            page.snack_bar.open = True
    
        archivo_seleccionado.update()
        if archivo_seleccionado.value!='CANCELADO':
            page.snack_bar = ft.SnackBar(ft.Text("Espera un momento, estamos analizando el archivo"))
            page.snack_bar.open = True
            page.update()
            
            try:
                
                datos=pd.read_excel(archivo_seleccionado.value)
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
    def datas(e):
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
                                                
                    fecha=ft.DataCell(ft.Text(lista_fecha[i]))
                    proye=ft.DataCell(ft.Text(lista_pro[i])),
                    tool=ft.DataCell(ft.Text(lista_tl[i]))
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
                    
                    proyectos.rows.append(ft.DataRow(
                            cells=[
                            ft.DataCell(ft.Text(lista_fecha[i])),
                            ft.DataCell(ft.Text(lista_pro[i])),
                            color_p,
                            ft.DataCell(ft.Text(lista_tl[i])),
                            color_t,
                            ft.DataCell(ft.Text('1')),
                            ]
                            )
                        )
                # aux=cont
                t.value=lista_id[pos_id[b.data]]
                print(pos_id[b.data+1])
                print(b.data)
        
                b.disabled=False

                b.update()
                t.update()
                proyectos.update()
                page.update()
        except Exception as ex:
            print(str(ex))
            b.disabled=False
            b.update()
            
            

    archivo_info = ft.FilePicker(on_result=leer_resultados)
    archivo_seleccionado = ft.Text()
    t=ft.Text()
    grafica=ft.Container(
                visible=False,
                content=proyectos,
                bgcolor='#212121',
                
                )
    
    page.overlay.extend([archivo_info])

    b=ft.ElevatedButton(
                    'Siguiente Empleado',
                    icon=ft.icons.ARROW_BACK,
                    on_click=datas,
                    disabled=True,
                    data=-1
                )
    page.scroll='auto'
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
        grafica,
        ft.Column(
            [
            ]
        )
    )
    
ft.app(target=main)