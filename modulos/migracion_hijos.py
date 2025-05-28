import pandas as pd 

from openpyxl import load_workbook

# Cargar los archivos Excel
excel_arch= 'servicios/input_datos/padron.xlsx'
hoja_personal= 'DatosPersonales'
hoja_lavorales = 'DatosLaborales'
hoja_conyuges = 'conyuges'
hoja_hijos = 'hijos'

#DataFrame
df_padres = pd.read_excel(excel_arch, sheet_name= hoja_personal)
df_hijos = pd.read_excel(excel_arch,sheet_name= hoja_hijos)
df_laborales = pd.read_excel(excel_arch,sheet_name= hoja_lavorales)
df_conyuges = pd.read_excel(excel_arch,sheet_name=hoja_conyuges)

#ver los encabezados de las columnas
columns_pesonales = df_padres.columns.tolist()
columns_hijos = df_hijos.columns.tolist()
columns_laborales = df_laborales.columns.tolist()
columns_conyuges = df_conyuges.columns.tolist()

#asignar clave primaria y clave foranea
primary_key = columns_pesonales[0]
hijos_foranea_key = columns_hijos[0]
laborales_foranea_key = columns_laborales[0]
conyuges_foranea_key = columns_conyuges[0]

# Ordenar hijos por DNI del padre y fecha de nacimiento (para asignar hijo1, hijo2, etc.)
df_hijos = df_hijos.sort_values(hijos_foranea_key)#(['dni_padre', 'fecha_nacimiento'])

# Agrupar hijos por padre
grupo_hijos = df_hijos.groupby(hijos_foranea_key)

# Función para procesar los hijos de cada padre
def asignar_hijos(row):
    dni_padre = row[primary_key]
    if dni_padre in grupo_hijos.groups:
        hijos = grupo_hijos.get_group(dni_padre)
        
        # Asignar hasta 7 hijos (ajusta según tus columnas)
        for i in range(1, 8):  # hijo1, hijo2, hijo(n)
            col_apellido_nombre = f'Apellido/s y Nombre/s  hijo/a {i}'
            col_dni = f'D.n.i hijo/a {i}'
            col_fecha = f'Fecha nacimiento hijo/a {i}'
            
            if i <= len(hijos):
                hijo = hijos.iloc[i-1]
                row[col_apellido_nombre] = hijo['Nombre y Apellido:']
                row[col_dni] = hijo['D.n.i:']
                row[col_fecha] = hijo['Fecha de Nacimiento:']
    
    return row
# Ordenar datos laborales
df_conyuges = df_conyuges.sort_values(conyuges_foranea_key)

#Agrupar conyuges
grupo_conyuges = df_conyuges.groupby(conyuges_foranea_key)

#funcion para procesar conyuges
def asignar_conyuges(row):
    pk = row[primary_key]
    if pk in grupo_conyuges.groups:
        conyuge = grupo_conyuges.get_group(pk)
        col_apellido_nombre = f'Nombre y Apellido ( Conyuge ) :'
        col_dni = f'D.n.i ( Conyuge ) :'
        col_fecha = f'Fecha  de Nacimiento ( Conyuge ) :'
            
        
        row[col_apellido_nombre] = conyuge['Nombre y Apellido:']
        row[col_dni] = conyuge['D.n.i:']
        row[col_fecha] = conyuge['Fecha  de Nacimiento:']
    


# Crear DataFrame con nuevos datos
# def crearDataFrame(df,archivo,hoja,encabezado):
#     wb = load_workbook(archivo)
#     ws = wb[hoja]
#     # Escribir los datos manualmente a partir de la segunda fila
#     for i, row in df.iterrows():
#         ws.cell(row=i+1, column= i+1, value=row[encabezado[i+1]])  
#         #ws.cell(row=i+1, column=2, value=row['Columna2'])  # Columna B

#     # Guardar cambios
#     wb.save(archivo)
    
# Aplicar la función a cada fila del dataframe de padres
def actualizarDatos():
    df_padres.apply(asignar_hijos, axis=1)
    df_padres.apply(asignar_conyuges, axis=1)
    df_padron_actualizado = df_padres
    # crearDataFrame(df=df_padres_actualizado,archivo=excel_arch_padre,
    #                hoja=hoja_descarga,encabezado=encabezados)

    # Guardar el resultado en un nuevo archivo Excel
    #df_padres_actualizado.to_excel('servicios/output_datos/tabla_padres_actualizada.xlsx', index=False)

    #return 
    print("Migración completada. Resultado guardado en 'tabla_padres_actualizada.xlsx'")
    return df_padron_actualizado
