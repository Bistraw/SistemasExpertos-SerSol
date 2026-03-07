# Sistema Experto de Servicio Social UAA

Aplicación inteligente para evaluar elegibilidad de estudiantes de la Universidad Autónoma de Aguascalientes para iniciar Servicio Social, basada en el Reglamento General de Titulación (Artículos 117-156).

---

## 🚀 Quick Start

```bash
python gui_serviciosocial.py
```

La aplicación abrirá maximizada en tu pantalla.

---

## 📋 ¿Qué hace?

El sistema valida 6 condiciones obligatorias basadas en el reglamento UAA:

1. **Art. 146** — Mínimo 70% de créditos completados
2. **Art. 148-I** — Curso de inducción acreditado
3. **Art. 126** — Institución pública o asociación civil (NO privada)
4. **Art. 136** — Institución SIN fines de lucro
5. **Art. 147** — Actividad válida (NO reciclaje, boteo, donativos)
6. **Conclusión** — Si TODAS las 5 anteriores se cumplen: APROBADO

---

## 🎯 Cómo usar la GUI

### Paso 1: Llenar el formulario

```
┌─────────────────────────────────────────────┐
│ NOMBRE:              Juan Pérez García      │
├─────────────────────────────────────────────┤
│ CRÉDITOS TOTALES:    400                    │
│ CRÉDITOS COMPLETADOS: 280                   │
│ PORCENTAJE:          70% ✓                  │
├─────────────────────────────────────────────┤
│ SEMESTRE:            6to (selector)         │
├─────────────────────────────────────────────┤
│ ¿INDUCCIÓN?          ✓ SÍ    ✗ NO          │
│ ¿INSTITUCIÓN PÚBLICA? ✓ SÍ   ✗ NO          │
│ ¿ACTIVIDAD VÁLIDA?   ✓ SÍ    ✗ NO          │
└─────────────────────────────────────────────┘
```

### Paso 2: Presiona "Evaluar elegibilidad"

El sistema analizará automáticamente:

- ✅ Calcula porcentaje de créditos
- ✅ Valida cada condición
- ✅ Genera conclusión

### Paso 3: Lee el resultado

**Si es VERDE (✓ APROBADO):**
```
✓ ¡APROBADO! PUEDES INICIAR SERVICIO SOCIAL

Recibirás instrucciones sobre:
  • 500 horas totales
  • 6-24 meses de duración
  • Reportes mensuales
  • Constancia de liberación
```

**Si es ROJO (✗ RECHAZADO):**
```
✗ RECHAZO: CRÉDITOS INSUFICIENTES

Necesitas: 70% completado
Tienes: 62.5%
Acción: Continúa con tus cursos
```

---

## 📊 Tabla de Decisión

| Condición | ≥70% Créditos | Inducción | Institución Válida | Institución Sin Fines Lucro | Actividad Válida | Resultado |
|-----------|:---:|:---:|:---:|:---:|:---:|---|
| Escenario A | ✓ | ✓ | ✓ | ✓ | ✓ | **✓ APROBADO** |
| Escenario B | ✗ | ✓ | ✓ | ✓ | ✓ | **✗ Créditos insuficientes** |
| Escenario C | ✓ | ✗ | ✓ | ✓ | ✓ | **✗ Sin inducción** |
| Escenario D | ✓ | ✓ | ✗ | ✓ | ✓ | **✗ Lugar no válido** |
| Escenario E | ✓ | ✓ | ✓ | ✗ | ✓ | **✗ Institución privada** |
| Escenario F | ✓ | ✓ | ✓ | ✓ | ✗ | **✗ Actividad no válida** |

---

## 🔢 Cálculo de Porcentaje

La GUI calcula automáticamente:

```
Porcentaje = (Créditos Completados / Créditos Totales) × 100
```

**Ejemplos:**

```
280 / 400 × 100 = 70%   ✓ Aprobado
250 / 400 × 100 = 62%   ✗ Rechazado (necesita 70%)
350 / 400 × 100 = 87.5% ✓ Aprobado
```

El indicador cambia de color automáticamente:
- 🟢 **VERDE** si ≥70%
- 🔴 **ROJO** si <70%

---

## 📚 Artículos Implementados

| Art. | Requisito | Estado |
|------|-----------|--------|
| 146  | 70% de créditos | ✅ |
| 148-I | Curso de inducción | ✅ |
| 148-III | 500 horas en 6-24 meses | ✅ Referencia |
| 148-IV | Reportes mensuales ≤100h | ✅ Referencia |
| 126  | No empresas privadas | ✅ |
| 136  | Solo públicas/civiles sin fines lucro | ✅ |
| 147  | No reciclaje/boteo/donativos | ✅ |
| 150  | Constancia de liberación | ✅ Referencia |
| 151  | Baja por incumplimiento | ✅ Referencia |
| 152  | Abandono con aprobación del tutor | ✅ Referencia |
| 153  | Pérdida de horas sin reporte | ✅ Referencia |

---

## ❓ Preguntas Frecuentes

**P: ¿Dónde conseguir información de mis créditos actuales?**
A: Consulta ESIIMA → Alumno → Requisitos de Titulación

**P: ¿Cómo obtengo el curso de inducción?**
A: Comunícate con tu Centro Académico o el tutor de SS de tu carrera

**P: ¿Qué instituciones son válidas?**
A: Solo públicas (gobierno, municipios) o Asociaciones Civiles sin fines de lucro

**P: ¿Puedo hacer SS en una empresa privada?**
A: No, Art. 126 lo prohíbe explícitamente

**P: ¿Qué actividades se rechazan?**
A: Art. 147 prohibe:
- Reciclaje
- Boteo
- Entrega de donativos económicos

---

##  Archivos incluidos

```
📁 sistemasexpertos/
├── gui_serviciosocial.py        ← CORRER ESTO
├── serviciosocialexperta.py      (Motor experto)
├── utils.py                      (Utilidades)
├── README.md                     (Este archivo)
├── EJEMPLOS_USO.md              (9 escenarios detallados)
└── test_escenarios.py           (Pruebas automatizadas)
```

---

## 🛠️ Para Desarrolladores

### Ejecutar pruebas

```bash
python test_escenarios.py
```

Verifica 9 escenarios diferentes (3 aprobados, 6 rechazados)

### Estructura del Motor Experto

```python
from serviciosocialexperta import SistemaServicioSocial, Goal, GoalKind, Alumno

engine = SistemaServicioSocial()
engine.reset()
engine.declare(Goal.create(GoalKind.CAN_ENROLL))
engine.declare(Alumno(
    porcentaje_creditos=70,
    induccion=True,
    lugar_valido=True,
    institucion_publica=True,
    actividad_valida=True
))
engine.run()

# Obtener conclusión
_, conclusion = engine.get_fact(Conclusion)
print(conclusion["text"])
```

---

## 📖 Documentación Completa

Ver **EJEMPLOS_USO.md** para:
- 9 escenarios detallados
- Tabla de decisión interactiva
- Cálculo de porcentaje paso a paso
- Casos especiales (carreras de Salud)
- Preguntas y respuestas extendidas

---

##  Notas Importantes

1. **Este es un SISTEMA EXPERTO**, no reemplaza la evaluación humana del tutor de SS
2. **Aplica a la mayoría de carreras** (excepto carreras de Salud con regulaciones especiales)
3. **Las respuestas son INFORMATIVAS** - para tramites reales, acude a tu Centro Académico
4. **Basado en** Reglamento General de Titulación, aprobado por H. Consejo Universitario el 27/06/2025

---

## 👥 Créditos

**Materia:** Sistemas Expertos Probabilísticos

**Equipo de Desarrollo:**
- Barrón Álvarez María Fernanda
- Benitez Marín Leslie Miroslava
- Guzmán Solís Gael
- Martínez López Humberto
- Merino Garfias Leonardo
- Villalobos Araiza Jorge Luis

---

**Última actualización:** 2026-03-07
