import sys
from cx_Freeze import setup,Executable
base =None
if sys.platform=="win32":
	base="Win32GUI"
setup(
	name='FerreteriaGuerrero',
	version='2.0',
	description='Primer entrega',
	executables=[Executable('Ferreteriaguerrero.py',base=base)]
	)
"""
exe=[cx_Freeze.Executable('FerreteriaGuerrero.py',base)]
cx_Freeze.setup(
	name="Ferreteria_guerrero",
	version="1.0",
	executables=exe
	)"""
#para ejecutar este se tiene que hacer asi (primero te hubicas en esta misma carpeta)
#py builder.py build