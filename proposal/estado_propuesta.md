# Estado de la propuesta

Orquestador: mantén este archivo actualizado tras cada fase/gate.

## Artefactos clave
- Pregunta de investigación: ¿Cómo desarrollar un ecosistema de agentes autónomos basados en IA que fortalezca el aprendizaje profundo —motivación intrínseca, argumentación técnica y resolución de problemas auténticos— en estudiantes de ingeniería, con TRL 6/7 transferible al entorno educativo y al sector productivo colombiano?
- Subproblema 1: Diagnóstico y modelado multidimensional del aprendiz
- Subproblema 2: Arquitectura agéntica autónoma para personalización del aprendizaje
- Subproblema 3: Validación empírica y transferencia tecnológica TRL 6/7
- Objetivo general: Desarrollar un ecosistema de agentes autónomos basados en IA que fortalezca el aprendizaje profundo (motivación intrínseca, argumentación técnica, resolución de problemas auténticos) en estudiantes de ingeniería, mediante diagnóstico multidimensional del aprendiz + arquitectura multiagente con LLMs/MCP + validación empírica en aula, alcanzando TRL 6 (proyectando TRL 7), transferible al entorno educativo y sector productivo colombiano, en 18+2 meses.
- Objetivos específicos: OE1 Caracterizar/modelar (→SP1, F1); OE2 Desarrollar (→SP2, F2); OE3 Validar+desplegar (→SP3, F3-F4)
- Hipótesis: La integración de un modelo computacional multidimensional del aprendiz con una arquitectura multiagente pedagógicamente fundada (LLMs + MCP + scaffolding adaptativo), desplegada en aula real, produce una mejora estadísticamente significativa (p<0.05) en el aprendizaje profundo de estudiantes de ingeniería frente a la instrucción tradicional, alcanzando TRL 6/7 transferible al sector productivo colombiano.
- TRL meta: 6/7

## Clasificación y ruta (Fase 0)

> **Nota (scaffold/plantilla):** plantilla de guía para futuras corridas del
> pipeline; no es una reclasificación retroactiva de los insumos reales de
> esta corrida ya completada.

| Campo | Valor |
|---|---|
| Ruta | _(DRAFT-EXISTS \| NO-DRAFT)_ |
| Archivo TDR | _(nombre de archivo, o "ninguno")_ |
| Archivo draft-base (confirmado por) | _(nombre de archivo — auto \| usuario)_ |
| Confirmaciones de usuario | _(lista de ambigüedades/preguntas resueltas por el usuario, o "ninguna")_ |

## Compuertas tempranas (G0.5, G1a)

> Estas compuertas son distintas de la fila "Confirmaciones de usuario" de
> arriba (esa cubre únicamente el gate de ambigüedad de la Fase 0) y también
> distintas del gate investigador→revisor→usuario de la Fase 1. G0.5 decide
> qué guía aplicar antes de la búsqueda de literatura; G1a cubre el scoping
> temprano (bibliografo-propuesta MODE=scope + graphify + borrador temprano
> del investigador).

### G0.5 — Guía ajustada al TDR

| Campo | Valor |
|---|---|
| Estado | _(N/A sin TDR \| OMITIDA-POR-USUARIO \| PENDIENTE \| EN REVISIÓN \| APROBADA)_ |
| Guía aplicable | _(`guiaProyectosIA_Agente.md` \| `proposal/guia_ajustada_TDR.md`)_ |
| Aprobada por / fecha | _(usuario y fecha, o "N/A" si OMITIDA-POR-USUARIO o sin TDR)_ |

### G1a — Scoping temprano

| Campo | Valor |
|---|---|
| Estado | _(PENDIENTE \| EN REVISIÓN \| APROBADA)_ |
| 5 papers | _(lista `paper-1..5`: título, cuartil, año, DOI/URL — o ruta a `proposal/scoping/papers/`)_ |
| Parámetros de búsqueda | _(query, filtro de cuartil, rango de años, hits por herramienta — `consensus`/`semanticscholar`/`openalex`)_ |
| Grafo | _(ruta `proposal/scoping/graphify-out/` + extracto de `GRAPH_REPORT.md`: God Nodes, Surprising Connections, Suggested Questions)_ |
| 3 subproblemas tempranos | _(cada uno con: gap, `paper-N` de origen, cruce de una línea contra el TDR/guía)_ |

## Prioridad por sección

> Esta tabla se **omite por completo** cuando no hay TDR clasificado/confirmado
> en Fase 0. Plantilla/guía únicamente — no es una clasificación real de esta
> corrida.

| Sección guía | Prioridad (ALTA/NORMAL) | Justificación |
|---|---|---|
| §1 Título | _(ALTA/NORMAL)_ | _(a completar desde la tabla de criterios del TDR)_ |
| §2 Justificación/pertinencia (2.1 problemática, 2.2 pertinencia) | _(ALTA/NORMAL)_ | _(a completar)_ |
| §3 Alcance | _(ALTA/NORMAL)_ | _(a completar)_ |
| §4 Objetivos | _(ALTA/NORMAL)_ | _(a completar)_ |
| §5 Referente teórico | _(ALTA/NORMAL)_ | _(a completar)_ |
| §6 Metodología | _(ALTA/NORMAL)_ | _(a completar)_ |
| §7 Plan de trabajo | _(ALTA/NORMAL)_ | _(a completar)_ |
| §8 Resultados/productos | _(ALTA/NORMAL)_ | _(a completar)_ |
| §9 Referencias | _(ALTA/NORMAL)_ | _(a completar)_ |

## Avance por fase
| Fase | Sección | Agente | Estado | Gate |
|------|---------|--------|--------|------|
| 0 | Insumos | Observador | completo | — |
| 1 | §2.1 | Investigador | completo | Revisor PASS |
| 2 | §2.2, §3 | Redactor | completo | Revisor PASS |
| 3 | §4.1, §4.2 | Investigador | completo | Revisor PASS |
| 4 | §5.1, §5.2, §5.3 | Bibliotecario + Investigador | completo | Revisor PASS |
| 5 | §6, §7 | Redactor + Diseñador | completo | Revisor PASS |
| 6 | §8, §9 | Redactor + Bibliotecario | completo | — |
| 7 | Auditoría + ensamble | Revisor + Orquestador | completo | Usuario |
