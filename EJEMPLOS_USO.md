# Ejemplos de Uso - Sistema Experto de Servicio Social

## ¿Cómo obtener respuestas deseadas?

El sistema experto analiza **6 condiciones clave** basadas en el reglamento UAA. Dependiendo de cómo completes el formulario, obtendrás diferentes respuestas.

---

## ESCENARIO 1: ✓ APROBADO - Alumno apto para iniciar SS

**Ingresa estos datos en la GUI:**

```
Nombre:                      Juan Pérez García
Créditos totales:            400
Créditos completados:        280  →  (280/400 = 70%)
Semestre:                    6to
¿Completaste inducción?      Sí ✓
¿Institución pública/civil?  Sí ✓
¿Es pública/sin fines lucro? Sí ✓
¿Actividad válida?           Sí ✓
```

**Respuesta esperada:**
```
✓ ¡APROBADO! PUEDES INICIAR SERVICIO SOCIAL

REQUISITOS CUMPLIDOS:
  ✓ Art. 146: 70% de créditos completados
  ✓ Art. 148-I: Curso de inducción acreditado
  ✓ Art. 126: Institución pública/civil válida
  ✓ Art. 147: Actividad de beneficio social

OBLIGACIONES DURANTE EL SERVICIO (Art. 148):
  1. Cumplir 500 horas (Art. 148-III)
  2. Duración: mínimo 6 meses, máximo 2 años
  3. Reportes mensuales cada 100h (Art. 148-IV)
  4. Informe final dentro de 1 mes tras terminar
  5. No reportar informes fuera de plazo (Art. 153)
```

---

## ESCENARIO 2: ✗ RECHAZO - Créditos insuficientes

**Ingresa estos datos:**

```
Nombre:                      María López
Créditos totales:            400
Créditos completados:        250  →  (250/400 = 62.5%)  ← MENOS DE 70%
Semestre:                    5to
¿Completaste inducción?      Sí ✓
¿Institución pública/civil?  Sí ✓
¿Es pública/sin fines lucro? Sí ✓
¿Actividad válida?           Sí ✓
```

**Respuesta esperada:**
```
✗ RECHAZO: CRÉDITOS INSUFICIENTES

(Art. 146) Debes completar mínimo 70% de los créditos
de tu plan de estudios antes de iniciar SS.

Acción: Continúa con tus cursos y vuelve después.
```

**¿Por qué se rechaza?** El porcentaje es 62.5%, menor a 70% requerido por Art. 146.

---

## ESCENARIO 3: ✗ REQUISITO NO CUMPLIDO - Sin curso de inducción

**Ingresa estos datos:**

```
Nombre:                      Carlos Mendez
Créditos totales:            400
Créditos completados:        300  →  (300/400 = 75%)  ✓
Semestre:                    7mo
¿Completaste inducción?      No ✗  ← FALTA ESTO
¿Institución pública/civil?  Sí ✓
¿Es pública/sin fines lucro? Sí ✓
¿Actividad válida?           Sí ✓
```

**Respuesta esperada:**
```
✗ REQUISITO NO CUMPLIDO: CURSO DE INDUCCIÓN

(Art. 148-I) Debes acreditar el curso de inducción
antes de iniciar tu servicio social.

Acción: Inscríbete en el próximo curso de inducción.
```

**¿Por qué se rechaza?** Aunque tiene 75% de créditos, no completó el curso obligatorio de inducción.

---

## ESCENARIO 4: ✗ PROHIBIDO - Institución privada

**Ingresa estos datos:**

```
Nombre:                      Ana García
Créditos totales:            400
Créditos completados:        290  →  (290/400 = 72.5%)  ✓
Semestre:                    6to
¿Completaste inducción?      Sí ✓
¿Institución pública/civil?  Sí ✓
¿Es pública/sin fines lucro? No ✗  ← INSTITUCIÓN PRIVADA
¿Actividad válida?           Sí ✓
```

**Respuesta esperada:**
```
✗ PROHIBIDO: INSTITUCIÓN PRIVADA

(Art. 136) Solo instituciones públicas o asociaciones
civiles sin fines de lucro pueden recibir prestadores.

Acción: Selecciona una institución pública o civil.
```

**¿Por qué se rechaza?** Por Art. 126 y 136: NO se permite SS en empresas privadas.

---

## ESCENARIO 5: ✗ PROHIBIDO - Actividad no válida (reciclaje, boteo, donativos)

**Ingresa estos datos:**

```
Nombre:                      Roberto Silva
Créditos totales:            400
Créditos completados:        285  →  (285/400 = 71.25%)  ✓
Semestre:                    6to
¿Completaste inducción?      Sí ✓
¿Institución pública/civil?  Sí ✓
¿Es pública/sin fines lucro? Sí ✓
¿Actividad válida?           No ✗  ← RECICLAJE/BOTEO/DONATIVOS
```

**Respuesta esperada:**
```
✗ PROHIBIDO: ACTIVIDAD NO VÁLIDA

(Art. 147) NO se aceptan para SS:
  • Reciclaje
  • Boteo
  • Entrega de donativos económicos

Acción: Propón una actividad que beneficie a
grupos menos favorecidos (Art. 120).
```

**¿Por qué se rechaza?** Por Art. 147: Estas actividades no generan impacto social real.

---

## ESCENARIO 6: ✗ MÚLTIPLES PROBLEMAS

**Ingresa estos datos:**

```
Nombre:                      Pedro Ruiz
Créditos totales:            400
Créditos completados:        200  →  (200/400 = 50%)  ✗
Semestre:                    4to
¿Completaste inducción?      No ✗
¿Institución pública/civil?  Sí
¿Es pública/sin fines lucro? No ✗
¿Actividad válida?           No ✗
```

**Respuesta esperada:**
```
✗ RECHAZO: CRÉDITOS INSUFICIENTES
```

**¿Por qué?** El sistema detiene en el PRIMER error encontrado (salience=100). 
En este caso: créditos insuficientes (50% < 70%).

---

## TABLA DE DECISIÓN RÁPIDA

| Condición | Sí (✓) | No (✗) | Resultado |
|-----------|--------|--------|-----------|
| 70%+ créditos (Art. 146) | ✓ | ✗ | RECHAZA |
| Curso inducción (Art. 148-I) | ✓ | ✗ | RECHAZA |
| Institución válida (Art. 126) | ✓ | ✗ | RECHAZA |
| Institución sin fines lucro (Art. 136) | ✓ | ✗ | RECHAZA |
| Actividad válida (Art. 147) | ✓ | ✗ | RECHAZA |
| TODAS las anteriores | ✓ | - | **APRUEBA** |

---

## CÁLCULO DE PORCENTAJE

El sistema calcula automáticamente el porcentaje:

```
Porcentaje = (Créditos Completados / Créditos Totales) × 100

Ejemplos:
  280 / 400 × 100 = 70%     ✓ Aprobado
  250 / 400 × 100 = 62.5%   ✗ Rechazado
  350 / 400 × 100 = 87.5%   ✓ Aprobado
```

**En la GUI:** 
- Ingresa "400" en "Total de créditos"
- Ingresa "280" en "Créditos completados"
- El sistema calcula automáticamente **70%**
- El color del indicador cambia a VERDE si es ≥70%, ROJO si es <70%

---

## CASOS ESPECIALES (según Art. 146)

El artículo dice:
> "El servicio social podrá iniciarse en el semestre de cumplimiento del 70% de los créditos académicos de su Plan de Estudios, **exceptuando para las carreras que se rigen por el Sector Salud**. Los casos particulares serán resueltos por el Centro Académico correspondiente y la Dirección General de Servicios Educativos."

**Para carreras de Salud:** Consulta con tu Centro Académico para excepciones.

---

## PASOS PARA OBTENER LA RESPUESTA DESEADA

### Si quieres: ✓ APROBACIÓN

1. ✓ Asegúrate de tener ≥70% de créditos
2. ✓ Completa el curso de inducción
3. ✓ Selecciona una institución pública o civil
4. ✓ Verifica que sea una institución sin fines de lucro
5. ✓ Propón una actividad que beneficie a grupos vulnerables
6. ✓ Presiona "Evaluar elegibilidad"

**Resultado:** Mensaje verde con APROBACIÓN

### Si quieres: ✗ IDENTIFICAR EL PROBLEMA

1. Completa el formulario normalmente
2. Presiona "Evaluar elegibilidad"
3. Lee el mensaje de error (indicará cuál condición no cumple)
4. Corrije esa condición específica
5. Vuelve a evaluar

---

## ARTÍCULOS CLAVE IMPLEMENTADOS

| Artículo | Requisito | Implementado |
|----------|-----------|--------------|
| 146 | Mínimo 70% de créditos | ✓ |
| 148-I | Curso de inducción obligatorio | ✓ |
| 126 | No empresas privadas | ✓ |
| 136 | Solo públicas/civiles sin fines lucro | ✓ |
| 147 | No reciclaje/boteo/donativos | ✓ |
| 148-III | 500 horas en 6-24 meses | ✓ Referencia |
| 148-IV | Reportes mensuales ≤100h | ✓ Referencia |
| 150 | Constancia de liberación | ✓ Referencia |
| 151 | Baja por incumplimiento | ✓ Referencia |
| 153 | Pérdida de horas sin reporte | ✓ Referencia |

---

## PREGUNTAS FRECUENTES

**P: ¿Qué pasa si cambio el semestre a 5to?**
A: Aún así se evalúa contra los 6 criterios. El semestre es informativo actualmente.

**P: ¿Puedo iniciar SS antes de 70% de créditos?**
A: No, Art. 146 lo prohíbe (excepto carreras de Salud con aprobación especial).

**P: ¿Qué pasa después de aprobar?**
A: Recibirás instrucciones sobre las obligaciones de 500 horas, 6 meses mínimo, reportes mensuales, etc.

**P: ¿Dónde consulto mis horas acumuladas?**
A: Art. 146 menciona ESIIMA (Sistema de Información de la UAA) → Alumno → Requisitos de Titulación.

---

## PRÓXIMAS FASES (NO IMPLEMENTADAS AÚN)

- **Fase 2:** Registro y validación de horas de servicio (500h, 6-24 meses)
- **Fase 3:** Validación de reportes mensuales (≤100h cada uno)
- **Fase 4:** Constancia de liberación
- **Fase 5:** Historial de estudiantes

