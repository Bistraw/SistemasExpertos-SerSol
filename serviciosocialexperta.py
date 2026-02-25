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
    def create(cls, kind: GoalKind):
        fact = Goal()
        fact["kind"] = kind
        return fact


class Missing(Fact):
    @classmethod
    def create(cls, fact_class: type, fact_key: str, fact_value_type: type, text: str):
        fact = Missing()
        fact["fact_class"] = fact_class
        fact["fact_key"] = fact_key
        fact["fact_value_type"] = fact_value_type
        fact["text"] = text
        return fact


class Conclusion(Fact):
    @classmethod
    def create(cls, text: str):
        fact = Conclusion()
        fact["text"] = text
        return fact


# Facts - Hechos
# 1. Definimos los Hechos (Facts) que el sistema manejar�
class Alumno(Fact):
    """Información del alumno"""
    pass


# Motor de inferencia
class SistemaServicioSocial(KnowledgeEngine):

    @DefFacts()
    def initial_facts(self):
        yield Alumno()

    # Prioridades definidas para el motor de inferencia

    #   0 - check for missing facts
    #  50 - posibly halting operations (conclusions)
    # 100 - general inferences 

    # check for missing facts 

    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          NOT(Alumno(nombre=MATCH.n)))
    def ask_nombre(self):
        self.declare(Missing.create(
            Alumno, "nombre", str,
            "¿Cómo te llamas? : "
        ))
        self.halt()

    #Regla para seleccionar carrera
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          NOT(Alumno(carrera=MATCH.c)))
    def ask_carrera(self):

        print("\nSelecciona tu carrera:\n")

        for key, value in utils.CARRERAS.items():
            print(f"{key}. {value[0]} - Total créditos: {value[1]}")

        self.declare(Missing.create(
            Alumno,
            "carrera",
            int,
            "Ingresa el número de tu carrera: "
        ))
        self.halt()

    @Rule(Alumno(carrera=MATCH.c),
          NOT(Alumno(total_creditos=MATCH.t)))
    def assign_total_creditos(self, c):

        if c in utils.CARRERAS:
            total = utils.CARRERAS[c][1]
            nombre_carrera = utils.CARRERAS[c][0]

            print(f"\nHas seleccionado: {nombre_carrera}")
            print(f"Total de créditos del plan: {total}")

            fact_id, alumno = self.get_fact(Alumno)
            self.modify(alumno, total_creditos=total)

        else:
            print("Carrera inválida.")
            self.halt()

    #Regla para seleccionar si se ingresan creditos o porcentajes
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          Alumno(carrera=MATCH.c),
          NOT(Alumno(modo_ingreso=MATCH.m)))
    def ask_modo_ingreso(self):

        print("\n¿Cómo deseas ingresar tu avance académico?")
        print("1. Ingresar créditos obtenidos")
        print("2. Ingresar porcentaje directamente")

        self.declare(Missing.create(
            Alumno,
            "modo_ingreso",
            int,
            "Selecciona 1 o 2: "
        ))
        self.halt()

    #Ingresar el numero de creditos
    @Rule(Alumno(modo_ingreso=1),
          NOT(Alumno(creditos_obtenidos=MATCH.co)))
    def ask_creditos(self):

        self.declare(Missing.create(
            Alumno,
            "creditos_obtenidos",
            int,
            "¿Cuántos créditos has obtenido? : "
        ))
        self.halt()

    @Rule(Alumno(modo_ingreso=1,
                 creditos_obtenidos=MATCH.co,
                 total_creditos=MATCH.tc),
          NOT(Alumno(porcentaje_creditos=MATCH.p)))
    def calcular_porcentaje(self, co, tc):

        porcentaje = int((co / tc) * 100)

        print(f"\nTu porcentaje calculado es: {porcentaje}%")

        fact_id, alumno = self.get_fact(Alumno)
        self.modify(alumno, porcentaje_creditos=porcentaje)

    #Ingreso de porcentaje directamente
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          Alumno(modo_ingreso=2),
          NOT(Alumno(porcentaje_creditos=MATCH.pc)))
    def ask_porcentaje(self):

        self.declare(Missing.create(
            Alumno,
            "porcentaje_creditos",
            int,
            "¿Cuál es el porcentaje de créditos que has obtenido? : "
        ))
        self.halt()

    #Valida curso de induccion
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          NOT(Alumno(induccion=MATCH.i)))
    def ask_induccion(self):

        self.declare(Missing.create(
            Alumno,
            "induccion",
            bool,
            "¿Has completado el curso de inducción? (s/n): "
        ))
        self.halt()

    #Valida si la institucion es publica o de interes social
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          NOT(Alumno(lugar_valido=MATCH.lv)))
    def ask_lugar(self):

        self.declare(Missing.create(
            Alumno,
            "lugar_valido",
            bool,
            "¿Realizarás tu servicio en institución pública o social? (s/n): "
        ))
        self.halt()

    # Posible "halting" operations (conclusions)

    # REGLA 1: Falta de créditos (Art. 146)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          Alumno(porcentaje_creditos=P(lambda x: x < 70)),
          salience=50)
    def creditos_insuficientes(self):

        self.declare(Conclusion.create(
            "[!] RECHAZO (Art. 146): No alcanzas el 70% de créditos requeridos."
        ))
        self.halt()

    # REGLA 2: Sin curso de inducción (Art. 148)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          Alumno(induccion=False),
          salience=50)
    def falta_induccion(self):

        self.declare(Conclusion.create(
            "[!] REQUISITO (Art. 148-I): Falta acreditar el curso de inducción."
        ))
        self.halt()

    # REGLA 3: Lugar no válido (Art. 126)
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          Alumno(lugar_valido=False),
          salience=50)
    def lugar_invalido(self):

        self.declare(Conclusion.create(
            "[!] PROHIBIDO (Art. 126): El lugar elegido no es válido."
        ))
        self.halt()

    # REGLA 4: Todo correcto (Elegibilidad)
    # Se activa si el alumno tiene >= 70% créditos, inducción True y lugar válido True
    @Rule(Goal(kind=GoalKind.CAN_ENROLL),
          Alumno(porcentaje_creditos=P(lambda x: x >= 70),
                 induccion=True,
                 lugar_valido=True))
    def alumno_apto(self):

        text = "\n" + "="*40
        text += "\nESTADO: ALUMNO APTO PARA INICIAR"
        text += "\n" + "="*40
        text += "\n- Debe cumplir 500 horas en mínimo 6 meses."
        text += "\n- Presentar informe cada 100 horas."

        self.declare(Conclusion.create(text))
        self.halt()


    def get_fact(self, fact_type: type):
        for i in self.facts:
            if isinstance(self.facts[i], fact_type):
                return i, self.facts[i]
        return -1, None


#Codigo principal
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

                while True:
                    try:
                        raw_value = input(missing["text"])

                        if missing["fact_value_type"] == int:
                            value = int(raw_value)

                        elif missing["fact_value_type"] == bool:
                            value = utils.string_to_bool(raw_value)

                        elif missing["fact_value_type"] == str:
                            value = raw_value

                        break

                    except:
                        print("Valor inválido, intenta nuevamente...")

                if missing_fact:
                    engine.modify(missing_fact,
                                  **{missing["fact_key"]: value})
                else:
                    new_fact = missing["fact_class"]()
                    new_fact[missing["fact_key"]] = value
                    engine.declare(new_fact)

                engine.retract(i)

            else:
                print("No fue posible llegar a una conclusión.")
                break

        if not utils.string_to_bool(input("\n¿Evaluar otro? (s/n): ")):
            break