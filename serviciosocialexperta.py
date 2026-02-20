from experta import *

# 1. Definimos los Hechos (Facts) que el sistema manejará
class Alumno(Fact):
    """Información sobre el estado del alumno."""
    pass

class SistemaServicioSocial(KnowledgeEngine):
    
    # REGLA 1: Falta de créditos (Art. 146)
    @Rule(Alumno(porcentaje_creditos=L(70)))
    def creditos_insuficientes(self):
        print("\n[!] RECHAZO (Art. 146): El alumno no alcanza el 70% de créditos requeridos.")

    # REGLA 2: Sin curso de inducción (Art. 148)
    @Rule(Alumno(induccion=False))
    def falta_induccion(self):
        print("[!] REQUISITO (Art. 148-I): Falta acreditar el curso de inducción.")

    # REGLA 3: Lugar no válido (Art. 126)
    @Rule(Alumno(lugar_valido=False))
    def lugar_invalido(self):
        print("[!] PROHIBIDO (Art. 126): El lugar elegido (privado/político) no es válido.")

    # REGLA 4: Todo correcto (Elegibilidad)
    # Se activa si el alumno tiene >= 70% créditos, inducción True y lugar válido True
    @Rule(Alumno(porcentaje_creditos=GE(70), 
                 induccion=True, 
                 lugar_valido=True))
    def alumno_apto(self):
        print("\n" + "="*40)
        print("ESTADO: ALUMNO APTO PARA INICIAR.")
        print("="*40)
        print("- Debe cumplir 500 horas en mínimo 6 meses.")
        print("- Registrar informes mensuales cada 100 horas.")

# --- Lógica de Interfaz (Fuera del motor de inferencia) ---

def solicitar_datos():
    print("\n--- INGRESO DE DATOS DEL ALUMNO ---")
    nombre = input("Nombre: ")
    try:
        total = float(input("Total créditos carrera: "))
        aprobados = float(input("Créditos aprobados: "))
        porc = (aprobados / total) * 100
        
        induccion = input("¿Acreditó inducción? (s/n): ").lower() == 's'
        lugar = input("¿Institución pública o social? (s/n): ").lower() == 's'
        
        return {
            "nombre": nombre,
            "porc": porc,
            "induccion": induccion,
            "lugar": lugar
        }
    except ZeroDivisionError:
        print("Error: El total de créditos no puede ser 0.")
        return None

if __name__ == "__main__":
    engine = SistemaServicioSocial()
    
    while True:
        datos = solicitar_datos()
        if datos:
            print(f"\nDIAGNÓSTICO PARA: {datos['nombre'].upper()}")
            print(f"Avance actual: {datos['porc']:.2f}%")
            
            # Resetear el motor y cargar los hechos
            engine.reset()
            engine.declare(Alumno(
                porcentaje_creditos=datos['porc'],
                induccion=datos['induccion'],
                lugar_valido=datos['lugar']
            ))
            
            # Ejecutar el motor de inferencia
            engine.run()
            
        if input("\n¿Evaluar otro? (s/n): ").lower() != 's':
            break