import pandas as pd 

# Cargar los archivos Excel
df_padres = pd.read_excel('servicios/input_datos/padron.xlsx',sheet_name="DatosPersonales")
df_hijos = pd.read_excel('servicios/input_datos/padron.xlsx',sheet_name="hijos")
df_laborales = pd.read_excel('servicios/input_datos/padron.xlsx',sheet_name="DatosLaborales")
df_conyuges = pd.read_excel('servicios/input_datos/padron.xlsx',sheet_name="conyuges")

# Ordenar hijos por DNI del padre y fecha de nacimiento (para asignar hijo1, hijo2, etc.)
df_hijos = df_hijos.sort_values(['Clave_foranea:', 'Fecha de Nacimiento:'])

# Agrupar hijos por padre
grupo_hijos = df_hijos.groupby('Clave_foranea:')

# Función para procesar los hijos de cada padre
def asignar_hijos(row):
    dni_padre = row['D.N.I:']
    if dni_padre in grupo_hijos.groups:
        hijos = grupo_hijos.get_group(dni_padre)
        
        # Asignar hasta 3 hijos (ajusta según tus columnas)
        for i in range(1, 8):  # hijo1, hijo2, hijo3
            col_apellido_nombre = f'Apellido/s y Nombre/s  hijo/a {i}'
            #col_apellido = f'apellido_hijo_{i}'
            col_dni = f'D.n.i hijo/a {i}'
            col_fecha = f'Fecha nacimiento hijo/a {i}'
            
            if i <= len(hijos):
                hijo = hijos.iloc[i-1]
                row[col_apellido_nombre] = hijo['Nombre y Apellido:']
                #row[col_apellido] = hijo['apellido']
                row[col_dni] = hijo['D.n.i:']
                row[col_fecha] = hijo['Fecha de Nacimiento:']
    
    return row

ordenar_columns = ["Marca temporal","Apellido/s:",
                   "Nombre/s:","D.N.I:","Tel Contacto:",
                   "Email:","Nacionalidad:","Género:",
                   "Fecha Nac:","Domicilio (Calle y n°):","Codigo Postal:",
                   "Provincia:","Localidad:","Estudios:","Titulo / Carrera:",
                   "N° De Legajo:","Comuna del sendero donde trabaja",
                   "Inicio Actividad en Prevención:","Relación de Dependencia",
                   "Esta En pareja? (Conyuge)",
                   "Nombre y Apellido ( Conyuge ) :","D.n.i ( Conyuge ) :",
                   "Fecha  de Nacimiento ( Conyuge ) :",
                   "hijo/s",
                   "Apellido/s y Nombre/s  hijo/a 1","D.n.i hijo/a 1",
                   "Fecha nacimiento hijo/a 1",
                   "Apellido/s y Nombre/s  hijo/a 2","D.n.i hijo/a 2",
                   "Fecha nacimiento hijo/a 2",
                   "Apellido/s y Nombre/s  hijo/a 3","D.n.i hijo/a 3",
                   "Fecha nacimiento hijo/a 3",
                   "Apellido/s y Nombre/s  hijo/a 4",
                   "D.n.i hijo/a 4","Fecha nacimiento hijo/a 4",
                   "Apellido/s y Nombre/s  hijo/a 5"
                    ]
# Aplicar la función a cada fila del dataframe de padres
def actualizarDatos():
    df_padres_h = df_padres.apply(asignar_hijos, axis=1)
    #combinar datos personales y su conyuges
    df_padres_actualizados = pd.merge(df_padres_h,df_conyuges,left_on='D.N.I:',
                                      right_on='Clave_foranea:',how="left")
    #eliminar columna clave_foranea de tabla conyuge
    df_padres_actualizados.drop(columns='Clave_foranea:',inplace=True)
    #combinar datos personales con datos laborales
    df_padron_actualizado = pd.merge(df_padres_actualizados,df_laborales,on='D.N.I:')

    # Guardar el resultado en un nuevo archivo Excel
    df_padron_actualizado[ordenar_columns].to_excel('servicios/output_datos/tabla_padron_actualizado.xlsx', index=False)

    return print("Migración completada. Resultado Guardado!!!")


