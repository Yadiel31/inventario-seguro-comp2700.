
# Inventario Academico - COMP 2700

Estudiante: Yadiel Ruiz

## Descripcion

Este proyecto consiste en corregir una aplicacion de inventario en Python que tenia varios problemas de seguridad.

Se corrigieron las contrasenas, los permisos de los usuarios, la validacion de cantidades y el registro de auditoria.

## Funciones del programa

- Inicio de sesion con usuario y contrasena.
- Contrasenas protegidas utilizando Argon2id.
- Admin puede consultar y modificar cantidades.
- User solamente puede consultar.
- Cantidades permitidas entre 0 y 1000.
- Los cambios se guardan en inventario.json.
- Registro de eventos en auditoria.jsonl.
- Manejo de archivos ausentes y JSON invalido.

## Requisitos

- Python 3.10 o superior.
- Biblioteca argon2-cffi.

## Instalacion y ejecucion

1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto en VS Code.
3. Crear el entorno virtual:

python -m venv .venv

4. Instalar las dependencias:

python -m pip install -r requirements.txt

5. Ejecutar el programa:

python app.py

El archivo usuarios.json publicado ya contiene los hashes de las cuentas de prueba. migrar_usuarios.py se utilizo para convertir las contrasenas originales.

## Cuentas de prueba

Admin:
Usuario: admin
Contrasena: AdminDemo2700!

User:
Usuario: user
Contrasena: UserDemo2700!

Estas cuentas son ficticias y solo se utilizan para el proyecto.

## Archivos principales

- app.py: programa principal.
- seguridad.py: funciones de Argon2id.
- migrar_usuarios.py: conversion de contrasenas a hashes.
- prueba5.py: pruebas de validacion.
- inventario.json: productos y cantidades.
- usuarios.json: usuarios con hashes.
- auditoria_ejemplo.jsonl: muestra de auditoria.
- requirements.txt: dependencias.

## Pruebas realizadas

1. Se verifico el inicio de sesion correcto e incorrecto.
2. Se comprobo que un usuario inexistente es rechazado.
3. Se verifico que user no puede modificar cantidades.
4. Se comprobo que sin sesion no se puede consultar ni modificar.
5. Se probaron las cantidades -1, 1001, abc, 2.5, vacia, 0 y 1000.
6. Se modifico P001 de 10 a 20.
7. Se comprobo que P999 no existe y no se crea.
8. Se verifico que P001 conserva la cantidad 20 al reiniciar.
9. Se revisaron los registros de auditoria.
10. Se probaron los errores de archivo ausente y JSON invalido.

Los resultados se comprobaron en la terminal y se tomaron capturas para Blackboard.

## Uso de inteligencia artificial

Utilice ChatGPT de OpenAI para ayudarme a revisar el codigo original, corregir los problemas de seguridad y preparar las pruebas.

Tambien lo utilice para comprender como funcionan los hashes, los permisos y la auditoria.

Comprobe las sugerencias ejecutando el programa y revisando los resultados de las pruebas.

## Fuentes

- Instrucciones y archivos originales del curso COMP 2700.
- Documentacion de Python: https://docs.python.org/3/
- Documentacion de argon2-cffi: https://argon2-cffi.readthedocs.io/

## Limitaciones

Este programa es un prototipo academico y no ofrece seguridad completa.

Una persona con acceso directo a los archivos JSON podria modificarlos fuera del programa.

No incluye autenticacion de multiples factores, cifrado de archivos ni proteccion contra cambios externos en la auditoria.

Una mejora futura seria proteger los archivos utilizando permisos del sistema operativo.
