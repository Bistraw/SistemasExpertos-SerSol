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