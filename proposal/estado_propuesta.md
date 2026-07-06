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

> **Prueba parcial real (2026-07-05):** ejecución real de `insumos-observador`
> sobre los 2 archivos de `info_data/`, seguida del cómputo de prioridad
> (rol de dispatcher) y el pre-step de `bibliografo-propuesta` (MODE=explore).
> No es una corrida completa del pipeline (no se despachó `investigador` ni
> el gate `revisor`); ver nota de hallazgos al final de esta sección.

| Campo | Valor |
|---|---|
| Ruta | DRAFT-EXISTS |
| Archivo TDR | `Téminos_Conv_Alianzas_UNAL_2025-2027 (1).pdf` (auto, confianza alta) |
| Archivo draft-base (confirmado por) | `Anexo 2. Propuesta detallada_SemilleroCienciaDatoseIA.docx` (auto, confianza alta) |
| Confirmaciones de usuario | Ninguna — ambos archivos produjeron exactamente una coincidencia confiada, sin AMBIGUA |

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
| Estado | APROBADA |
| Guía aplicable | `proposal/guia_ajustada_TDR.md` |
| Aprobada por / fecha | usuario, 2026-07-05 |

### G1a — Scoping temprano

| Campo | Valor |
|---|---|
| Estado | APROBADA (usuario, 2026-07-05) |
| 5 papers | `paper-1`: Adaptive intelligent tutoring systems for STEM education... (2025, Smart Learning Environments, Q1) · `paper-2`: Multi-Agent System for Students Cognitive Assessment in E-Learning Environment (2024, IEEE Access, Q1) · `paper-3`: Advancing Problem-Based Learning in Biomedical Engineering in the Era of Generative AI (2025, IEEE Trans. on Education, Q1) · `paper-4`: Integrating Generative AI into Programming Education... (2025, Int. J. of AI in Education, Q1) · `paper-5`: Impact of educational agents on student's learning outcomes: a meta-analysis (2026, Frontiers in Psychology, Q2). Archivos: `proposal/scoping/papers/paper-{1..5}.md`. |
| Parámetros de búsqueda | `consensus` `search` como filtro primario (`sjr_max=2`, `year_min=2024`, `exclude_preprints=true`), complementado con `semanticscholar` para metadatos/DOI. Queries: tutoría personalizada + agentes IA + educación en ingeniería + aprendizaje profundo/motivación/argumentación/resolución de problemas. |
| Grafo | `proposal/scoping/graphify-out/` (graph.html/json + GRAPH_REPORT.md). 34 nodos, 57 edges, 5 comunidades (una por paper). God Nodes: "Educational Agents" e ITS (7 y 6 edges). Surprising Connections (todas INFERRED): Educational Agents↔ITS, Personalized Feedback↔Cognitive Assessment, Adaptive Trajectory↔Multi-Agent System. Nodos aislados: "STEM Education", "E-Learning Environment". Repo-root `graphify-out/graph.json` verificado intacto (mismo md5/mtime). |
| 3 subproblemas tempranos | **SP1** Caracterización unificada del estado cognitivo-motivacional del estudiante (gap: cognición/trayectoria/motivación evaluadas en silos monomodales; paper-1, paper-2, paper-5; cruza OE1/criterio a). **SP2** Ausencia de un ecosistema multiagente autónomo coordinado (gap: 5 comunidades disjuntas, integración solo INFERRED, nunca construida; paper-1 a paper-4; cruza OE2/criterio a-innovación). **SP3** Falta de validación empírica TRL 6/7 del aprendizaje profundo en ingeniería (gap: meta-análisis muestra efecto no significativo en resolución de problemas/engagement; paper-5, paper-1, paper-3, paper-4; cruza OE3/TRL 6-7/criterios a,d,e). |

### G1b — Corpus y subsecciones SOTA

| Campo | Valor |
|---|---|
| Estado | _(N/A sin G1a=APROBADA \| PENDIENTE \| EN REVISIÓN \| APROBADA)_ |
| Corpus (30-40 papers) | _(conteo final + ruta a `proposal/scoping/papers/paper-{1..N}.md`; `paper-6..N` deduplicados contra el corpus semilla de G1a, `paper-1..5` byte-inalterados)_ |
| Parámetros de búsqueda | _(query, filtro de cuartil, rango de años, hits por herramienta — `consensus`/`semanticscholar`/`openalex`, sub-paso corpus de MODE=sota)_ |
| Grafo actualizado | _(ruta `proposal/scoping/graphify-out/` tras `graphify --update` + extracto de `GRAPH_REPORT.md` sobre el corpus ampliado; `proposal/scoping/graphify-out-g1a-snapshot/` = copia fija del grafo de G1a, nunca reconstruida)_ |
| Tabla de subsecciones SOTA | _(3-5 subsecciones: paper → subsección → SP1/SP2/SP3, un paper por fila, ninguno repetido ni faltante)_ |

> **G1a permanece intacta:** esta sub-tabla se agrega inmediatamente después
> de "G1a — Scoping temprano" sin modificar ninguna de sus filas ni el
> encabezado de la sección "Compuertas tempranas (G0.5, G1a)". Una
> iteración de G1b que cambia solo el CORPUS siempre re-deriva también la
> tabla de subsecciones SOTA (sub-paso grouping de MODE=sota) — eso es el
> comportamiento esperado, no scope creep. Ver `propuesta.md`, "Fase 1b",
> "Reglas de iteración por componente".

## Prioridad por sección

> Calculada por el dispatcher a partir de la tabla de criterios ponderados
> extraída por `insumos-observador` (ver `proposal/insumos.md` §"Extracción
> del TDR"), regla ALTA = tercil superior por puntaje (⌈5/3⌉=2 → criterios
> **a** [30 pts] y **b** [25 pts] son ALTA-elegibles), usando el mapeo
> Sección(es) afectada(s) que `insumos-observador` extrajo directamente del
> TDR real (más específico que el crosswalk genérico de 4 temas fijado en
> `propuesta.md`; ver hallazgo al final).

| Sección guía | Prioridad (ALTA/NORMAL) | Justificación |
|---|---|---|
| §1 Título | NORMAL | Ningún criterio ALTA (a, b) lo referencia; el TDR no exige título de propuesta. |
| §2 Justificación/pertinencia (2.1 problemática, 2.2 pertinencia) | ALTA | Criterio a (30 pts, calidad del proyecto — coherencia con justificación) y criterio b (25 pts, articulación SIUN, vía §2.2). |
| §3 Alcance | ALTA | Criterio a (30 pts) y criterio b (25 pts). |
| §4 Objetivos | ALTA | Criterio a (30 pts, exige objetivos "claros, medibles y alcanzables"). |
| §5 Referente teórico | NORMAL | Ningún criterio ALTA lo referencia explícitamente (el TDR no lo exige como sección propia). |
| §6 Metodología | ALTA | Criterio a (30 pts). |
| §7 Plan de trabajo | ALTA | Criterio a (30 pts); también referenciado por d (20 pts, NORMAL). |
| §8 Resultados/productos | ALTA | Criterio a (30 pts); también referenciado por d (20 pts, NORMAL). |
| §9 Referencias | NORMAL | El TDR no exige referencias; ese mínimo (≥50, IEEE/APA) proviene de la guía interna del equipo, no del TDR. |

> **Hallazgo de la prueba:** el crosswalk genérico de 4 temas fijado en
> `.claude/commands/propuesta.md` (`calidad/innovación→§4/§5/§6,
> formación→§8, impacto territorial/ODS→§2.2/§3, articulación→§2.2/§8`)
> habría marcado ALTA un conjunto distinto (§2, §4, §5, §6, §8 — incluye §5,
> excluye §3 y §7) frente al mapeo real extraído del TDR (§2, §3, §4, §6,
> §7, §8 — sin §5). Se usó el mapeo específico del TDR real por ser más
> preciso; el crosswalk fijo del dispatcher queda como una divergencia a
> resolver (no bloqueante, ver reporte al usuario).

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
