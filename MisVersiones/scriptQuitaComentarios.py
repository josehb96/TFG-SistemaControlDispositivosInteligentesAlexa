import re

with open("FinalGame copy.py", "r") as f:
    codigo = f.read()

# Eliminar los comentarios de una sola línea
codigo = re.sub(r"^\s*#.*?$", "", codigo, flags=re.MULTILINE)

# Eliminar los comentarios al lado de una línea de código
codigo = re.sub(r"([^\'\"])(#.*?$)", r"\1", codigo, flags=re.MULTILINE)

# Eliminar los comentarios de varias líneas
codigo = re.sub(r"^\s*('''|\"\"\").*?('''|\"\"\")", "", codigo, flags=re.MULTILINE | re.DOTALL)

with open("FinalGame sin comentarios.py", "w") as f:
    f.write(codigo)
