---
description: Inicia el pipeline multi-agente de redacción de una propuesta de investigación en IA a partir de la idea del usuario y sus insumos.
argument-hint: [idea o contexto inicial de la propuesta]
---

El usuario quiere redactar una propuesta de investigación en IA siguiendo el
marco multi-agente descrito en `AGENTS.md` y en la referencia canónica del
pipeline, `.claude/agents/coordinador-propuesta.md`. **Tú, el asistente
primario, eres el dispatcher real** de este pipeline: `coordinador-propuesta`
es documentación de referencia, no un subagente activo, porque los subagentes
de Claude Code no pueden invocar a otros subagentes. Usa la herramienta `Task`
para despachar cada fase al subagente correspondiente en `.claude/agents/`.

Entrada del usuario:

$ARGUMENTS

## Roster de subagentes (`.claude/agents/`)

`insumos-observador`, `investigador`, `redactor`, `bibliografo-propuesta`,
`disenador-tikz`, `tikz-optimizer`, `revisor-figuras`, `revisor`. (No existen
`orquestador`, `observador` ni `bibliotecario` — usa siempre estos 8 nombres
reales.)

## Instrucciones de inicio

1. Si no hay insumos (PDFs/papers/enlaces) en el mensaje ni en `info_data/`,
   pídelos al usuario antes de avanzar. Los archivos fuente se guardan en
   `info_data/`. Si los hay, despacha con `Task` al subagente
   `insumos-observador` (Fase 0) para clasificar (TDR / draft-base /
   background), extraer el TDR si aplica, y estructurar el contexto en
   `proposal/insumos.md`. Ver el bloque "Fase 0" del pipeline abajo para el
   flujo completo de clasificación, gate de ambigüedad y decisión de ruta.
2. Crea/mantén un registro de estado del documento en
   `proposal/estado_propuesta.md` con: sección actual, artefactos clave
   (pregunta de investigación, subproblemas, objetivos, hipótesis) y estado de
   cada gate.
3. Avanza fase por fase según el pipeline de `coordinador-propuesta.md`
   (resumido abajo). Tras cada gate, presenta al usuario: (a) resumen de lo
   producido, (b) veredicto del `revisor` (o `revisor-figuras` en la Fase 5),
   (c) petición de aprobación explícita. **NO avances sin aprobación.**
4. Recuerda: toda la salida del documento es en español; los archivos van en
   `proposal/sections/*.tex` y `proposal/refs.bib`; ensambla `proposal/main.tex`
   al final (Fase 7).
5. Consulta `guiaProyectosIA_Agente.md` para las instrucciones párrafo a
   párrafo de cada sección antes de despachar cualquier fase.

## Pipeline (dispatch con `Task` fase por fase)

```
Fase 0  Task → insumos-observador → ingerir insumos (PDFs, papers, links, prompt)
        y clasificarlos (TDR / draft-base / background, ver
        `insumos-observador.md`); si hay TDR, extraer sus secciones + tabla
        de criterios ponderados.
        ──→ GATE DE AMBIGÜEDAD: si insumos-observador marca uno o más
        archivos como AMBIGUA (para TDR y/o draft-base), DETENTE y pregunta
        al usuario para confirmar/corregir. Si TDR y draft-base están
        ambiguos a la vez, combina ambas dudas en UNA sola pregunta.
        ──→ RAMA TDR: si hay un TDR confirmado (auto o por el usuario),
        calcula la tabla de prioridad por sección (regla ALTA = tercil
        superior por puntaje de criterios ponderados del TDR; crosswalk:
        calidad/innovación→§4/§5/§6, formación→§8, impacto
        territorial/ODS→§2.2/§3, articulación→§2.2/§8) y escríbela en
        `proposal/estado_propuesta.md` ("Prioridad por sección"). Si no hay
        TDR, omite este paso por completo.
        ──→ RAMA DRAFT: si hay draft-base confirmado → ruta DRAFT-EXISTS.
        Si no, pregunta explícitamente "¿existe un borrador previo?" antes
        de concluir NO-DRAFT; el usuario puede nombrar un archivo para pasar
        a DRAFT-EXISTS.
        ──→ Escribe la decisión de ruta (DRAFT-EXISTS | NO-DRAFT, archivo
        TDR, archivo draft-base y quién confirmó cada uno) en
        `proposal/estado_propuesta.md` ("Clasificación y ruta (Fase 0)").
Fase 1  (en AMBAS rutas) Task → bibliografo-propuesta MODE=explore → mapa de
        literatura de amplitud (≥5 obras, devuelto inline al dispatcher, sin
        archivo de salida), despachado ANTES del investigador.
        Task → investigador → §2.1 subproblemas + pregunta de investigación.
        Inyecta inline en el prompt de esta Task el mapa de MODE=explore y,
        si existe, el bloque "PRIORIDAD TDR" de la Fase 0.
        ──→ GATE Task → revisor ──→ usuario. NO avances sin aprobación.
Fase 2  Task → redactor → §2.2 pertinencia, §3 alcance
        ──→ GATE Task → revisor ──→ usuario. NO avances sin aprobación.
Fase 3  Task → investigador → §4.1 objetivo general + §4.2 objetivos específicos
        ──→ GATE Task → revisor (valida mapeo subproblema↔objetivo) ──→ usuario.
        NO avances sin aprobación.
Fase 4  Task → bibliografo-propuesta → §5.2 estado del arte (en paralelo)
        Task → investigador → §5.1, §5.3, hipótesis
        ──→ GATE Task → revisor ──→ usuario. NO avances sin aprobación.
Fase 5  Task → redactor → §6 metodología, luego bucle de figuras:
          Task → disenador-tikz (autor .tex)
          → Task → tikz-optimizer (compila a PNG, primer ajuste)
          → Task → revisor-figuras (audita, PASS/FAIL)
          → en FAIL, vuelve a Task → tikz-optimizer con los hallazgos
          → en PASS, continúa
        Task → redactor → §7 plan de trabajo (Gantt)
        ──→ GATE Task → revisor ──→ usuario. NO avances sin aprobación.
Fase 6  Task → redactor → §8 resultados; Task → bibliografo-propuesta → §9 referencias (BibTeX)
Fase 7  Task → revisor → auditoría final ──→ usuario. NO avances sin aprobación.
        Tú (el asistente primario) ensamblas `proposal/main.tex` una vez aprobado.
```

## Reglas de dependencia (haz que `revisor` las valide en cada gate)

- 3 subproblemas (§2.1) ↔ 3 objetivos específicos (§4.2), mapeo 1:1.
- Pregunta de investigación (cierre §2.1) ↔ objetivo general (§4.1).
- Hipótesis (cierre §5.2) ↔ objetivo general.
- Enfoques teóricos (§5.3) ↔ subproblemas (§2.1), causa-efecto explícito.
- Metodología (§6) ↔ objetivos específicos, cadena de valor.
- Plan de trabajo (§7) ↔ fases de la Metodología (§6).
- Resultados (§8) ↔ productos entregados en hitos del plan (§7).
- TRL 6 o 7 debe ser explícito en objetivos, pertinencia y resultados.

## Reglas de clasificación y ambigüedad

- Confirmación obligatoria ante ambigüedad: si `insumos-observador` marca un
  archivo como AMBIGUA para TDR y/o draft-base, el dispatcher DEBE detenerse
  y pedir confirmación al usuario antes de continuar (no autoresolver).
- El draft-base nunca es la única fuente: cuando existe, se complementa —no
  se reemplaza— con el mapa de MODE=explore y el resto de insumos de
  background.
- Sin bypass del gate: ambas rutas (DRAFT-EXISTS y NO-DRAFT) convergen en el
  mismo gate investigador→revisor→usuario existente; ninguna rama lo omite.
- Garantía retrocompatible: si no hay TDR ni archivos candidatos a
  draft-base (todo es background), el comportamiento es idéntico al de antes
  de este cambio — no se agregan preguntas ni pasos adicionales.

## Reglas de gate (obligatorias)

- Tras cada gate, presenta el veredicto PASS/FAIL del revisor correspondiente
  y espera aprobación explícita del usuario antes de despachar la siguiente
  fase. **Tras cada gate, NO avances sin aprobación.**
- En FAIL, vuelve a despachar con `Task` al agente responsable de la sección
  con las correcciones exactas del revisor, y repite el gate.
- No reescribas contenido de sección tú mismo; ese trabajo es de los
  subagentes especialistas.

Comienza ahora confirmando la idea del usuario y listando los insumos
detectados, luego arranca la Fase 0 despachando `insumos-observador` con
`Task`.
