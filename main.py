import flet as ft
import pandas as pd
import os

def main(page: ft.Page):
    page.title = "Porra Mundial 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "black"
    page.window.width = 400
    page.window.height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.fonts = {
        "Retro8Bit": "https://fonts.gstatic.com/s/pressstart2p/v15/e3t4ve96Z8rk0RWmr5_6BpX6-D_LswS66V776A.ttf"
    }

    def ir_a_precios(_): 
        page.controls.clear()
        
        btn_volver = ft.Container(
            content=ft.Text("VOLVER", font_family="Retro8Bit", size=10, color="black"),
            bgcolor="yellow",
            padding=20, 
            border=ft.Border(
                top=ft.BorderSide(2, "yellow"), left=ft.BorderSide(2, "yellow"),
                bottom=ft.BorderSide(2, "grey900"), right=ft.BorderSide(2, "grey900")
            ),
            on_click=ir_a_inicio
        )
        
        titulo = ft.Text("ELIGE TUS EQUIPOS", size=18, font_family="Retro8Bit", color="yellow")
        subtitulo = ft.Text("70 puntos para 7 selecciones", size=12, font_family="Retro8Bit", color="grey400")
        
        page.add(
            ft.Row([btn_volver], alignment=ft.MainAxisAlignment.START),
            ft.Divider(height=10, color="transparent"),
            titulo,
            subtitulo,
            ft.Divider(height=10, color="transparent")
        )

        try:
            df = pd.read_csv("selecciones.csv", sep=";")
            df_sorted = df.sort_values(by="PRECIO", ascending=False)
            lista_equipos = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, width=380)

            for _, row in df_sorted.iterrows():
                bandera_path = row['BANDERA']
                img = ft.Image(src=bandera_path, width=30) if os.path.exists(bandera_path) else ft.Icon(ft.Icons.FLAG, color="yellow")

                fila = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Row([img, ft.Text(row['SELECCION'], size=16, font_family="Retro8Bit", color="white")], spacing=15),
                            ft.Text(str(row['PRECIO']), size=16, font_family="Retro8Bit", weight=ft.FontWeight.BOLD, color="white")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=0,
                    border=ft.Border(bottom=ft.BorderSide(1, "grey900"))
                )
                lista_equipos.controls.append(fila)
            
            page.add(lista_equipos)
            
        except Exception as ex:
            page.add(ft.Text(f"Error: {ex}", color="red"))
            
        page.update()

    def ir_a_puntos(_):
        page.controls.clear()
        
        btn_volver = ft.Container(
            content=ft.Text("VOLVER", font_family="Retro8Bit", size=10, color="black"),
            bgcolor="yellow", padding=10, on_click=ir_a_inicio,
            border=ft.Border(top=ft.BorderSide(2, "white"), left=ft.BorderSide(2, "white"))
        )

        try:
            df = pd.read_csv("selecciones.csv", sep=";")
            # --- CÁLCULO AUTOMÁTICO ---
            df['PUNTOS_CALC'] = (df['PG'] * 3) + df['PE']+df['GF']-df['GC']-df['EXP']
            df_sorted = df.sort_values(by=["PUNTOS_CALC", "GF"], ascending=False)
            
            lista = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

            for _, row in df_sorted.iterrows():
                esta_vivo = str(row['STATUS']).upper() == "YES"
                
                # Detalle desplegable
                tile = ft.ExpansionTile(
                    title=ft.Row([
                        ft.Image(src=row['BANDERA'], width=25) if os.path.exists(row['BANDERA']) else ft.Icon(ft.Icons.FLAG),
                        ft.Text(row['SELECCION'], font_family="Retro8Bit", size=12),
                        ft.Text(f"{row['PUNTOS_CALC']} PTS", font_family="Retro8Bit", size=12, color="yellow")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    subtitle=ft.Text(f"Ronda: {row['RONDA']}", size=8, font_family="Retro8Bit",color="grey400"),
                    controls=[
                        ft.Container(
                            padding=15, bgcolor="#1a1a1a",
                            content=ft.Column([
                                ft.Text(f"PJ: {row['PJ']} | PG: {row['PG']} | PE: {row['PE']} | PP: {row['PP']}", size=12, font_family="Retro8Bit"),
                                ft.Text(f"Goles: {row['GF']} F / {row['GC']} C", size=12, font_family="Retro8Bit"),
                                ft.Text(f"Grupo: {row['GRUPO']}", size=12, color="yellow", font_family="Retro8Bit")
                            ])
                        )
                    ],
                    # Efecto apagado si está eliminado
                    opacity=1.0 if esta_vivo else 0.4 
                )
                lista.controls.append(tile)

            page.add(ft.Row([btn_volver]), ft.Text("CLASIFICACIÓN", font_family="Retro8Bit", size=20, color="yellow"), lista)
        except Exception as ex:
            page.add(ft.Text(f"Error: {ex}", color="red"))
        page.update()

    def ir_a_clasificacion(_):
        page.controls.clear()
        
        btn_volver = ft.Container(
            content=ft.Text("VOLVER", font_family="Retro8Bit", size=10, color="black"),
            bgcolor="yellow", padding=10, on_click=ir_a_inicio,
            border=ft.Border(top=ft.BorderSide(2, "white"), left=ft.BorderSide(2, "white"))
        )

        try:
            # 1. Cargar selecciones y calcular sus puntos
            df_s = pd.read_csv("selecciones.csv", sep=";")
            df_s['PTS'] = (df_s['PG'] * 3) + df_s['PE']
            
            # Crear mapa de puntos { 'ESP': 10, 'BRA': 8... } usando el nombre del archivo
            puntos_map = {row['BANDERA'].split('.')[0]: row['PTS'] for _, row in df_s.iterrows()}
            nombres_map = {row['BANDERA'].split('.')[0]: row['SELECCION'] for _, row in df_s.iterrows()}
            banderas_map = {row['BANDERA'].split('.')[0]: row['BANDERA'] for _, row in df_s.iterrows()}

            # 2. Cargar participantes
            df_p = pd.read_csv("participantes.csv", sep=";")
            
            # 3. Calcular puntos de cada porrero
            ranking_data = []
            columnas_equipos = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7']
            
            for _, p in df_p.iterrows():
                equipos_p = [p[col] for col in columnas_equipos]
                total_puntos = sum(puntos_map.get(cod, 0) for cod in equipos_p)
                ranking_data.append({
                    "NOMBRE": p['NOMBRE'],
                    "TOTAL": total_puntos,
                    "EQUIPOS": equipos_p
                })
            
            # Ordenar por puntos totales
            ranking_sorted = sorted(ranking_data, key=lambda x: x['TOTAL'], reverse=True)

            lista = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

            for pos, p in enumerate(ranking_sorted, 1):
                # Filas con espacio repartido equitativamente
                fila_banderas = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                fila_puntos = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)

                for cod in p['EQUIPOS']:
                    pts_equipo = puntos_map.get(cod, 0)
                    bandera_img = banderas_map.get(cod, "")
                    
                    # Definimos un ancho fijo para cada columna (bandera + punto)
                    # 380 de ancho total / 7 equipos ≈ 54px por hueco
                    ancho_columna = 50 

                    # Contenedor para la bandera
                    fila_banderas.controls.append(
                        ft.Container(
                            content=ft.Image(src=bandera_img, height=22, fit=ft.BoxFit.CONTAIN) if os.path.exists(bandera_img) 
                            else ft.Icon(ft.Icons.FLAG, size=20, color="yellow"),
                            width=ancho_columna,
                            alignment=ft.Alignment(0, 0) # Centrado perfecto
                        )
                    )
                    
                    # Contenedor para el punto (mismo ancho para forzar alineación)
                    fila_puntos.controls.append(
                        ft.Container(
                            content=ft.Text(
                                str(pts_equipo), 
                                size=10, 
                                font_family="Retro8Bit", 
                                color="yellow" # Cambiado a amarillo para mejor visibilidad
                            ),
                            width=ancho_columna,
                            alignment=ft.Alignment(0, 0) # Centrado perfecto
                        )
                    )

                tile = ft.ExpansionTile(
                    title=ft.Row([
                        ft.Text(f"{pos}. {p['NOMBRE']}", font_family="Retro8Bit", size=11, color="white"),
                        ft.Text(f"{p['TOTAL']} PTS", font_family="Retro8Bit", size=11, color="yellow")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    # Estética del desplegable
                    controls=[
                        ft.Container(
                            padding=ft.Padding(0, 15, 0, 20), # Usamos la clase Padding directamente
                            bgcolor="#111111",
                            content=ft.Column([
                                fila_banderas,
                                ft.Divider(height=2, color="transparent"),
                                fila_puntos
                            ], spacing=0)
                        )
                    ]
                )
                lista.controls.append(tile)

            page.add(
                ft.Row([btn_volver]), 
                ft.Text("RANKING PORREROS", font_family="Retro8Bit", size=20, color="yellow"), 
                lista
            )
            
        except Exception as ex:
            page.add(ft.Text(f"Error: {ex}", color="red"))
        
        page.update()

    def ir_a_inicio(_=None):
        page.controls.clear()
        
        titulo_retro = ft.Text(
            "LA PORRA\nDEL MUNDIAL\n2026", 
            font_family="Retro8Bit", 
            size=24, 
            color="yellow", 
            text_align=ft.TextAlign.CENTER
        )
        
# Corregido: Uso de ft.BoxFit.CONTAIN en lugar de string
        logo = ft.Image(
            src="FONDO.jpg", 
            width=420, 
            fit=ft.BoxFit.CONTAIN
        ) if os.path.exists("FONDO.jpg") else ft.Text("[FONDO.jpg no encontrado]", color="grey")
        
# Botón ultra-compatible
        btn_precios = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "ELIGE TUS 7", 
                        # Comenta la siguiente línea si sigue sin verse:
                        font_family="Retro8Bit", 
                        size=16, 
                        color="black", 
                        weight="bold"
                    )
                ],
                alignment="center", # Alineación del Row
            ),
            bgcolor="yellow",
            width=250,      # Ancho fijo para asegurar visibilidad
            height=60,      # Alto fijo
            border_radius=2,
            border=ft.Border(
                top=ft.BorderSide(4, "yellow"),
                left=ft.BorderSide(4, "yellow"),
                bottom=ft.BorderSide(4, "#333333"),
                right=ft.BorderSide(4, "#333333")
            ),
            on_click=ir_a_precios
        )
        
        btn_puntos = ft.Container(
            content=ft.Row([ft.Text("EL MUNDIAL", font_family="Retro8Bit", size=16, color="black")], alignment="center"),
            bgcolor="yellow", width=250, height=60, on_click=ir_a_puntos,
            border=ft.Border(top=ft.BorderSide(4, "yellow"), left=ft.BorderSide(4, "yellow"), bottom=ft.BorderSide(4, "#333333"), right=ft.BorderSide(4, "#333333"))
        )

        btn_ranking = ft.Container(
            content=ft.Row([ft.Text("RANKING", font_family="Retro8Bit", size=16, color="black")], alignment="center"),
            bgcolor="yellow", width=250, height=60, on_click=ir_a_clasificacion,
            border=ft.Border(top=ft.BorderSide(4, "yellow"), left=ft.BorderSide(4, "yellow"), bottom=ft.BorderSide(4, "#333333"), right=ft.BorderSide(4, "#333333"))
        )

        portada = ft.Column(
            controls=[
                ft.Divider(height=40, color="transparent"),
                titulo_retro,
                ft.Divider(height=20, color="transparent"),
                logo,
                ft.Divider(height=40, color="transparent"),
                btn_ranking,
                btn_puntos,
                btn_precios
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        page.add(portada)
        page.update()

    ir_a_inicio()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
