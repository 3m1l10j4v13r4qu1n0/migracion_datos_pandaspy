import pandas as pd

# --- FUNCIONES ---

def marcar_pareja_e_hijos(df):
    """
    Marca con 1 si tiene pareja o hijos. 0 si no los tiene.
    Usa texto 'no dato' como referencia de valor vacío.
    """

    # Marcar pareja solo si el texto no es 'no dato'
    df['Esta En pareja? (Conyuge)'] = (df['Nombre y Apellido ( Conyuge ) :'] != 'no dato').astype(int)

    # Marcar hijos: al menos uno de los campos no debe ser 'no dato'
    df['hijo/s'] = (df['Apellido/s y Nombre/s hijo/a 1'] != 'no dato').astype(int)
    
    return df


def limpiar_nulos_personalizada(df):
    """
    Reemplaza nulos según tipo:
    - Números → 0
    - Fechas → 1990-01-01
    - Cadenas → 'no dato'
    """
    fecha_default = pd.to_datetime("1990-01-01")
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].fillna(fecha_default)
        else:
            df[col] = df[col].fillna("no dato")
    return df

def procesar_hijos(df_hijos):
    """
    Devuelve un DataFrame pivotado con hasta 7 hijos por padre.
    """
    df_hijos = df_hijos.sort_values(['Clave_foranea:', 'Fecha de Nacimiento:'])
    df_hijos['n_hijo'] = df_hijos.groupby('Clave_foranea:').cumcount() + 1

    df_hijos.rename(columns={
        'Clave_foranea:': 'D.N.I:',
        'Nombre y Apellido:': 'Apellido/s y Nombre/s',
        'D.n.i:': 'D.n.i',
        'Fecha de Nacimiento:': 'Fecha nacimiento'
    }, inplace=True)

    df_hijos_pivot = df_hijos.pivot(index='D.N.I:', columns='n_hijo', values=['Apellido/s y Nombre/s', 'D.n.i', 'Fecha nacimiento'])
    df_hijos_pivot.columns = [f'{label} hijo/a {num}' for label, num in df_hijos_pivot.columns]
    df_hijos_pivot.reset_index(inplace=True)
    
    return df_hijos_pivot

def actualizarDatos():
    # Leer datos

    try:
        df_padres = pd.read_excel('servicios/input_datos/padron.xlsx', sheet_name="DatosPersonales")
        df_hijos = pd.read_excel('servicios/input_datos/padron.xlsx', sheet_name="hijos")
        df_laborales = pd.read_excel('servicios/input_datos/padron.xlsx', sheet_name="DatosLaborales")
        df_conyuges = pd.read_excel('servicios/input_datos/padron.xlsx', sheet_name="conyuges")
        
    except Exception as e:
        print("Error al leer el archivo:", e)
        raise

    # Limpiar nulos
    df_padres = limpiar_nulos_personalizada(df_padres)
    df_hijos = limpiar_nulos_personalizada(df_hijos)
    df_laborales = limpiar_nulos_personalizada(df_laborales)
    df_conyuges = limpiar_nulos_personalizada(df_conyuges)
    

    # Procesar hijos
    df_hijos_pivot = procesar_hijos(df_hijos)

    # Combinar todo
    df_merged = pd.merge(df_padres, df_hijos_pivot, on='D.N.I:', how='left')
    df_merged = pd.merge(df_merged, df_conyuges, left_on='D.N.I:', right_on='Clave_foranea:', how='left')
    df_merged = pd.merge(df_merged, df_laborales, on='D.N.I:', how='left')

    if 'Clave_foranea:' in df_merged.columns:
        df_merged.drop(columns='Clave_foranea:', inplace=True)


    # Orden final de columnas
    ordenar_columns = [
        "Marca temporal", "Apellido/s:", "Nombre/s:", "D.N.I:", "Tel Contacto:", "Email:",
        "Nacionalidad:", "Género:", "Fecha Nac:", "Domicilio (Calle y n°):", "Codigo Postal:",
        "Provincia:", "Localidad:", "Estudios:", "Titulo / Carrera:", "N° De Legajo:",
        "Comuna del sendero donde trabaja", "Inicio Actividad en Prevención:", "Relación de Dependencia",
        "Esta En pareja? (Conyuge)", "Nombre y Apellido ( Conyuge ) :", "D.n.i ( Conyuge ) :",
        "Fecha  de Nacimiento ( Conyuge ) :", "hijo/s"
    ]

    for i in range(1, 8):
        ordenar_columns.extend([
            f'Apellido/s y Nombre/s hijo/a {i}',
            f'D.n.i hijo/a {i}',
            f'Fecha nacimiento hijo/a {i}'
        ])

    # Asegurar que solo las columnas que existan se usen
    columnas_finales = [col for col in ordenar_columns if col in df_merged.columns]

    #Limpiar datos nulos de df_merged
    df_merged = limpiar_nulos_personalizada(df_merged)
    
    # Marcar pareja e hijos
    df_merged = marcar_pareja_e_hijos(df_merged)

    # Guardar archivo final
    df_merged[columnas_finales].to_excel('servicios/output_datos/tabla_padron_actualizado.xlsx', index=False)
    print("Migración completada. Resultado guardado.")

    
# --- EJECUTAR ---
#actualizarDatos()
