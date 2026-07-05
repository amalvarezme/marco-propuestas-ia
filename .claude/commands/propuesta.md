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
        superior por puntaje de criterios ponderados del TDR, empates en el
        límite del tercil se incluyen como ALTA; crosswalk:
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
Fase 0.5 [COMPUERTA G0.5] Solo aplica si el campo "Archivo TDR" de la tabla
        "Clasificación y ruta (Fase 0)" quedó con un valor no vacío
        (confirmado auto o resuelto vía el gate de ambigüedad — ambos
        cuentan). Si no hay TDR, omite esta fase por completo: la guía
        aplicable sigue siendo `guiaProyectosIA_Agente.md` sin cambios y el
        dispatcher continúa directo a la Fase 1a.
        ──→ OPT-IN G0.5 (concepto nuevo y separado del campo
        "Confirmaciones de usuario" de la Fase 0, que solo cubre el gate de
        ambigüedad): pregunta una sola vez, explícitamente, "Se detectó un
        TDR (<archivo>). ¿Genero una guía ajustada al TDR antes de la
        búsqueda de literatura? (sí/no)".
          - "no" → guía aplicable = `guiaProyectosIA_Agente.md` (sin
            cambios); registra G0.5 = OMITIDA-POR-USUARIO en
            `proposal/estado_propuesta.md` ("Compuertas tempranas (G0.5,
            G1a)").
          - "sí" → Task → investigador → genera
            `proposal/guia_ajustada_TDR.md` a partir de
            `guiaProyectosIA_Agente.md` (entrada de solo lectura — el
            archivo base NUNCA se modifica), ajustando
            secciones/alcance/requisitos según la tabla de criterios
            ponderados ya extraída en `proposal/insumos.md` ("Extracción
            del TDR").
        ──→ GATE G0.5: presenta `proposal/guia_ajustada_TDR.md` al usuario
        para aprobación explícita.
          - Aprobada → guía aplicable = `proposal/guia_ajustada_TDR.md`;
            registra G0.5 = APROBADA (quién/fecha) en
            `proposal/estado_propuesta.md`.
          - Cambios solicitados → vuelve a despachar la misma Task al
            `investigador` con las correcciones exactas del usuario, y
            repite el gate. NO avances sin aprobación explícita.
        En ambos desenlaces finales (OMITIDA-POR-USUARIO o APROBADA), el
        dispatcher continúa con la Fase 1a, que consume la "guía aplicable"
        resuelta aquí (ver bloque "Fase 1a" a continuación).
Fase 1a [COMPUERTA COMBINADA G1a] Scoping temprano: se ejecuta siempre,
        haya o no TDR — la "guía aplicable" resuelta en la Fase 0/Fase 0.5
        (base o ajustada) solo determina el parámetro (b) de la búsqueda del
        bibliógrafo en el paso (a) siguiente, no si esta fase corre.
        (a) Task → bibliografo-propuesta MODE=scope → exactamente 5 papers
        Q1/Q2 publicados en los últimos 2 años, abstract-only, que calcen
        con (i) el prompt original del usuario a `/propuesta` y (ii) la guía
        aplicable (`proposal/guia_ajustada_TDR.md` si G0.5 = APROBADA, si no
        `guiaProyectosIA_Agente.md`). Ver `bibliografo-propuesta.md`,
        "MODE=scope", para el contrato completo (herramientas, esquema de
        salida `proposal/scoping/papers/paper-{1..5}.md`, prohibición de
        leer cualquier borrador existente).
        (b) El DISPATCHER (no el subagente) ejecuta `graphify`, de forma
        aislada. Mecánica exacta:
          1. `cd proposal/scoping/` (cambio de CWD obligatorio).
          2. `graphify papers/` (INPUT_PATH relativo — siempre una ruta,
             nunca una pregunta en lenguaje natural, para no disparar el
             fast-path de graphify).
          3. La salida queda en `proposal/scoping/graphify-out/`.
        NUNCA ejecutes `graphify` desde la raíz del repo. NUNCA uses
        `--force`. Si `proposal/scoping/graphify-out/` ya existe de una
        iteración previa con papers distintos, bórralo antes de reconstruir
        (evita el shrink-guard y respuestas obsoletas del fast-path).
        (c) Task → investigador (rama de entrada temprana — ver
        `investigador.md`, "Entrada temprana (Fase 1a)") → 3 subproblemas
        tempranos, cada uno con (1) el gap, (2) de qué abstract(s)
        (`paper-N`) proviene, (3) un cruce de una línea contra el TDR/guía.
        ──→ COMPUERTA COMBINADA G1a: presenta juntos, en una sola solicitud
        de aprobación:
          1. Los 5 papers + parámetros de búsqueda (query, filtro de
             cuartil, rango de años, hits por herramienta).
          2. El grafo (ruta `proposal/scoping/graphify-out/` + las 3
             secciones del `GRAPH_REPORT.md`: God Nodes, Surprising
             Connections, Suggested Questions).
          3. Los 3 subproblemas tempranos, cada uno con su gap y su
             `paper-N` de origen.
        Reglas de iteración por componente (NO es un rechazo en bloque):
          - Cambio solo a los PAPERS → re-despacha MODE=scope con el ajuste
            solicitado → regenera los 5 abstracts → RECONSTRUYE el grafo
            (repite el paso (b)) → re-ejecuta la entrada temprana del
            investigador (repite el paso (c)) → vuelve a presentar G1a.
          - Cambio solo al GRAFO (reetiquetar/reagrupar) → re-ejecuta
            únicamente el clustering/reporte de `graphify`; los papers y los
            subproblemas quedan intactos; vuelve a presentar G1a. El
            auto-cascade a los subproblemas es explícitamente NO, salvo que
            el usuario lo pida (default adoptado).
          - Cambio solo a los SUBPROBLEMAS → re-despacha la entrada temprana
            del investigador con el feedback exacto del usuario; mismos 5
            papers y mismo grafo; vuelve a presentar G1a.
        Regla de faltante G1a: si el bibliógrafo reporta menos de 5 papers
        Q1/Q2 ≤2 años, el dispatcher NO debe sustituir ni relajar filtros en
        silencio — preséntale al usuario, en vivo, estas opciones:
          (a) ampliar la ventana de años,
          (b) relajar el cuartil (aceptar solo Q2 o un venue top nombrado),
          (c) ampliar/reformular los términos de búsqueda,
          (d) continuar con menos de 5,
          (e) aceptar un paper específico que el usuario nombre.
        Aplica la opción elegida y vuelve a presentar dentro de G1a.
        ──→ Al aprobar G1a: escribe los 3 subproblemas aprobados + G1a =
        APROBADA en `proposal/estado_propuesta.md` ("Compuertas tempranas
        (G0.5, G1a)" → sub-tabla "G1a — Scoping temprano": 5 papers,
        parámetros de búsqueda, ruta del grafo + extracto del reporte, los 3
        subproblemas tempranos con su gap/`paper-N`, y Estado G1a).
Fase 1  (en AMBAS rutas) Task → bibliografo-propuesta MODE=explore → mapa de
        literatura de amplitud (≥5 obras, devuelto inline al dispatcher, sin
        archivo de salida), despachado ANTES del investigador.
        Task → investigador → §2.1 subproblemas + pregunta de investigación.
        Inyecta inline en el prompt de esta Task el mapa de MODE=explore y,
        si existe, el bloque "PRIORIDAD TDR" de la Fase 0.
        Si la Fase 1a corrió y su gate cerró con G1a = APROBADA (ver
        `proposal/estado_propuesta.md`, sub-tabla "G1a — Scoping temprano"),
        inyecta ADEMÁS, inline, el bloque "SUBPROBLEMAS TEMPRANOS APROBADOS
        (G1a)" con los 3 subproblemas tempranos y su justificación
        gap↔`paper-N`. Si la Fase 1a no corrió (o no cerró en APROBADA),
        omite por completo este bloque adicional: el despacho de esta Task
        es entonces idéntico al de hoy.
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
  draft-base (todo es background), la clasificación no agrega preguntas de
  confirmación adicionales. El pre-step de `bibliografo-propuesta`
  (MODE=explore) en la Fase 1 sigue siendo obligatorio para ambas rutas,
  incluida esta — no se omite ni se bypassea el gate.

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
