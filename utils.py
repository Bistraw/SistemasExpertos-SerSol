def string_to_bool(string : str) -> bool:

  string = string.lower().strip()

  if string in ["yes", "y", "si", "sí", "s"]:
    return True
  
  if string in ["no", "n"]:
    return False
  
  raise ValueError()

def print_fact(fact):
  print(f"{type(fact)} = ", end="")
  print("{ ", end="")

  for key in fact:
    print(f"{key}: {fact[key]}", end=", ")

  print(" }")

CARRERAS = {
  1: ("Ing. Bioquímico", 398),
  2: ("Ing. en Computación Inteligente", 400),
  3: ("Ing. en Electrónica", 367),
  4: ("Ing. en Sistemas Computacionales", 394),
  5: ("Ing. Industrial Estadístico", 371),
  6: ("Lic. en Biología", 383),
  7: ("Lic. en Biotecnología", 391),
  8: ("Lic. en Desarrollo de Videojuegos y Entornos Virtuales", 360),
  9: ("Lic. en Informática y Tecnologías Computacionales", 390),
  10: ("Lic. en Matemáticas Aplicadas", 351),
  11: ("Químico Farmacéutico Biólogo", 400)
}
