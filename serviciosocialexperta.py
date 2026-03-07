"""
==========================================================================================

 ██████╗  █████╗ ██╗     ██╗      ██████╗     ███████╗███╗   ██╗    ███████╗   ███████╗   
██╔════╝ ██╔══██╗██║     ██║     ██╔═══██╗    ██╔════╝████╗  ██║    ██╔════╝   ██╔════╝   
██║  ███╗███████║██║     ██║     ██║   ██║    █████╗  ██╔██╗ ██║    ███████╗   ███████╗   
██║   ██║██╔══██║██║     ██║     ██║   ██║    ██╔══╝  ██║╚██╗██║    ╚════██║   ╚════██║   
╚██████╔╝██║  ██║███████╗███████╗╚██████╔╝    ███████╗██║ ╚████║    ███████║██╗███████║██╗
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝     ╚══════╝╚═╝  ╚═══╝    ╚══════╝╚═╝╚══════╝╚═╝
__________________________________________________________________________________________
 MATERIA: SISTEMAS EXPERTOS PROBABILISTICOS
==========================================================================================
 INTEGRANTES:
__________________________________________________________________________________________                                                             
* Barrón Álvarez María Fernanda 
* Benitez Marín Leslie Miroslava
* Guzmán Solís Gael
* Martínez López Humberto 
* Merino Garfias Leonardo 
* Villalobos Araiza Jorge Luis                                                                 
==========================================================================================
"""
from enum import Enum
from experta import *

import utils

class GoalKind(Enum):
    CAN_ENROLL = 0
    CAN_REGISTER_HOURS = 1
    CAN_SUBMIT_REPORT = 2

class Goal(Fact): 
    
    @classmethod
    def create(cls, kind : GoalKind):
        fact = Goal()

        fact["kind"] = kind

        return fact

class Missing(Fact):
    
    @classmethod
    def create(cls, fact_class : type, fact_key : str, fact_value_type : type, text : str):
        fact = Missing()

        fact["fact_class"] = fact_class
        fact["fact_key"] = fact_key
        fact["fact_value_type"] = fact_value_type
        fact["text"] = text

        return fact

class Conclusion(Fact):
    
    @classmethod
    def create(cls, text : str):
        fact = Conclusion()

        fact["text"] = text
        
        return fact
    
# 1. Definimos los Hechos (Facts) que el sistema maneja
class Alumno(Fact):
    """Información sobre el estado del alumno."""
    pass

class ProyectoServicio(Fact):
    """Información del proyecto de servicio social."""
    pass

class ReporteServicio(Fact):
    """Información sobre reportes de horas."""
    pass

class SistemaServicioSocial(KnowledgeEngine):

    @DefFacts()
    def initial_facts(self):
        # NO inicializar Alumno vacío - será proveído por la GUI/test
        return
        yield  # Generator vacío

    # prioridades definidas para el motor de inferencia

    #   0 - check for missing facts
    #  50 - posibly halting operations (conclusions)
    # 100 - general inferences 

    # NOTA: La interfaz GUI suministra todos los datos al motor
    # No necesitamos fase de recolección aquí

    # ════════════════════════════════════════════════════════════════════════════════════════
    # FASE 2: VALIDAR CONDICIONES PREVIAS (Artículos 146-148)
    # Prioridad ALTA (salience=100) para detener si alguna no se cumple
    # ════════════════════════════════════════════════════════════════════════════════════════

    # Artículo 146: Mínimo 70% de créditos
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(porcentaje_creditos=P(lambda x: x < 70)), salience=100)
    def rechazo_creditos_insuficientes(self):
        text = ""
        text += "\n" + "="*60
        text += "\n" + "✗ RECHAZO: CRÉDITOS INSUFICIENTES"
        text += "\n" + "="*60
        text += "\n" + "(Art. 146) Debes completar mínimo 70% de los créditos"
        text += "\n" + "de tu plan de estudios antes de iniciar SS."
        text += "\n\n" + "Acción: Continúa con tus cursos y vuelve después."
        self.declare(Conclusion(text=text))
        self.halt()

    # Artículo 148-I: Curso de inducción obligatorio
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(induccion=False), salience=100)
    def rechazo_sin_induccion(self):
        text = ""
        text += "\n" + "="*60
        text += "\n" + "✗ REQUISITO NO CUMPLIDO: CURSO DE INDUCCIÓN"
        text += "\n" + "="*60
        text += "\n" + "(Art. 148-I) Debes acreditar el curso de inducción"
        text += "\n" + "antes de iniciar tu servicio social."
        text += "\n\n" + "Acción: Inscríbete en el próximo curso de inducción."
        self.declare(Conclusion(text=text))
        self.halt()

    # Artículo 126: Institución válida (pública o civil sin fines de lucro)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(lugar_valido=False), salience=100)
    def rechazo_lugar_invalido(self):
        text = ""
        text += "\n" + "="*60
        text += "\n" + "✗ PROHIBIDO: INSTITUCIÓN NO VÁLIDA"
        text += "\n" + "="*60
        text += "\n" + "(Art. 126) No se permite SS en empresas privadas"
        text += "\n" + "ni en asociaciones partidistas/partidos políticos."
        text += "\n\n" + "Acción: Elige una institución pública o civil válida."
        self.declare(Conclusion(text=text))
        self.halt()

    # Institución debe ser pública o sin fines de lucro
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(institucion_publica=False), salience=100)
    def rechazo_institucion_privada(self):
        text = ""
        text += "\n" + "="*60
        text += "\n" + "✗ PROHIBIDO: INSTITUCIÓN PRIVADA"
        text += "\n" + "="*60
        text += "\n" + "(Art. 136) Solo instituciones públicas o asociaciones"
        text += "\n" + "civiles sin fines de lucro pueden recibir prestadores."
        text += "\n\n" + "Acción: Selecciona una institución pública o civil."
        self.declare(Conclusion(text=text))
        self.halt()

    # Actividades válidas (no reciclaje, boteo, donativos)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(actividad_valida=False), salience=100)
    def rechazo_actividad_no_valida(self):
        text = ""
        text += "\n" + "="*60
        text += "\n" + "✗ PROHIBIDO: ACTIVIDAD NO VÁLIDA"
        text += "\n" + "="*60
        text += "\n" + "(Art. 147) NO se aceptan para SS:"
        text += "\n  • Reciclaje"
        text += "\n  • Boteo"
        text += "\n  • Entrega de donativos económicos"
        text += "\n\n" + "Acción: Propón una actividad que beneficie a"
        text += "\n" + "grupos menos favorecidos (Art. 120)."
        self.declare(Conclusion(text=text))
        self.halt()

    # ════════════════════════════════════════════════════════════════════════════════════════
    # FASE 3: CONCLUSIÓN FINAL - TODO CUMPLE
    # Se activa SOLO si TODAS las condiciones son correctas
    # ════════════════════════════════════════════════════════════════════════════════════════

    @Rule(Goal(kind=GoalKind.CAN_ENROLL), 
          Alumno(porcentaje_creditos=GE(70), 
                 induccion=True, 
                 lugar_valido=True,
                 institucion_publica=True,
                 actividad_valida=True), 
          salience=50)  # Menor prioridad que validaciones
    def aprobado_iniciar_servicio(self):
        text = ""
        text += "\n" + "="*60
        text += "\n" + "✓ ¡APROBADO! PUEDES INICIAR SERVICIO SOCIAL"
        text += "\n" + "="*60
        text += "\n\n" + "REQUISITOS CUMPLIDOS:"
        text += "\n  ✓ Art. 146: 70% de créditos completados"
        text += "\n  ✓ Art. 148-I: Curso de inducción acreditado"
        text += "\n  ✓ Art. 126: Institución pública/civil válida"
        text += "\n  ✓ Art. 147: Actividad de beneficio social"
        text += "\n\n" + "OBLIGACIONES DURANTE EL SERVICIO (Art. 148):"
        text += "\n  1. Cumplir 500 horas (Art. 148-III)"
        text += "\n  2. Duración: mínimo 6 meses, máximo 2 años"
        text += "\n  3. Reportes mensuales cada 100h (Art. 148-IV)"
        text += "\n  4. Informe final dentro de 1 mes tras terminar"
        text += "\n  5. No reportar informes fuera de plazo (Art. 153)"
        text += "\n\n" + "SANCIONES POR INCUMPLIMIENTO:"
        text += "\n  • Art. 151: Baja automática si incumples el proyecto"
        text += "\n  • Art. 152: Puedes abandonar si cambian condiciones"
        text += "\n  • Art. 153: Pierdes horas si reportas fuera de plazo"
        text += "\n\n" + "CONSTANCIA DE LIBERACIÓN:"
        text += "\n  El tutor te entregará la constancia cuando"
        text += "\n  completes las 500 horas (Art. 150)."
        
        self.declare(Conclusion(text=text))
        self.halt()


    def get_fact(self, fact_type : type):
        for i in self.facts:
            if isinstance(self.facts[i], fact_type):
                return i, self.facts[i]
        return -1, None

    def get_all_facts(self, fact_type : type):
        """Retorna todos los facts de un tipo (no solo el primero)."""
        results = []
        for i in self.facts:
            if isinstance(self.facts[i], fact_type):
                results.append((i, self.facts[i]))
        return results

if __name__ == "__main__":
    engine = SistemaServicioSocial()
    
    while True:

        engine.reset()

        engine.declare(Goal.create(GoalKind.CAN_ENROLL))

        while True:

            # for f in engine.facts:
            #    utils.print_fact(engine.facts[f])

            engine.run()

            i, conclusion = engine.get_fact(Conclusion)

            if conclusion:
                print(conclusion["text"])
                break 
            
            i, missing = engine.get_fact(Missing)

            if missing:

                m_i, missing_fact = engine.get_fact(missing["fact_class"])

                value = None

                while True:
                    try:
                        raw_value = input(missing["text"])

                        if missing["fact_value_type"] == int:
                            value = int(raw_value)

                        if missing["fact_value_type"] == bool:
                            value = utils.string_to_bool(raw_value)

                        if missing["fact_value_type"] == str:
                            value = raw_value

                        break

                    except Exception as e:
                        print("valor invalido, intenta otra vez...")

                if missing_fact:
                    engine.modify(missing_fact, **{ missing["fact_key"]: value })
                else:
                    missing_fact = missing["fact_class"]()

                    missing_fact[missing["fact_key"]] = value

                    engine.declare(missing_fact)
                
                engine.retract(i)
            else:
                print("no fue posible llegar a una conclusión con la información proveida, eres... inimaginable")

                break

        if utils.string_to_bool(input("\n¿Evaluar otro? (s/n): ")) == False:
            break