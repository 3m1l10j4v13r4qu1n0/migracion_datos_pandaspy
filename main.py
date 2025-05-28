from modulos.migracion_hijos import actualizarDatos
if __name__ == "__main__":
    # Código que se ejecuta solo cuando el archivo se corre directamente
    a = actualizarDatos()
    print(a)
    #print(type(encabezados))
    print("Este script se está ejecutando directamente")
else:
    print("Este script se ha importado como módulo")