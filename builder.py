from cx_Freeze import setup, Executable
setup(name="Inventario",
      version="1.0",
      description="Ventana",
      executables=[Executable("ViewInventario.py")],)
#para ejecutar este se tiene que hacer asi (primero te hubicas en esta misma carpeta)
#py builder.py build