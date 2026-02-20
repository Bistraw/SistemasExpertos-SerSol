import sys

class SistemaExpertoServicioSocial:
    def __init__(self):
        self.divisor = "=" * 65

    def bienvenida(self):
        print("\n" + self.divisor)
        print("   SISTEMA EXPERTO: VALIDACION DE SERVICIO SOCIAL")
        print("        (Reglamento General de Docencia - Cap. XIII)")
        print(self.divisor)

    def explicar_creditos(self):
        print("\nDEFINICION DE CREDITOS CUMPLIDOS:")
        print("Es el valor numerico de las materias que han sido aprobadas.")
        print("No se consideran las materias cursadas actualmente sin calificacion.")
        print("Segun el Art. 146, se requiere el 70% de avance para iniciar.")

    def solicitar_datos(self):
        datos = {}
        print("\n--- [1] DATOS DEL ALUMNO ---")
        datos['nombre'] = input("Nombre completo del alumno: ")
        
        try:
            total_c = float(input("Total de creditos de la carrera (Plan de estudios): "))
            aprob_c = float(input("Cantidad de creditos aprobados actualmente: "))
            datos['porc_creditos'] = (aprob_c / total_c) * 100
            datos['faltantes'] = max(0.0, (total_c * 0.70) - aprob_c)
        except ValueError:
            print("ERROR: Ingrese valores numericos para los creditos.")
            return None

        print("\n--- [2] REQUISITOS OBLIGATORIOS (Art. 148) ---")
        datos['induccion'] = input("Acredito el curso de induccion? (s/n): ").lower() == 's'
        
        print("\n--- [3] LUGAR DE REALIZACION (Art. 126) ---")
        print("Restriccion: No se permite en empresas privadas o partidos politicos.")
        tipo = input("La institucion es publica o de asistencia social? (s/n): ").lower()
        datos['es_lugar_valido'] = (tipo == 's')
        
        return datos

    def evaluar(self, datos):
        print("\n" + "=" * 65)
        print(f"DIAGNOSTICO DE SERVICIO SOCIAL: {datos['nombre'].upper()}")
        print("=" * 65)
        
        errores = []
        
        # Art. 146: Porcentaje de creditos
        if datos['porc_creditos'] < 70:
            errores.append(f"BLOQUEO (Art. 146): El alumno posee el {datos['porc_creditos']:.1f}% de creditos. "
                           f"Faltan {datos['faltantes']:.1f} creditos para el minimo requerido.")
        
        # Art. 148: Curso de induccion
        if not datos['induccion']:
            errores.append("REQUISITO (Art. 148-I): Falta acreditacion del curso de induccion.")
            
        # Art. 126: Tipo de institucion
        if not datos['es_lugar_valido']:
            errores.append("PROHIBIDO (Art. 126): El lugar elegido no es valido por normativa.")

        # Resultado de elegibilidad
        if not errores:
            print("ESTADO: ALUMNO APTO PARA INICIAR.")
            print("\nLINEAMIENTOS POST-INSCRIPCION:")
            print("- Cumplir 500 horas en un minimo de 6 meses (Art. 148-III).")
            print("- Registro de informes mensuales cada 100 horas (Art. 148-IV).")
        else:
            print("ESTADO: ALUMNO NO APTO.")
            print("MOTIVOS DE RECHAZO:")
            for e in errores:
                print(f"   * {e}")
        
        print("\nNOTIFICACION DE SANCIONES (Art. 151-153):")
        print("La falta de registro de informes en tiempo o el abandono por causas")
        print("imputables al alumno resultara en la baja sin horas acumuladas.")

def ejecutar():
    sistema = SistemaExpertoServicioSocial()
    while True:
        sistema.bienvenida()
        sistema.explicar_creditos()
        
        datos_alumno = sistema.solicitar_datos()
        
        if datos_alumno:
            sistema.evaluar(datos_alumno)
        
        repetir = input("\nDesea evaluar a otro alumno? (s/n): ").lower()
        if repetir != 's':
            print("Finalizando programa.")
            break

if __name__ == "__main__":
    ejecutar()