# Insumos — Digest de Fase 0

**Corrida:** nueva y desde cero (reemplaza cualquier propuesta previa).
**Idea original del usuario:**
> Agentes de IA para fomentar la motivación, el aprendizaje profundo y la resolución de problemas en estudiantes de ingeniería.

---

## 1. Clasificación de insumos

| Archivo | Tipo | Confianza | Señales | Confirmado por |
|---|---|---|---|---|
| `Téminos_Conv_Alianzas_UNAL_2025-2027 (1).pdf` | TDR | alta | Título "Convocatoria nacional…"; usa explícitamente "términos de referencia" (§18); tabla de criterios de evaluación ponderados (§11.3.1, 100 pts); cronograma con fechas de apertura/cierre (§15: 15-abr-2026 a 30-nov-2027); requisitos mínimos de elegibilidad (§8) e incompatibilidades (§10). Único match confiado para TDR; cero señales de draft-base (no es una propuesta de proyecto específica, es el llamado). | auto |
| `Anexo 2. Propuesta detallada_SemilleroCienciaDatoseIA.docx` | draft-base | alta | Documento "Anexo 2. Documento técnico de la propuesta"; estructura completa tipo §1-§9 de la guía ya desarrollada (justificación 2.1/2.2, alcance, objetivos general/específicos, referente teórico, estado del arte, metodología en 4 fases, cronograma, presupuesto, resultados/productos, ~47 referencias bibliográficas, anexos/avales); objetivos planteados como artefacto terminado, no como requisito a cumplir. Único match confiado para draft-base; cero señales de TDR (no contiene tabla de criterios de evaluación propia ni reglas de elegibilidad para evaluadores — es una propuesta que responde a otra convocatoria). | auto |
| `Secciones_Propuesta.docx` | doc-secciones | alta | Extraído vía `textutil -convert txt -stdout`. Contenido: 18 títulos numerados/encabezados sueltos (Título, Resumen, Resumen ejecutivo, Descripción del problema, Objetivo general, Objetivos específicos, Resultados esperados, Palabras clave, Equipo de trabajo, Justificación, Metodología, Consideraciones éticas, Articulación SIUN, Articulación con actores externos, Aportes a necesidades territoriales/nacionales/globales, Estrategia de formación en investigación, Estrategia de divulgación científica, Bibliografía) sin prosa desarrollada — es un esquema/lista de secciones obligatorias, no una propuesta redactada ni una tabla de criterios. No compite en el cómputo AMBIGUA (no-competidor, mismo estatus que background). | auto |

**Resultado de ambigüedad:** ninguno de los dos archivos requiere confirmación del usuario — cada uno produjo exactamente un match confiado (no 0, no >1) para su etiqueta. No hay AMBIGUA que reportar.

### Alerta de coherencia (no es ambigüedad de clasificación, pero debe surgirse al usuario)

El TDR y el draft-base **no pertenecen a la misma convocatoria**:

- El **TDR** es la *"Convocatoria nacional para el fortalecimiento de alianzas estratégicas interdisciplinarias entre los actores del SIUN (2025-2027)"* — exige una **alianza intersedes** (mínimo un grupo de investigación + un Centro/Instituto de Investigación de distintas sedes), presupuesto de $120.000.000 por proyecto, duración de hasta 18 meses, apertura 15-abr-2026.
- El **draft-base** fue escrito para la *"Convocatoria para el apoyo y fortalecimiento de semilleros de investigación — Sede Manizales 2026"* — un llamado de sede (no nacional/intersedes), presupuesto de $17.000.000, duración de 12 meses, sin exigencia de alianza interinstitucional.

Esto significa que el draft-base es **muy reutilizable en contenido** (problemática, marco teórico, estado del arte, metodología, referencias — casi calcado a la idea del usuario) pero **no cumple el alcance/escala exigidos por el TDR actual** (falta la alianza intersedes con múltiples actores SIUN, el presupuesto es de otro orden de magnitud, y faltan criterios como "articulación entre actores del SIUN" y "articulación con actores externos"). El Investigador y el Redactor deben decidir si: (a) se reescala el draft-base a la lógica de alianza exigida por el TDR, o (b) se usa el draft-base como base conceptual pero se reformula alcance/metodología/presupuesto/equipo para cumplir los criterios b y c del TDR (25 + 5 = 30 de 100 puntos). Recomiendo que el Orquestador confirme con el usuario cuál convocatoria efectivamente se está respondiendo antes de fijar alcance en Fase 0.5/1a.

---

## 2. Extracción del TDR — `Téminos_Conv_Alianzas_UNAL_2025-2027 (1).pdf`

### Secciones obligatorias declaradas por el TDR
- Declara secciones propias: No
- Fuente: `Secciones_Propuesta.docx` (doc-secciones)
- Evidencia: no se encontró en el TDR ningún pasaje que enumere la
  estructura/secciones que debe contener el documento de la propuesta. El
  TDR solo trae (a) la tabla de criterios de evaluación ponderados (§11.3.1,
  100 pts — responde "cómo puntúan los evaluadores", no "qué debe contener
  el documento") y (b) requisitos mínimos de elegibilidad de la alianza
  (§8: composición, vinculación estudiantil, etc.). El "Mapeo a las 9
  secciones de la guía" de abajo es una derivación del agente sobre esos dos
  insumos, no una lista de secciones enunciada por el TDR mismo — por lo
  tanto no cuenta como "sí" bajo la señal distintiva de
  `insumos-observador.md`.
- Lista de secciones exigidas (fuente: `Secciones_Propuesta.docx`, dado que
  el TDR no declara las suyas):
  1. Título — [→ §1 de la guía]
  2. Resumen — [ADICIONAL, no cubierto por las 9 secciones de la guía]
  3. Resumen ejecutivo — [ADICIONAL, no cubierto por las 9 secciones de la guía]
  4. Descripción del problema — [→ §2.1 de la guía]
  5. Objetivo general — [→ §4.1 de la guía]
  6. Objetivos específicos — [→ §4.2 de la guía]
  7. Resultados esperados — [→ §8 de la guía]
  8. Palabras clave — [ADICIONAL, no cubierto por las 9 secciones de la guía]
  9. Equipo de trabajo — [ADICIONAL, no cubierto por las 9 secciones de la guía; roles se mencionan tangencialmente en §7]
  10. Justificación — [→ §2.2 de la guía]
  11. Metodología — [→ §6 de la guía]
  12. Consideraciones éticas — [ADICIONAL, no cubierto por las 9 secciones de la guía]
  13. Articulación entre actores del SIUN de la alianza — [→ §3 de la guía; ya cubierto por el `[AJUSTE TDR]` de criterio b]
  14. Articulación con actores externos de la alianza — [→ §3 de la guía; ya cubierto por el `[AJUSTE TDR]` de criterio c]
  15. Aportes a necesidades territoriales/nacionales/globales — [→ §2/§8 de la guía; ya cubierto por el `[AJUSTE TDR]` de criterio e]
  16. Estrategia de formación en investigación de estudiantes/semilleros — [→ §6/§7 de la guía; ya cubierto por el `[AJUSTE TDR]` de criterio d]
  17. Estrategia de divulgación científica — [→ §8 de la guía; ya cubierto por Anexo 1 tipología C]
  18. Bibliografía — [→ §9 de la guía]

> **Nota de corroboración (hallazgo real, no asumido):** 13/18 títulos
> mapean sobre las 9 secciones existentes de la guía (varios ya estaban
> cubiertos por los ajustes TDR de §3/§6/§8 en `guia_ajustada_TDR.md`). Los
> otros **5 títulos (Resumen, Resumen ejecutivo, Palabras clave, Equipo de
> trabajo, Consideraciones éticas) son secciones adicionales exigidas por
> este documento que NO están cubiertas por la estructura fija de 9
> secciones** de `guiaProyectosIA_Agente.md`/`guia_ajustada_TDR.md`. Esto es
> un hallazgo de esta corroboración, no un supuesto: requiere decisión
> explícita del usuario sobre si se añaden como partes adicionales del
> documento final (ver G0.5 en `estado_propuesta.md`).

### Metadatos de la convocatoria
- **Nombre:** Convocatoria nacional para el fortalecimiento de alianzas estratégicas interdisciplinarias entre los actores del Sistema de Investigación de la Universidad Nacional de Colombia - SIUN (2025–2027).
- **Dependencia responsable:** Dirección Nacional de Investigación y Laboratorios – Vicerrectoría de Investigación.
- **Modalidad:** Única.
- **Presupuesto por proyecto:** $120.000.000 (70% nivel nacional / 30% contrapartida de facultad, o 100% nacional si no hay facultades participantes).
- **Presupuesto total disponible:** $3.960.000.000, distribuido por sede (Medellín $960M, Manizales $600M, Palmira $600M, De La Paz $480M, Amazonia $360M, Orinoquia $360M, Caribe $360M, Tumaco $240M).
- **Duración:** hasta 18 meses de ejecución técnica-financiera + 2 meses adicionales para productos/informe final; prórroga máx. 6 meses.
- **Cronograma:** apertura 15-abr-2026; convocatoria permanente hasta agotar recursos; cierre no posterior al 30-nov-2027.
- **Umbral de aprobación:** puntaje ≥ 80/100.
- **Elegibilidad del líder:** docente de planta UNAL de las sedes listadas en §6.1 (no Bogotá, no docentes especiales, no Sede Bogotá como líder aunque sí como coinvestigador).
- **Requisitos mínimos de la alianza:** mínimo un grupo de investigación + un Centro/Instituto; evidenciar trabajo intersedes; grupos en estado activo con información actualizada en Hermes; vincular al menos un estudiante de pregrado o posgrado; estrategia de divulgación científica; roles/responsabilidades definidos; semillero opcional (puede crearse); aliado externo opcional.

### Mapeo a las 9 secciones de la guía

| Sección guía | Contenido exigido por el TDR |
|---|---|
| §1 Título | No define título de proyecto; sí el nombre de la convocatoria (marco de referencia obligatorio a citar). |
| §2 Justificación/pertinencia (2.1 problemática, 2.2 pertinencia) | Debe alinearse con Plan Global de Desarrollo 2025-2027 (Eje 4, "Líneas integradas de trabajo académico"); debe evidenciar aporte a necesidades territoriales/nacionales/globales (criterio e, 20 pts) y coherencia problema-justificación (criterio a, 10 pts). |
| §3 Alcance | Debe evidenciar: alianza con ≥1 grupo + ≥1 centro/instituto, trabajo intersedes, vinculación de estudiante(s), semillero (opcional), aliado externo (opcional); relevancia/pertinencia/alcance (criterio a, 10 pts). |
| §4 Objetivos | Objetivo general y específicos "claros, medibles y alcanzables" (criterio a, 10 pts). |
| §5 Referente teórico | No exigido explícitamente por el TDR como sección aparte, pero sustenta la "coherencia" evaluada en criterio a. |
| §6 Metodología | Debe mostrar coherencia con problema/justificación/presupuesto/resultados (criterio a, 10 pts); trabajo colaborativo intersedes con intercambio de conocimiento entre disciplinas (criterio b, 25 pts); trabajo interinstitucional con actores externos (criterio c, 5 pts); estrategia de formación en investigación de estudiantes/semilleros (criterio d, 20 pts). |
| §7 Plan de trabajo | Roles/responsabilidades/actividades de cada actor de la alianza; duración ≤18 meses; informes semestrales; ejecución de ≥50% del presupuesto a mitad de proyecto. |
| §8 Resultados/productos | Mínimo 1 producto tipología A (nuevo conocimiento), 1 tipología B (formación), 2 tipología C (divulgación científica + apropiación social), según Anexo 1 de productos académicos del TDR. |
| §9 Referencias | No exigido explícitamente por el TDR. |

### Tabla de criterios ponderados

| Criterio | Pts | Sección(es) afectada(s) |
|---|---|---|
| a. Calidad del proyecto (coherencia problema-justificación-metodología-plan-presupuesto-resultados 10; claridad objetivo general/específicos 10; relevancia/pertinencia/alcance 10) | 30 | §2, §3, §4, §6, §7 |
| b. Articulación entre actores del SIUN (investigadores, grupos, centros, institutos) | 25 | §3, §6 |
| c. Articulación con actores externos | 5 | §3, §6 |
| d. Estrategia de fortalecimiento de formación en investigación de estudiantes/semilleros | 20 | §6, §7 |
| e. Aportes a necesidades territoriales, nacionales o globales | 20 | §2, §8 |
| **Total** | **100** | — |

---

## 3. Extracción del draft-base — `Anexo 2. Propuesta detallada_SemilleroCienciaDatoseIA.docx`

**Convocatoria original que responde:** "Convocatoria para el apoyo y fortalecimiento de semilleros de investigación de la Universidad Nacional de Colombia Sede Manizales - 2026" (dirigida a la Dirección de Investigación y Extensión, Sede Manizales) — **distinta** de la TDR clasificada en este Fase 0.

**Datos generales del proyecto previo:**
- Título: "Apropiación de ecosistemas de agentes inteligentes autónomos para el desarrollo de software con inteligencia artificial".
- Semillero: Semillero de ciencia de datos e inteligencia artificial.
- Grupo asociado: Grupo de control y procesamiento digital de señales (Categoría A1 Minciencias).
- Investigador principal: Andrés Marino Álvarez Meza (Facultad de Ingeniería y Arquitectura, UNAL Manizales).
- Presupuesto: $17.000.000 (equipos, servicios/suscripciones IA, estudiantes auxiliares, divulgación).
- Duración: 12 meses.

### Contenido por sección (guía §1-§9)

- **§1 Título:** "Apropiación de ecosistemas de agentes inteligentes autónomos para el desarrollo de software con inteligencia artificial".
- **§2.1 Problemática:** brecha estructural entre la formación en ingeniería y las exigencias cognitivas del modelado/optimización de procesos bajo incertidumbre; adopción instrumental de la IA en la universidad (automatización sin transformar el aprendizaje profundo); tres limitantes: (1) ausencia de diagnósticos sistemáticos del aprendizaje profundo, (2) ausencia de herramientas tecnológicas validadas para personalizar trayectorias de aprendizaje, (3) ausencia de validación empírica en condiciones reales de aula.
  - **Pregunta de investigación original:** "¿Cómo fortalecer el aprendizaje profundo de estrategias de desarrollo de software en los miembros del Semillero de Investigación en Ciencia de Datos e IA, mediante la apropiación de ecosistemas basados en agentes inteligentes autónomos?"
- **§2.2 Pertinencia:** enmarcada en Plan Global de Desarrollo 2025-2027 (Eje 4); CONPES 4075 de 2022; Política de Investigación e Innovación Orientada por Misiones (PIIOM 2024-2033); necesidad de caracterización basal (motivación, argumentación, resolución de problemas) antes de intervenir.
- **§3 Alcance:** diseño, desarrollo colaborativo y evaluación piloto de un prototipo de software (ecosistema de agentes) — no plataforma comercial; delimitado a estudiantes de pregrado/posgrado del semillero (Manizales); 12 meses; evaluación restringida a 3 dimensiones (motivación, argumentación, resolución de problemas); entregables: 1 póster + 1 artículo científico indexado.
- **Objetivos:**
  - **General:** "Fortalecer el aprendizaje profundo de estrategias de desarrollo de software en los miembros del Semillero de Investigación en Ciencia de Datos e IA de la UNAL sede Manizales, mediante la apropiación, diseño y evaluación de un ecosistema de agentes inteligentes autónomos."
  - **Específicos (3):**
    1. Diseñar un ecosistema de agentes inteligentes autónomos (ML, redes neuronales profundas, PLN) orientado a resolución de problemas en desarrollo de software.
    2. Desarrollar colaborativamente la herramienta de software (retroalimentación adaptativa, modelado del usuario, ciclos iterativos).
    3. Evaluar la incidencia del ecosistema en el aprendizaje profundo (motivación, argumentación, resolución de problemas) mediante pruebas piloto.
- **§5 Referente teórico:** aprendizaje profundo (Marton & Säljö 1976; Biggs 1999); construccionismo computacional (Papert & Harel 1991); andamiaje cognitivo / ZDP (Vygotsky 1978; Wood, Bruner & Ross 1976); socio-constructivismo / comunidades de práctica (Lave & Wenger 1991); enfoque sociotécnico y co-agencia humano-máquina (Selwyn 2019; Anastasiades et al. 2025). Estado del arte: evolución de la IA educativa hacia IA agéntica (Ouyang & Jiao 2021; Park et al. 2023; Wang et al. 2024); ecosistemas de agentes en desarrollo de software (Claude Code, Gemini Spark, Hermes/NousResearch, OpenClaw); desafíos pedagógicos en Latinoamérica (Salas-Pilco & Yang 2022; UNESCO 2023; Chan & Hu 2024); paradigmas de codificación (vibe coding vs. Spec-Driven Development — White et al. 2023).
- **§6 Metodología:** investigación aplicada con desarrollo tecnológico; constructivismo computacional ("aprender haciendo"); metodología ágil híbrida (Scrum + AI-Assisted Software Engineering); 4 fases: (1) fundamentación tecnológica y diseño (near-peer mentoring, MCP/CLI, diseño arquitectónico), (2) desarrollo colaborativo y despliegue (pruebas en hardware local/nube, integración de herramientas agénticas), (3) pruebas piloto y evaluación (Spec-Driven Development vía GitHub Spec-Kit, prueba piloto de app móvil, medición de impacto), (4) divulgación y transferencia (charlas, póster, artículo).
- **§7 Plan de trabajo:** cronograma de 12 meses (tabla de actividades × responsables × mes); roles definidos por estudiante/docente/egresado.
- **§8 Resultados/productos:** 1 póster divulgativo, 1 artículo científico sometido/publicado en revista indexada, 1 informe técnico-académico.
- **§9 Referencias:** ~47 referencias bibliográficas (APA), ver lista de notables abajo.

### Referencias notables encontradas (para Bibliografo-Propuesta)

- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). *Generative agents: Interactive simulacra of human behavior*. UIST '23. ACM. https://doi.org/10.1145/3586183.3606763
- Wang, L., Ma, C., Feng, X., Zhang, Z., & Zhao, H. (2024). *A Survey on Large Language Model based Autonomous Agents*. Frontiers of Computer Science, 18(1). https://doi.org/10.1007/s11704-024-30231-1
- Xi, Z., et al. (2023). *The rise and potential of large language model based agents: A survey*. arXiv:2309.07864.
- Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). *Systematic review of research on artificial intelligence applications in higher education*. IJETHE, 16(39). https://doi.org/10.1186/s41239-019-0171-0
- Hooshyar, D., et al. (2024). *The effectiveness of personalized technology-enhanced learning in higher education: A meta-analysis*. Computers & Education, 223. https://doi.org/10.1016/j.compedu.2024.105169
- Dolmans, D. H. J. M., Loyens, S. M. M., Marcq, H., & Gijbels, D. (2016). *Deep and surface learning in problem-based learning*. Advances in Health Sciences Education, 21, 1087–1112.
- Theobald, E. J., et al. (2020). *Active learning narrows achievement gaps for underrepresented students in STEM*. PNAS, 117(12), 6476–6483.
- Salas-Pilco, S. Z., & Yang, Y. (2022). *Artificial intelligence applications in Latin American higher education: a systematic review*. IJETHE, 19(21).
- Lin, V., Huang, Y., & Lu, S. (2023). *The evolution of intelligent tutoring systems in the era of large language models: A systematic review*. Journal of Computers in Education, 11(2), 245-268.
- Babar, P. A. (2025). *Agentic AI for personalized education and adaptive learning environments*. International Journal of Computing and Engineering, 7(12), 1–10.

No se detectaron figuras/diagramas como archivos de imagen separados en `info_data/`; el docx referencia dos figuras internas (árbol de problemas y diagrama de metodología, "Fuente: propia - asistida con CanvasGPT") que no están disponibles como archivos independientes para reutilizar — se marcan como [inferido: no reutilizables directamente, deben rehacerse por Diseñador-TikZ].

---

## 4. Notas para agentes posteriores

- **Investigador:** el draft-base ya trae una pregunta de investigación, objetivos y 3 dimensiones de aprendizaje profundo (motivación, argumentación, resolución de problemas) muy cercanas a la idea del usuario — pero el TDR actual exige alianza intersedes con múltiples actores SIUN, lo que el draft-base no contempla (es un proyecto de un solo grupo/sede). Los 3 subproblemas candidatos deben decidir si se conserva el enfoque semillero-céntrico o se reescala a una alianza multi-actor.
- **Bibliografo-Propuesta:** partir de las ~47 referencias del draft-base como núcleo, verificar cuáles son Q1/Q2 y completar hasta el mínimo de 50 refs exigido.
- **Redactor:** el draft-base tiene prosa ya redactada y reutilizable en §2.1, §2.2, §5 y parte de §6 — útil como borrador de partida, ajustando terminología al nuevo alcance (alianza SIUN) si el usuario confirma que se responde al TDR de Alianzas Estratégicas.

## 5. Vault mirror

No se crearon notas en `vault/insumos/` en esta fase: los dos archivos de `info_data/` se clasificaron como TDR y draft-base (excluidos explícitamente de la regla de notas de insumos-paper). `vault/secciones/` y `vault/insumos/` ya existían (creados por el Orquestador con `.gitkeep`); no requirieron inicialización adicional.
