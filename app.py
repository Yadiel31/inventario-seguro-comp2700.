
"""Aplicación de inventario corregida."""

import json
from datetime import datetime
from pathlib import Path
from seguridad import verificar_clave

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    try:
        return json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Error: no se encontró inventario.json.")
        return None
    except json.JSONDecodeError:
        print("Error: inventario.json no contiene JSON válido.")
        return None
    except OSError:
        print("Error: no se pudo leer inventario.json.")
        return None


def guardar_inventario(productos):
    try:
        DATOS.write_text(
            json.dumps(productos, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        return True
    except OSError:
        print("Error: no se pudo guardar el inventario.")
        return False


def registrar_evento(usuario, accion, resultado, **detalles):
    evento = {
        "fecha_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
        "usuario": usuario if usuario else "sin_sesion",
        "accion": accion,
        "resultado": resultado
    }

    for campo in ("producto", "anterior", "nueva"):
        if campo in detalles:
            evento[campo] = detalles[campo]

    try:
        with LOG.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
    except OSError:
        print("Aviso: no se pudo escribir el registro de auditoría.")


def autenticar(nombre, clave):
    try:
        usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("Error: no se pudo leer usuarios.json.")
        return None

    for usuario in usuarios:
        if usuario.get("usuario") == nombre:
            if verificar_clave(usuario.get("hash", ""), clave):
                registrar_evento(nombre, "login", "exitoso")
                print("Inicio de sesión exitoso.")
                return {
                    "usuario": usuario["usuario"],
                    "rol": usuario["rol"]
                }
            break

    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def sesion_valida(sesion):
    return (
        isinstance(sesion, dict)
        and bool(sesion.get("usuario"))
        and sesion.get("rol") in ("admin", "user")
    )


def consultar_inventario(sesion):
    if not sesion_valida(sesion):
        print("Acceso denegado: debe iniciar sesión.")
        return False

    productos = cargar_inventario()

    if productos is None:
        return False

    print("\nINVENTARIO")
    for producto in productos:
        print(
            f'{producto["id"]} | '
            f'{producto["nombre"]} | '
            f'Cantidad: {producto["cantidad"]}'
        )

    return True


def validar_cantidad(entrada):
    if type(entrada) is int:
        cantidad = entrada
    elif isinstance(entrada, str):
        texto = entrada.strip()

        if not texto or not texto.isascii() or not texto.isdecimal():
            return None

        cantidad = int(texto)
    else:
        return None

    if 0 <= cantidad <= 1000:
        return cantidad

    return None


def modificar_cantidad(sesion, identificador, entrada):
    usuario = (
        sesion.get("usuario", "sin_sesion")
        if isinstance(sesion, dict)
        else "sin_sesion"
    )

    if not sesion_valida(sesion):
        print("Acceso denegado: sesión no válida.")
        registrar_evento(
            usuario, "modificar", "rechazado_sin_sesion",
            producto=identificador
        )
        return False

    if sesion.get("rol") != "admin":
        print("Acceso denegado: solo admin puede modificar.")
        registrar_evento(
            usuario, "modificar", "rechazado_permisos",
            producto=identificador
        )
        return False

    cantidad = validar_cantidad(entrada)

    if cantidad is None:
        print("Cantidad inválida. Debe ser un entero entre 0 y 1000.")
        registrar_evento(
            usuario, "modificar", "rechazado_validacion",
            producto=identificador
        )
        return False

    productos = cargar_inventario()

    if productos is None:
        return False

    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad

            if not guardar_inventario(productos):
                return False

            registrar_evento(
                usuario, "modificar", "exitoso",
                producto=identificador,
                anterior=anterior,
                nueva=cantidad
            )

            print("Cantidad actualizada correctamente.")
            return True

    print("No existe un producto con ese identificador.")
    registrar_evento(
        usuario, "modificar", "producto_inexistente",
        producto=identificador
    )
    return False



def main():
    print("Inventario académico - versión corregida")
    nombre_estudiante = input("Escriba su nombre: ")
    print("Estudiante:", nombre_estudiante)

    sesion = None

    while True:
        if sesion is None:
            nombre = input("\nUsuario (o salir): ")

            if nombre.lower() == "salir":
                break

            clave = input("Contraseña de prueba: ")
            sesion = autenticar(nombre, clave)
            continue

        if sesion["rol"] == "admin":
            print("\n1. Consultar | 2. Modificar | 3. Cerrar sesión | 0. Salir")
        else:
            print("\n1. Consultar | 3. Cerrar sesión | 0. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            consultar_inventario(sesion)

        elif opcion == "2":
            if sesion["rol"] != "admin":
                print("Opción inválida.")
                continue

            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)

        elif opcion == "3":
            sesion = None
            print("Sesión cerrada.")

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
