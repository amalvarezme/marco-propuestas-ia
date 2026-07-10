# Playbook: Marco de Redacción de Propuestas de Investigación en IA

Este playbook rige el comportamiento de todos los agentes del marco multi-agente
de redacción de propuestas.

**Runtime canónico: Claude Code.** El **asistente primario de Claude Code**
es el dispatcher real del pipeline: usa la herramienta `Task` para despachar
cada fase al subagente correspondiente definido en `.claude/agents/`, siguiendo
el comando `/propuesta` (`.claude/commands/propuesta.md`). El archivo
`.claude/agents/coordinador-propuesta.md` es la **referencia canónica** del
pipeline y de las dependencias de despacho —no es un subagente activo, porque
los subagentes de Claude Code no pueden invocar a otros subagentes. El agente
**Revisor** valida en cada **puerta de revisión (gate)** antes de avanzar.

## Reglas globales

1. **Idioma:** Los *system prompts* de los agentes están en inglés, pero toda
   la **salida del documento (propuesta) debe redactarse en español**.
2. **Insumos:** La propuesta se construye desde un prompt/idea del usuario más
   PDFs, papers, enlaces o información relevante que este aporte. Los archivos
   fuente (PDFs, papers, propuestas previas, documentos de referencia) se
   guardan en `info_data/`. El agente **Insumos-Observador** los lee desde ahí y
   extrae/estructura esos insumos en un contexto compartido.
3. **Enfoque:** Productos/servicios de IA con innovación investigativa,
   transferencia tecnológica clara, productos tangibles con **TRL 6 o 7**.
4. **Estructura:** Sigue rigurosamente las 16 secciones de la
   `guiaProyectosIA_Agente.md`. No omitas ni renumeraciones secciones.
5. **Dependencias cruzadas (obligatorias):**
   - Los 3 subproblemas (§3) ↔ 3 objetivos específicos (§7), mapeo 1:1.
   - La pregunta de investigación (cierre §3) ↔ objetivo general (§6).
   - La hipótesis (§5) ↔ objetivo general (§6).
   - Metodología (§10) ↔ objetivos específicos (§7), marco conceptual (§8) y
     equipo de trabajo (§9), cadena de valor. El punto 2 de Metodología nombra
     el enfoque/algoritmo por subproblema con razonamiento causa-efecto
     explícito referenciando el marco conceptual (§8) — función que antes
     cubría el desaparecido §5.3 Enfoques teóricos.
   - Equipo de trabajo (§9) deriva sus roles de los objetivos específicos
     (§7); nunca de la Metodología (§10).
   - Cronograma de actividades (§14) ↔ fases de la Metodología (§10).
   - Resultados esperados (§11) ↔ productos entregados en hitos del
     cronograma (§14).
   - Presupuesto (§13) ↔ Metodología (§10) y Cronograma (§14) —referencia
     hacia adelante válida, ya que Presupuesto se redacta antes que Cronograma
     en el pipeline pero ambos referencian las mismas fases de Metodología.
   - TRL 6 o 7 debe ser explícito en pertinencia (§2) y resultados esperados
     (§11); **nunca** se nombra en objetivo general (§6) ni en objetivos
     específicos (§7).
6. **Calidad bibliográfica:** ≥10 refs Q1/Q2 para §2 Justificación y
   pertinencia (mínimo 6 párrafos); ≥30 refs Q1/Q2 (≤3 años) para §4 Estado
   del arte; ≥50 refs totales para §16 Bibliografía; formato **APA
   author-year únicamente** (natbib+apalike, `\citet{}`/`\citep{}`) — el
   estilo numérico IEEE (`[1]`) está prohibido, conforme a
   `guiaProyectosIA_Agente.md` §16 Bibliografía. Sin tesis; preprints solo de
   labs/líderes reconocidos.
7. **Salida LaTeX:** Cada sección se escribe como archivo `.tex` en
   `proposal/sections/`; referencias en `proposal/refs.bib`; ensamblaje en
   `proposal/main.tex`. El template `main.tex` incluye un footer con los logos
   institucionales (`proposal/logos/`: LabIA, UNAL, GCPDS) vía `fancyhdr`; los
   agentes no deben eliminarlo.

## Roster de agentes (`.claude/agents/`) y modelos por defecto

El marco tiene **10 agentes**, todos definidos en `.claude/agents/` (fuente de
verdad):

| Agente | Modelo por defecto | Rol |
|--------|--------------------|-----|
| `coordinador-propuesta` | sonnet | Referencia canónica del pipeline (no despachable como subagente activo) |
| `investigador` | opus | Subproblemas, pregunta, objetivos, hipótesis, marco conceptual |
| `redactor` | opus | Secciones narrativas (§1, §2, §9–§12, §14–§15) |
| `insumos-observador` | sonnet | Ingesta y estructuración de insumos del usuario |
| `bibliografo-propuesta` | sonnet | Bibliografía (§4, §16) |
| `revisor` | sonnet | Validación de coherencia/calidad en cada gate |
| `presupuestador` | sonnet | Presupuesto (§13): tabla de rubros + aritmética + cofinanciación |
| `disenador-tikz` | sonnet | Autoría de diagramas TikZ |
| `revisor-figuras` | sonnet | Auditoría visual publication-ready de figuras (PNG) |
| `tikz-optimizer` | sonnet | Compilación y optimización visual de diagramas TikZ |

No existen agentes llamados `orquestador`, `observador` (a secas) ni
`bibliotecario`; esos nombres no forman parte de este marco.

## Flujo del pipeline (interactivo, con gates)

```
Fase 0  Insumos-Observador → ingerir insumos
Fase 1  Investigador → §3 descripción del problema + pregunta ──→ GATE Revisor ──→ user
Fase 2  Bibliografo-Propuesta → §4 estado del arte (paralelo)
        Investigador → §5 hipótesis ──→ GATE Revisor ──→ user
Fase 3  Redactor → §2 justificación y pertinencia ──→ GATE Revisor ──→ user
Fase 4  Investigador → §6 objetivo general + §7 objetivos específicos ──→ GATE Revisor
        (subproblema↔objetivo específico; también valida hipótesis↔objetivo general) ──→ user
Fase 5  Investigador → §8 marco conceptual (paralelo)
        Redactor → §9 equipo de trabajo (deriva roles de §7, nunca de Metodología) ──→ GATE Revisor ──→ user
Fase 6  Redactor → §10 metodología, luego bucle de figuras:
          Diseñador-TikZ (autor .tex)
          → Tikz-Optimizer (compila a PNG, primer ajuste)
          → Revisor-Figuras (audita, PASS/FAIL)
          → en FAIL, vuelve a Tikz-Optimizer con los hallazgos
          → en PASS, continúa
        ──→ GATE Revisor ──→ user
        Redactor → §11 resultados esperados; §12 consideraciones éticas (sin gate propio)
Fase 6.4  Presupuestador → §13 presupuesto (interactivo) ──→ GATE Revisor ──→ user
Fase 6.45 Redactor → §14 cronograma de actividades (Gantt); §15 productos esperados
          Bibliografo-Propuesta → §16 bibliografía (BibTeX) (sin gate propio)
Fase 6.5  Redactor → front-matter (Resumen, Resumen ejecutivo, Palabras clave),
          síntesis de §1–§16 ya aprobadas ──→ GATE Revisor ──→ user
Fase 7  Revisor → auditoría final ──→ user; Coordinador-Propuesta → ensambla main.tex
```

En cada **GATE**, el asistente primario de Claude Code (siguiendo la
referencia de `coordinador-propuesta`) **detiene** el flujo y espera
aprobación del usuario antes de avanzar. El Revisor devuelve PASS/FAIL +
correcciones.

## Dispatch directo de agentes de propuesta

El **asistente primario de Claude Code** puede despachar directamente
cualquier subagente de propuesta para tareas puntuales —arreglar figuras,
revisar una sección, actualizar bibliografía, refinar objetivos— **sin pasar
por el pipeline completo de `coordinador-propuesta`**. El pipeline completo de
16 secciones con gates sigue el comando `/propuesta`.

| Agente | Cuándo despacharlo directamente |
|--------|--------------------------------|
| `disenador-tikz` | Rediseñar o crear diagramas TikZ de la propuesta |
| `revisor-figuras` | Auditar visualmente figuras renderizadas (PNG) y describir problemas publication-ready |
| `tikz-optimizer` | Compilar y optimizar visualmente diagramas TikZ existentes |
| `investigador` | Definir/refinar subproblemas, pregunta, objetivos, hipótesis, marco conceptual |
| `redactor` | Redactar o revisar secciones narrativas (§1, §2, §9–§12, §14–§15) |
| `revisor` | Validar coherencia y calidad de secciones ya redactadas |
| `bibliografo-propuesta` | Construir o actualizar la bibliografía (§4, §16) |
| `insumos-observador` | Ingerir y estructurar insumos del usuario (PDFs, papers) |
| `presupuestador` | Construir o ajustar el presupuesto (§13): rubros, montos, cofinanciación |

Cuando despaches un agente de propuesta directamente, incluye en el prompt
todo el contexto necesario (sección asignada, artefactos clave, dependencias
cruzadas) ya que el agente no tiene el estado del pipeline que el
`coordinador-propuesta` mantiene.

## Guía completa de redacción

La guía autoritativa sección por sección (con instrucciones de párrafo a
párrafo, verbos rectores, parámetros de calidad y volumen bibliográfico) vive
en `guiaProyectosIA_Agente.md`. Todos los agentes deben consultarla al redactar
su sección asignada. Resumen de asignación:

| Sección | Agente responsable |
|---------|--------------------|
| Ingesta insumos | Insumos-Observador |
| §1 Título | Redactor |
| §2 Justificación y pertinencia | Redactor |
| §3 Descripción del problema + pregunta de investigación | Investigador |
| §4 Estado del arte | Bibliografo-Propuesta |
| §5 Hipótesis | Investigador |
| §6 Objetivo general | Investigador |
| §7 Objetivos específicos | Investigador |
| §8 Marco conceptual | Investigador |
| §9 Equipo de trabajo | Redactor |
| §10 Metodología | Redactor |
| Diagramas (árbol de problemas, metodológico, Gantt) | Diseñador-TikZ |
| Auditoría visual de figuras (publication-ready) | Revisor-Figuras |
| Compilación/optimización visual de diagramas (loop PNG) | Tikz-Optimizer |
| §11 Resultados esperados | Redactor |
| §12 Consideraciones éticas | Redactor |
| §13 Presupuesto | Presupuestador |
| §14 Cronograma de actividades | Redactor |
| §15 Productos esperados | Redactor |
| §16 Bibliografía | Bibliografo-Propuesta |
| Front-matter (Resumen, Resumen ejecutivo, Palabras clave) | Redactor |
| Revisión de coherencia y calidad | Revisor |
| Coordinación del pipeline de propuesta | Coordinador-Propuesta |

> **Runtime canónico:** Claude Code (`.claude/agents/` +
> `.claude/commands/propuesta.md`) es el **único runtime/fuente de verdad**
> de este marco. El asistente primario de Claude Code despacha
> el pipeline completo vía `/propuesta` y puede además despachar directamente
> cualquier subagente de propuesta para tareas puntuales (ver sección
> "Dispatch directo" arriba).
