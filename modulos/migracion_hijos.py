import pandas as pd 

# Cargar los archivos Excel
df_padres = pd.read_excel('tabla_padres.xlsx')
df_hijos = pd.read_excel('tabla_hijos.xlsx')

# Ordenar hijos por DNI del padre y fecha de nacimiento (para asignar hijo1, hijo2, etc.)
df_hijos = df_hijos.sort_values(['dni_padre', 'fecha_nacimiento'])

# Agrupar hijos por padre
grupo_hijos = df_hijos.groupby('dni_padre')

# Función para procesar los hijos de cada padre
def asignar_hijos(row):
    dni_padre = row['dni']
    if dni_padre in grupo_hijos.groups:
        hijos = grupo_hijos.get_group(dni_padre)
        
        # Asignar hasta 3 hijos (ajusta según tus columnas)
        for i in range(1, 8):  # hijo1, hijo2, hijo3
            col_apellido_nombre = f'apellido_nombre_hijo_{i}'
            #col_apellido = f'apellido_hijo_{i}'
            col_dni = f'dni_hijo_{i}'
            col_fecha = f'fecha_nacimiento_hijo_{i}'
            
            if i <= len(hijos):
                hijo = hijos.iloc[i-1]
                row[col_apellido_nombre] = hijo['apellido_nombre']
                #row[col_apellido] = hijo['apellido']
                row[col_dni] = hijo['dni']
                row[col_fecha] = hijo['fecha_nacimiento']
    
    return row

# Aplicar la función a cada fila del dataframe de padres
df_padres_actualizado = df_padres.apply(asignar_hijos, axis=1)

# Guardar el resultado en un nuevo archivo Excel
df_padres_actualizado.to_excel('tabla_padres_actualizada.xlsx', index=False)

print("Migración completada. Resultado guardado en 'tabla_padres_actualizada.xlsx'")
#print(df_padres)
#print(df_hijos)


