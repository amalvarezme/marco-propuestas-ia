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
4. **Estructura:** Sigue rigurosamente las 10 secciones de la
   `guiaProyectosIA_Agente.md`. No omitas ni renumeraciones secciones.
5. **Dependencias cruzadas (obligatorias):**
   - Los 3 subproblemas (§2.1) ↔ 3 objetivos específicos (§4.2), mapeo 1:1.
   - La pregunta de investigación (cierre §2.1) ↔ objetivo general (§4.1).
   - La hipótesis (cierre §5.2) ↔ objetivo general.
   - Enfoques teóricos (§5.3) ↔ subproblemas (§2.1), causa-efecto explícito.
   - Metodología (§6) ↔ objetivos específicos, cadena de valor.
   - Plan de trabajo (§7) ↔ fases de la Metodología (§6).
   - Resultados (§8) ↔ productos entregados en hitos del plan (§7).
6. **Calidad bibliográfica:** ≥30 refs Q1/Q2 (≤3 años) para §5.2; ≥50 refs
   totales para §10; formato APA o IEEE (priorizar IEEE). Sin tesis; preprints
   solo de labs/líderes reconocidos.
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
| `investigador` | opus | Subproblemas, pregunta, objetivos, hipótesis, enfoques |
| `redactor` | opus | Secciones narrativas (§1–§3, §6–§8) |
| `insumos-observador` | sonnet | Ingesta y estructuración de insumos del usuario |
| `bibliografo-propuesta` | sonnet | Bibliografía (§5.2, §10) |
| `revisor` | sonnet | Validación de coherencia/calidad en cada gate |
| `disenador-tikz` | sonnet | Autoría de diagramas TikZ |
| `revisor-figuras` | sonnet | Auditoría visual publication-ready de figuras (PNG) |
| `tikz-optimizer` | sonnet | Compilación y optimización visual de diagramas TikZ |

No existen agentes llamados `orquestador`, `observador` (a secas) ni
`bibliotecario`; esos nombres no forman parte de este marco.

## Flujo del pipeline (interactivo, con gates)

```
Fase 0  Insumos-Observador → ingerir insumos
Fase 1  Investigador → §2.1 subproblemas + pregunta ──→ GATE Revisor ──→ user
Fase 2  Redactor → §2.2 pertinencia, §3 alcance ──→ GATE Revisor ──→ user
Fase 3  Investigador → §4.1 + §4.2 ──→ GATE Revisor (subproblema↔objetivo) ──→ user
Fase 4  Bibliografo-Propuesta → §5.2 estado del arte (paralelo)
        Investigador → §5.1, §5.3, hipótesis ──→ GATE Revisor ──→ user
Fase 5  Redactor → §6 metodología, luego bucle de figuras:
          Diseñador-TikZ (autor .tex)
          → Tikz-Optimizer (compila a PNG, primer ajuste)
          → Revisor-Figuras (audita, PASS/FAIL)
          → en FAIL, vuelve a Tikz-Optimizer con los hallazgos
          → en PASS, continúa
        Redactor → §7 plan de trabajo (Gantt) ──→ GATE Revisor ──→ user
Fase 6  Redactor → §8 resultados; Bibliografo-Propuesta → §10 referencias (BibTeX)
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
10 secciones con gates sigue el comando `/propuesta`.

| Agente | Cuándo despacharlo directamente |
|--------|--------------------------------|
| `disenador-tikz` | Rediseñar o crear diagramas TikZ de la propuesta |
| `revisor-figuras` | Auditar visualmente figuras renderizadas (PNG) y describir problemas publication-ready |
| `tikz-optimizer` | Compilar y optimizar visualmente diagramas TikZ existentes |
| `investigador` | Definir/refinar subproblemas, pregunta, objetivos, hipótesis, enfoques |
| `redactor` | Redactar o revisar secciones narrativas (§1–§3, §6–§8) |
| `revisor` | Validar coherencia y calidad de secciones ya redactadas |
| `bibliografo-propuesta` | Construir o actualizar la bibliografía (§5.2, §10) |
| `insumos-observador` | Ingerir y estructurar insumos del usuario (PDFs, papers) |

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
| §2.1 Problemática + pregunta | Investigador |
| §2.2 Pertinencia | Redactor |
| §3 Alcance | Redactor |
| §4.1 Objetivo general | Investigador |
| §4.2 Objetivos específicos | Investigador |
| §5.1 Marco conceptual | Investigador |
| §5.2 Estado del arte + hipótesis | Bibliografo-Propuesta (refs) + Investigador (hipótesis) |
| §5.3 Enfoques teóricos | Investigador |
| §6 Metodología | Redactor |
| Diagramas (árbol problemas, metodológico, Gantt) | Diseñador-TikZ |
| Auditoría visual de figuras (publication-ready) | Revisor-Figuras |
| Compilación/optimización visual de diagramas (loop PNG) | Tikz-Optimizer |
| §7 Plan de trabajo | Redactor |
| §8 Resultados y productos | Redactor |
| §10 Referencias | Bibliografo-Propuesta |
| Revisión de coherencia y calidad | Revisor |
| Coordinación del pipeline de propuesta | Coordinador-Propuesta |

> **Runtime canónico:** Claude Code (`.claude/agents/` +
> `.claude/commands/propuesta.md`) es el **único runtime/fuente de verdad**
> de este marco. El asistente primario de Claude Code despacha
> el pipeline completo vía `/propuesta` y puede además despachar directamente
> cualquier subagente de propuesta para tareas puntuales (ver sección
> "Dispatch directo" arriba).
