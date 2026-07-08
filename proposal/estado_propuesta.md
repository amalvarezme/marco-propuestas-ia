# Estado de la propuesta

Orquestador: mantén este archivo actualizado tras cada fase/gate.

## Idea inicial del usuario

Agentes de IA para fomentar la motivación, el aprendizaje profundo y la
resolución de problemas en estudiantes de ingeniería.

## Artefactos clave
- Pregunta de investigación: _(pendiente — Fase 1)_
- Subproblema 1: _(pendiente)_
- Subproblema 2: _(pendiente)_
- Subproblema 3: _(pendiente)_
- Objetivo general: _(pendiente — Fase 3)_
- Objetivos específicos: _(pendiente — Fase 3)_
- Hipótesis: _(pendiente — Fase 4)_
- TRL meta: _(pendiente)_

## Clasificación y ruta (Fase 0)

| Campo | Valor |
|---|---|
| Ruta | DRAFT-EXISTS |
| Archivo TDR | `Téminos_Conv_Alianzas_UNAL_2025-2027 (1).pdf` (auto, confianza alta) |
| Archivo draft-base (confirmado por) | `Anexo 2. Propuesta detallada_SemilleroCienciaDatoseIA.docx` (auto, confianza alta) |
| Confirmaciones de usuario (ambigüedad) | Ninguna — ambos archivos dieron match único confiado, sin AMBIGUA |
| TDR especifica sus propias secciones | No |
| Fuente de la lista de secciones | `Secciones_Propuesta.docx` (`doc-secciones`) |
| Evidencia (cita de secciones) | El TDR solo trae la tabla de criterios ponderados (§11.3.1) y requisitos de elegibilidad de la alianza (§8); no enumera la estructura/secciones del documento de propuesta — ver `proposal/insumos.md`, "Secciones obligatorias declaradas por el TDR" |

> **Alerta de coherencia (no es ambigüedad de clasificación, es de alcance):**
> el TDR es la convocatoria **Alianzas Estratégicas Interdisciplinarias SIUN**
> (exige alianza intersedes, ≥1 grupo + ≥1 centro/instituto, $120M, 18 meses).
> El draft-base fue escrito para **Semilleros Sede Manizales 2026** ($17M, 12
> meses, sin exigencia de alianza). El draft-base no cumple tal cual los
> criterios b/c del TDR de Alianzas (articulación SIUN 25 pts + articulación
> externa 5 pts). Pendiente de confirmación del usuario antes de fijar
> alcance en G0.5/G1a.

## Compuertas tempranas (G0.5, G1a)

### G0.5 — Guía ajustada al TDR

| Campo | Valor |
|---|---|
| Estado | APROBADA-RE-VALIDADA (usuario, 2026-07-06 original + re-validación 2026-07-07, incluida la confirmación del usuario sobre las 5 secciones adicionales) |
| Opt-in | SÍ (implícito en la decisión del usuario de seguir el alcance del TDR de Alianzas, 2026-07-06) |
| Guía aplicable propuesta | `proposal/guia_ajustada_TDR.md` |
| Cambios clave | Reescalado transversal: §3 Alcance y §6 Metodología pasan de un solo grupo/sede a alianza intersedes (≥1 grupo + ≥1 centro/instituto), 18+2 meses, $120M; §1/§2/§4/§7 ajustados en consecuencia; §8 exige Anexo 1 (1 tipología A + 1 B + 2 C); §5/§9 sin cambios de fondo. |
| Secciones obligatorias corroboradas | Sí (fuente: `Secciones_Propuesta.docx`, `doc-secciones`) — 13/18 títulos exigidos ya mapean sobre las 9 secciones; **5 títulos (Resumen, Resumen ejecutivo, Palabras clave, Equipo de trabajo, Consideraciones éticas) son ADICIONALES**, confirmadas por el usuario (2026-07-07) para incorporación formal — ver `proposal/guia_ajustada_TDR.md`, "Secciones adicionales exigidas" |
| Estado re-validación | REABIERTA (2026-07-07) → APROBADA-RE-VALIDADA (corroboración vía `doc-secciones`, 2026-07-07; usuario confirmó incorporar las 5 secciones adicionales al documento final) |
| Historial | APROBADA original (usuario, 2026-07-06, sin corroboración de secciones) → REABIERTA y re-validada (2026-07-07) |

### G1a — Scoping temprano

| Campo | Valor |
|---|---|
| Estado | APROBADA (usuario, 2026-07-06) |
| 5 papers | `paper-1`: López-Goyez et al. (2026), MAS de IA generativa (ELA Tutor) en ed. superior, *Applied Sciences* Q2 · `paper-2`: Rida et al. (2025), IMTS multi-agente (JADE) con ganancias en desempeño/motivación, *IEEE Access* Q1 · `paper-3`: Xu et al. (2026), meta-análisis 52 estudios sobre agentes educativos, *Frontiers in Psychology* Q2 · `paper-4`: Fan, Deng & Liu (2025), impacto de IA generativa en estudiantes de ingeniería (China), *Scientific Reports* Q1 · `paper-5`: Bravo & Cruz-Bohorquez (2024), chatbots en educación de ingeniería, *Education Sciences* Q2. Archivos: `proposal/scoping/papers/paper-{1..5}.md`. |
| Parámetros de búsqueda | `consensus` `search` primario (`year_min=2024`, `exclude_preprints=true`, `sjr_max=2`), complementado con `openalex`/`semanticscholar` para DOI/autores. 6 queries sobre agentes de IA + motivación/aprendizaje profundo/resolución de problemas + educación en ingeniería. Sin faltante (5/5 sin relajar filtros). |
| Grafo | `proposal/scoping/graphify-out/` (graph.html/json + GRAPH_REPORT.md, backend `claude-cli`). 14 nodos, 15 edges, 4 comunidades (1 delgada omitida). God Nodes: ELA Tutor (6 edges), Educational Agents concept (4), IMTS (4). Surprising Connections (todas menos una INFERRED, una AMBIGUOUS): ELA Tutor↔Generative AI [AMBIGUOUS], ELA Tutor↔Educational Agents, MAS Architecture↔IMTS, IMTS↔Educational Agents, AI Chatbots↔Educational Agents. Repo-root `graphify-out/graph.json` verificado intacto (mtime sin cambios, Jul 4). |
| 3 subproblemas tempranos | **SP1** Diagnóstico/caracterización de aprendizaje profundo (gap: no hay modelo/instrumento validado que alimente decisión adaptativa; paper-1, paper-3, paper-4; cruza criterio a). **SP2** Diseño de arquitectura multi-agente enfocada en resolución de problemas de ingeniería (gap: MAS existentes no validados cuantitativa/específicamente para esta capacidad; paper-1, paper-2, paper-3; cruza criterio a, novedad). **SP3** Despliegue y validación cuantitativa intersedes en entornos reales (gap: evidencia mono-institucional/pequeña escala, sin transferibilidad TRL 6-7; paper-1, paper-2, paper-3, paper-5; cruza criterio b + exigencia de alianza intersedes). |

## Prioridad por sección

> Regla ALTA = tercil superior por puntaje de criterios ponderados del TDR
> (⌈5/3⌉=2 → criterios **a** [30 pts] y **b** [25 pts] son ALTA-elegibles; no
> hay empate en el límite del tercil, e/d quedan en 20 pts, debajo de b=25).
> **Decisión del usuario (2026-07-06):** se sigue el alcance del TDR de
> Alianzas SIUN (no el draft-base de Semilleros tal cual).

| Sección guía | Prioridad (ALTA/NORMAL) | Justificación |
|---|---|---|
| §1 Título | NORMAL | Ningún criterio ALTA (a, b) lo referencia. |
| §2 Justificación/pertinencia | ALTA | Criterio a (30 pts). |
| §3 Alcance | ALTA | Criterio a (30 pts) y criterio b (25 pts, articulación SIUN — exige alianza intersedes). |
| §4 Objetivos | ALTA | Criterio a (30 pts, "claros, medibles y alcanzables"). |
| §5 Referente teórico | NORMAL | No exigido explícitamente por el TDR. |
| §6 Metodología | ALTA | Criterio a (30 pts) y criterio b (25 pts, trabajo colaborativo intersedes). |
| §7 Plan de trabajo | ALTA | Criterio a (30 pts, vía coherencia con plan/presupuesto). |
| §8 Resultados/productos | NORMAL | Solo referenciado por criterio e (20 pts, no ALTA). |
| §9 Referencias | NORMAL | No exigido por el TDR (mínimo ≥50 es guía interna del equipo). |

## Avance por fase
| Fase | Sección | Agente | Estado | Gate |
|------|---------|--------|--------|------|
| 0 | Insumos | Observador | completo | — |
| 0.5 | Guía ajustada TDR | Investigador | completo | G0.5 PASS |
| 1a | Scoping temprano | Bibliografo + Investigador | completo | G1a PASS |
| 1b | Corpus SOTA | Bibliografo | pendiente | G1b |
| 1 | §2.1 | Investigador | pendiente | Revisor |
| 2 | §2.2, §3 | Redactor | pendiente | Revisor |
| 3 | §4.1, §4.2 | Investigador | pendiente | Revisor |
| 4 | §5.1, §5.2, §5.3 | Bibliografo + Investigador | pendiente | Revisor |
| 5 | §6, §7 | Redactor + Diseñador | pendiente | Revisor |
| 6 | §8, §9 | Redactor + Bibliografo | pendiente | — |
| 7 | Auditoría + ensamble | Revisor + Orquestador | pendiente | Usuario |
