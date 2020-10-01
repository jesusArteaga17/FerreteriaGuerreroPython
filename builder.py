from cx_Freeze import setup, Executable
setup(name="Productos",
      version="1.0",
      description="Ventana",
      executables=[Executable("ViewProductos.py")],)