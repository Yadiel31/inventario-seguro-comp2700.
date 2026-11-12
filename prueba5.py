
import app
from contextlib import redirect_stdout
from io import StringIO

nombre = input("Escribe tu nombre: ")
print("Estudiante:", nombre)

sesion = app.autenticar("admin", "AdminDemo2700!")

if sesion is None:
    raise SystemExit("No se pudo iniciar sesión.")

app.modificar_cantidad(sesion, "P001", "10")

print("\nPRUEBA 5 - VALIDACION DE CANTIDADES")
print("-----------------------------------")

valores = ["-1", "1001", "abc", "2.5", "", "0", "1000"]

for valor in valores:
    archivo_antes = app.DATOS.read_bytes()

    with redirect_stdout(StringIO()):
        resultado = app.modificar_cantidad(sesion, "P001", valor)

    archivo_despues = app.DATOS.read_bytes()

    esperado = valor in ("0", "1000")
    correcto = resultado == esperado

    if not esperado:
        correcto = correcto and archivo_antes == archivo_despues

    print(
        f"Entrada: {valor!r:8} | "
        f"{'ACEPTADA' if resultado else 'RECHAZADA':9} | "
        f"Prueba: {'OK' if correcto else 'ERROR'}"
    )

app.modificar_cantidad(sesion, "P001", "10")

print("\nINVENTARIO FINAL:")
app.consultar_inventario(sesion)
