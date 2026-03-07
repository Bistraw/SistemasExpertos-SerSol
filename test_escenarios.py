"""
Script de prueba rápida - Sistema Experto de Servicio Social
Ejecuta diferentes escenarios sin necesidad de la GUI

Uso: python test_escenarios.py
"""

from serviciosocialexperta import (
    SistemaServicioSocial, Goal, GoalKind, Alumno, Conclusion, Missing
)

# Colores para terminal
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def test_scenario(nombre_escenario, datos_alumno):
    """Ejecuta un escenario y muestra el resultado."""
    print(f"\n{AZUL}{'='*70}")
    print(f"ESCENARIO: {nombre_escenario}")
    print(f"{'='*70}{RESET}\n")

    # Mostrar datos ingresados
    print(f"{NEGRITA}Datos ingresados:{RESET}")
    for key, value in datos_alumno.items():
        print(f"  {key:30s}: {value}")

    # Ejecutar motor experto
    engine = SistemaServicioSocial()
    engine.reset()
    
    # Declarar Goal
    engine.declare(Goal.create(GoalKind.CAN_ENROLL))
    
    # Declarar Alumno con TODOS los datos
    alumno = Alumno(
        nombre=datos_alumno.get("nombre", ""),
        porcentaje_creditos=datos_alumno.get("porcentaje_creditos", 0),
        induccion=datos_alumno.get("induccion", False),
        lugar_valido=datos_alumno.get("lugar_valido", False),
        semestre=datos_alumno.get("semestre", 0),
        institucion_publica=datos_alumno.get("institucion_publica", False),
        actividad_valida=datos_alumno.get("actividad_valida", False),
    )
    engine.declare(alumno)
    
    # Ejecutar el motor
    engine.run()
    
    # Obtener conclusión
    _, conclusion = engine.get_fact(Conclusion)
    conclusion_text = conclusion["text"] if conclusion else None

    # Mostrar resultado
    if not conclusion_text:
        conclusion_text = "No fue posible llegar a una conclusión."

    print(f"\n{NEGRITA}RESULTADO:{RESET}")
    if "APROBADO" in conclusion_text:
        print(f"{VERDE}{conclusion_text}{RESET}")
    elif any(k in conclusion_text for k in ("RECHAZO", "PROHIBIDO", "REQUISITO")):
        print(f"{ROJO}{conclusion_text}{RESET}")
    else:
        print(f"{AMARILLO}{conclusion_text}{RESET}")


def main():
    print(f"\n{NEGRITA}{AZUL}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║        PRUEBAS DE ESCENARIOS - SISTEMA EXPERTO SS                  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    # ESCENARIO 1: APROBADO
    test_scenario(
        "✓ APROBADO - Todas las condiciones cumplidas",
        {
            "nombre": "Juan Pérez García",
            "porcentaje_creditos": 70,  # 280/400
            "induccion": True,
            "lugar_valido": True,
            "semestre": 6,
            "institucion_publica": True,
            "actividad_valida": True,
        },
    )

    # ESCENARIO 2: CRÉDITOS INSUFICIENTES
    test_scenario(
        "✗ CRÉDITOS INSUFICIENTES (62.5% < 70%)",
        {
            "nombre": "María López",
            "porcentaje_creditos": 62,  # 250/400
            "induccion": True,
            "lugar_valido": True,
            "semestre": 5,
            "institucion_publica": True,
            "actividad_valida": True,
        },
    )

    # ESCENARIO 3: SIN INDUCCIÓN
    test_scenario(
        "✗ SIN CURSO DE INDUCCIÓN",
        {
            "nombre": "Carlos Mendez",
            "porcentaje_creditos": 75,  # 300/400
            "induccion": False,
            "lugar_valido": True,
            "semestre": 7,
            "institucion_publica": True,
            "actividad_valida": True,
        },
    )

    # ESCENARIO 4: INSTITUCIÓN PRIVADA
    test_scenario(
        "✗ INSTITUCIÓN PRIVADA",
        {
            "nombre": "Ana García",
            "porcentaje_creditos": 72,  # 290/400
            "induccion": True,
            "lugar_valido": True,
            "semestre": 6,
            "institucion_publica": False,
            "actividad_valida": True,
        },
    )

    # ESCENARIO 5: LUGAR NO VÁLIDO
    test_scenario(
        "✗ LUGAR NO VÁLIDO (Empresa privada/política)",
        {
            "nombre": "Roberto Silva",
            "porcentaje_creditos": 71,  # 285/400
            "induccion": True,
            "lugar_valido": False,
            "semestre": 6,
            "institucion_publica": True,
            "actividad_valida": True,
        },
    )

    # ESCENARIO 6: ACTIVIDAD NO VÁLIDA
    test_scenario(
        "✗ ACTIVIDAD NO VÁLIDA (Reciclaje/Boteo/Donativos)",
        {
            "nombre": "Sofia Ruiz",
            "porcentaje_creditos": 80,  # 320/400
            "induccion": True,
            "lugar_valido": True,
            "semestre": 8,
            "institucion_publica": True,
            "actividad_valida": False,
        },
    )

    # ESCENARIO 7: MÚLTIPLES PROBLEMAS
    test_scenario(
        "✗ MÚLTIPLES PROBLEMAS (Detiene en el primero)",
        {
            "nombre": "Pedro López",
            "porcentaje_creditos": 50,  # 200/400 - FALLA
            "induccion": False,  # FALLA
            "lugar_valido": False,  # FALLA
            "semestre": 4,
            "institucion_publica": False,  # FALLA
            "actividad_valida": False,  # FALLA
        },
    )

    # ESCENARIO 8: APROBADO CON MÁS CRÉDITOS
    test_scenario(
        "✓ APROBADO - 87.5% de créditos (350/400)",
        {
            "nombre": "Patricia Martínez",
            "porcentaje_creditos": 87,
            "induccion": True,
            "lugar_valido": True,
            "semestre": 8,
            "institucion_publica": True,
            "actividad_valida": True,
        },
    )

    # ESCENARIO 9: APROBADO EXACTO 70%
    test_scenario(
        "✓ APROBADO - EXACTO 70% de créditos",
        {
            "nombre": "Gabriel Torres",
            "porcentaje_creditos": 70,
            "induccion": True,
            "lugar_valido": True,
            "semestre": 6,
            "institucion_publica": True,
            "actividad_valida": True,
        },
    )

    print(f"\n{AZUL}{'='*70}")
    print("FIN DE PRUEBAS")
    print(f"{'='*70}{RESET}\n")

    print(f"{NEGRITA}Resumen:{RESET}")
    print("  ✓ Escenarios de APROBACIÓN: 3")
    print("  ✗ Escenarios de RECHAZO: 6")
    print("\nPara más información, consulta EJEMPLOS_USO.md\n")


if __name__ == "__main__":
    main()
