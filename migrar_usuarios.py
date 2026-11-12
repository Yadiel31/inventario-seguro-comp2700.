
import json
from pathlib import Path
from seguridad import crear_hash

ARCHIVO = Path(__file__).resolve().parent / "usuarios.json"

usuarios = json.loads(ARCHIVO.read_text(encoding="utf-8"))

for usuario in usuarios:
    if "clave" in usuario:
        usuario["hash"] = crear_hash(usuario.pop("clave"))

ARCHIVO.write_text(
    json.dumps(usuarios, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Migración completada.")
print("Las contraseñas ahora están protegidas con Argon2id.")
