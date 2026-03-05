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
    
# 1. Definimos los Hechos (Facts) que el sistema manejar
class Alumno(Fact):
    """InformaciOn sobre el estado del alumno."""
    pass

class SistemaServicioSocial(KnowledgeEngine):

    @DefFacts()
    def initial_facts(self):
        yield Alumno()

    # prioridades definidas para el motor de inferencia

    #   0 - check for missing facts
    #  50 - posibly halting operations (conclusions)
    # 100 - general inferences 

    # check for missing facts 

    @Rule(Goal(kind=GoalKind.CAN_ENROLL), NOT(Alumno(porcentaje_creditos=MATCH.pc)))
    def unknown_student_credits(self):
        self.declare(Missing.create(Alumno, "porcentaje_creditos", int, "cual es el porcentaje de créditos escolares que ha obtenido? : "))
        self.halt()

    @Rule(Goal(kind=GoalKind.CAN_ENROLL), NOT(Alumno(induccion=MATCH.i)))
    def unknown_student_induccion(self):
        self.declare(Missing.create(Alumno, "induccion", bool, "ha completado el curso de inducción? : "))
        self.halt()

    @Rule(Goal(kind=GoalKind.CAN_ENROLL), NOT(Alumno(lugar_valido=MATCH.lv)))
    def unknown_student_lugar_valido(self):
        self.declare(Missing.create(Alumno, "lugar_valido", bool, "planea realizar su servicio en una institución pública o social? : "))
        self.halt()

    @Rule(Goal(kind=GoalKind.CAN_ENROLL), NOT(Alumno(nombre=MATCH.n)))
    def unknown_student_name(self):
        self.declare(Missing.create(Alumno, "nombre", str, "cómo te llamas? : "))
        self.halt()

    # posible "halting" operations (conclusions)

    # REGLA 1: Falta de créditos (Art. 146)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(porcentaje_creditos=L(70)), salience=50)
    def creditos_insuficientes(self):
        self.declare(Conclusion(text="[!] RECHAZO (Art. 146): El alumno no alcanza el 70% de créditos requeridos."))
        self.halt()

    # REGLA 2: Sin curso de inducción (Art. 148)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(induccion=False), salience=50)
    def falta_induccion(self):
        self.declare(Conclusion(text="[!] REQUISITO (Art. 148-I): Falta acreditar el curso de inducción."))
        self.halt()

    # REGLA 3: Lugar no válido (Art. 126)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(lugar_valido=False))
    def lugar_invalido(self):
        self.declare(Conclusion(text="[!] PROHIBIDO (Art. 126): El lugar elegido (privado/político) no es válido."))
        self.halt()

    # REGLA 4: Todo correcto (Elegibilidad)
    # Se activa si el alumno tiene >= 70% créditos, inducción True y lugar válido True
    @Rule(Goal(kind=GoalKind.CAN_ENROLL), Alumno(porcentaje_creditos=GE(70), 
                induccion=True, 
                lugar_valido=True))
    def alumno_apto(self):
        text = ""
        text += "\n" + "="*40
        text += "\n" + "ESTADO: ALUMNO APTO PARA INICIAR."
        text += "\n" + "="*40
        text += "\n" + "- Debe cumplir 500 horas en mínimo 6 meses."
        text += "\n" + "- Registrar informes mensuales cada 100 horas."
        
        self.declare(Conclusion(text=text))
        self.halt()

    def get_fact(self, fact_type : type):

        for i in self.facts:
            if isinstance(self.facts[i], fact_type):
                return i, self.facts[i]

        return -1, None

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