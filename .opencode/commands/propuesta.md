---
description: Inicia el pipeline multi-agente de redacción de una propuesta de investigación en IA a partir de la idea del usuario y sus insumos.
---

El usuario quiere redactar una propuesta de investigación en IA siguiendo el
marco multi-agente descrito en `AGENTS.md` y en la referencia canónica del
pipeline, `coordinador-propuesta.md` (documento de referencia del pipeline, no incluido en este puerto). **Tú, el asistente
primario, eres el dispatcher real** de este pipeline: `coordinador-propuesta`
es documentación de referencia, no un subagente activo, porque los subagentes
de OpenCode no pueden invocar a otros subagentes. Usa la herramienta `task` (o la mención `@<agente>`)
para despachar cada fase al subagente correspondiente en `.opencode/agents/` (o mediante la mención `@<agente>`).

Entrada del usuario:

$ARGUMENTS

## Roster de subagentes (`.opencode/agents/`)

`insumos-observador`, `investigador`, `redactor`, `bibliografo-propuesta`,
`disenador-tikz`, `tikz-optimizer`, `revisor-figuras`, `revisor`,
`presupuestador`. (No existen `orquestador`, `observador` ni `bibliotecario`
— usa siempre estos 9 nombres reales.)

## Instrucciones de inicio

1. Si no hay insumos (PDFs/papers/enlaces) en el mensaje ni en `info_data/`,
   pídelos al usuario antes de avanzar. Los archivos fuente se guardan en
   `info_data/`. Si los hay, despacha con `task` al subagente
   `insumos-observador` (Fase 0) para clasificar (TDR / draft-base /
   background), extraer el TDR si aplica, y estructurar el contexto en
   `proposal/insumos.md`. Ver el bloque "Fase 0" del pipeline abajo para el
   flujo completo de clasificación, gate de ambigüedad y decisión de ruta.
2. Crea/mantén un registro de estado del documento en
   `proposal/estado_propuesta.md` con: sección actual, artefactos clave
   (pregunta de investigación, subproblemas, objetivos, hipótesis) y estado de
   cada gate. En esta misma Fase 0 asegúrate también de que existan
   `vault/secciones/` y `vault/insumos/` (créalos si faltan) — el mirror
   Obsidian de la propuesta (ver "Vault mirror" en `coordinador-propuesta.md`).
   Más adelante (a partir de G1b, ver bloque "Fase 1b" abajo), el dispatcher
   ejecuta `graphify` sobre `vault/` y escribe su salida en
   `vault/graphify-out/` — scratch, gitignored (cubierto por la regla
   existente `graphify-out/` en `.gitignore`), nunca se commitea, igual que
   `proposal/scoping/graphify-out/` de la Fase 1a/1b (son dos corridas de
   `graphify` completamente distintas, sobre entradas y salidas distintas).
3. Avanza fase por fase según el pipeline de `coordinador-propuesta.md`
   (resumido abajo). Tras cada gate, presenta al usuario: (a) resumen de lo
   producido, (b) veredicto del `revisor` (o `revisor-figuras` en la Fase 5),
   (c) petición de aprobación explícita. **NO avances sin aprobación.**
4. Recuerda: toda la salida del documento es en español; los archivos van en
   `proposal/sections/*.tex` y `proposal/refs.bib`; ensambla `proposal/main.tex`
   al final (Fase 7). También existen `vault/secciones/*.md` y
   `vault/insumos/*.md`: un mirror visual en Markdown (Obsidian) mantenido por
   los propios agentes que escriben secciones (`insumos-observador`,
   `investigador`, `redactor`, `bibliografo-propuesta`, `presupuestador`) al
   escribir su `.tex` o `.bib` correspondiente — tú no lo regeneras aparte.
5. Consulta `guiaProyectosIA_Agente.md` para las instrucciones párrafo a
   párrafo de cada sección antes de despachar cualquier fase.

## Grafo de coherencia del vault (asesor, NO bloqueante)

A partir de la aprobación de G1b, el DISPATCHER mantiene un grafo de ideas
sobre `vault/` con `graphify` y lo inyecta como evidencia asesora en cada
`Task → revisor` de las Fases 1-5 y 7 (ver los pasos "[NUEVO]" dentro de cada
fase, abajo). Esta corrida es DISTINTA de la de la Fase 1a/1b (que indexa
`proposal/scoping/papers/`, el corpus de papers de scoping, y escribe en
`proposal/scoping/graphify-out/`): la corrida de esta sección indexa el
mirror Obsidian (`vault/secciones/` + `vault/insumos/`) y escribe en
`vault/graphify-out/`. Nunca la ejecuta `revisor` (solo tiene Read/Grep/Glob,
sin Bash) — siempre la dispara el dispatcher.

Formato exacto del bloque que el dispatcher inyecta inline en el prompt de
`Task → revisor` (el mismo tag `ASESOR-GRAFO` que usa `revisor.md` en su
HALLAZGOS debe leerse contra este bloque):

```
EVIDENCIA DE GRAFO (asesora, NO bloqueante) — vault/graphify-out/
Dependencias duras (guia_ajustada_TDR "Nota de trazabilidad"): §3↔§7, §3↔§6, §5↔§6, §10↔§8.
- Presentes: <edges hallados>
- Ausentes/huérfanas: <p. ej. SP3 sin objetivo enlazado>
- God nodes / conexiones sorprendentes: <extracto de GRAPH_REPORT.md>
Es pista; tu checklist manual sigue siendo la autoridad del veredicto.
```

Nota de renumeración: el 4º par (antes `§5.3↔§2.1`, Enfoques teóricos ↔
subproblemas) ya no existe como sección propia — `§5.3 Enfoques teóricos` fue
eliminada y su función (nombrar el enfoque/algoritmo por subproblema con
causa-efecto explícito) quedó absorbida en Metodología (§10), punto 2, que
referencia el marco conceptual (§8); de ahí el par `§10↔§8`.

Si graphify revela un `[[wikilink]]` roto, una contradicción, o una idea
huérfana frente a uno de los 4 pares de trazabilidad de arriba, el
dispatcher además agrega una fila a `## Hallazgos de coherencia (grafo)` en
`proposal/estado_propuesta.md` (crea la sección la primera vez que se usa),
con fase, archivo, y tipo de problema. Este hallazgo NUNCA por sí solo hace
que `revisor` cambie su VEREDICTO a FAIL.

## Grafo de pipeline (`proposal/pipeline/`, tercer grafo, distinto de papers y vault)

Un TERCER grafo, independiente de los otros dos, indexa la estructura del
pipeline mismo (fases/compuertas/agentes/artefactos), no el corpus de
papers ni el mirror Obsidian. Corpus y CWD dedicados: `proposal/pipeline/`
— NUNCA corre desde la raíz del repo.

Corpus: el DISPATCHER escribe/actualiza un archivo `proposal/pipeline/<NN>-<fase>.md`
por cada evento de fase (p. ej. `00-fase0.md`, `10-fase1a.md`,
`11-fase1b.md`, `20-fase1.md`, ...), más un `proposal/pipeline/_estado.md`
compacto que espeja la tabla de compuertas en cada actualización (mantiene
el corpus autocontenido bajo el único CWD `proposal/pipeline/`, ya que
`estado_propuesta.md` vive un nivel arriba). Plantilla mínima por evento:

```markdown
---
fase: <id>
agentes: [<subagente(s)>]
gate: <Gx | none>
veredicto: <PASS | FAIL | pending | n/a>
fecha: <YYYY-MM-DD>
---
# Fase <id> — <nombre>
## Entradas
- <artefacto/sección consumida>
## Salidas
- <sección/artefacto producido>  [[<nota-vault-o-sección>]]
## Dependencias
- <fase previa de la que depende>
```

Cuándo actualiza: en CADA transición de compuerta (los mismos puntos donde
el dispatcher voltea `gate_status`, ver "Reglas de gate (obligatorias)"
abajo) — ver el bloque `[NUEVO] DISPATCHER: pipeline-graph` dentro de cada
fase/compuerta. Mecánica: el DISPATCHER únicamente escribe/actualiza el
archivo de evento `.md` y `proposal/pipeline/_estado.md` — no se ejecuta
`graphify` sobre `proposal/pipeline/` (build/update/export eliminados por
no aportar valor consumido; overhead de token descartado). Nunca lo hace
`revisor` (solo Read/Grep/Glob) — siempre lo hace el dispatcher.

## Pipeline (dispatch con `task` fase por fase)

```
Fase 0  ──→ RESOLUCIÓN DE RUN-ID (identidad de la corrida): antes de
        continuar, resuelve el run-id de esta corrida. Esquema
        `<YYYY-MM>-<slug>` (p. ej. `2026-07-siun-alianzas`). `<YYYY-MM>` sale
        de la fecha del sistema. `<slug>` = 2-4 palabras clave en
        kebab-case, en minúsculas, sin tildes/ñ (ASCII-folded), derivadas de
        la idea en `$ARGUMENTS` descartando stopwords. Override: si
        `$ARGUMENTS` empieza con `run-id=<valor>` o `--run-id <valor>`,
        valida `<valor>` contra `[a-z0-9-]+` y úsalo tal cual (el resto de
        `$ARGUMENTS` es la idea); si no hay override, usa el slug
        auto-derivado. Escribe el run-id resuelto en
        `proposal/estado_propuesta.md` ("## Identidad de la corrida
        (run-id)": `run_id`, `slug_source` [auto|user], `idea`, `creada`
        [YYYY-MM-DD], `estado` [activa]) y agrega una fila a
        `proposals/registry.md` (crea el archivo con su tabla de encabezado
        si no existe: `| run-id | creada | cerrada | estado | idea (breve) |
        archivo | commit |`).
        ──→ GUARDIA DE COLISIÓN (corrida sin terminar): si
        `proposal/estado_propuesta.md` ya existe con `estado: activa` en su
        bloque "Identidad de la corrida" y no todas las compuertas están
        cerradas, DETENTE y exige confirmación explícita: "Existe una
        corrida SIN terminar (`<run-id>`, última compuerta `<Gx>`).
        ¿Archivarla y empezar una nueva? (sí/no)". Solo "sí" continúa con
        ARCHIVADO-Y-REINICIO (abajo); "no" ofrece reanudar la corrida
        existente en vez de iniciar una nueva.
        ──→ ARCHIVADO-Y-REINICIO (solo corridas futuras, tras "sí" arriba):
          1. Lee el `run_id` previo de `estado_propuesta.md`.
          2. `mkdir -p proposals/<run-id-previo>/`; copia el contenido de la
             corrida activa a `proposals/<run-id-previo>/proposal/` y
             `proposals/<run-id-previo>/vault/` (misma superficie que la
             eliminación única de la corrida actual, ver Fase de limpieza
             única en el diseño).
          3. Escribe `proposals/<run-id-previo>/run.md` (manifiesto: run-id,
             idea, fechas, estado final de cada compuerta, conteo de
             referencias, commit); marca la fila del registro como
             `archivada`, fija `cerrada` y `archivo`.
          4. Commit `chore(proposals): archive run <run-id-previo>`;
             force-add los tres `graph.json`/`GRAPH_REPORT.md`/`graph.html`
             (viven bajo `graphify-out/`, gitignored) para que la corrida
             archivada quede autocontenida en el historial.
          5. Reinicia el árbol activo a scaffolding: vacía
             `proposal/sections/`, `proposal/scoping/papers/`,
             `proposal/pipeline/`; reescribe vacíos
             `proposal/estado_propuesta.md`, `proposal/refs.bib`,
             `proposal/insumos.md`; vacía `vault/secciones/` y
             `vault/insumos/` (conserva `.gitkeep`); borra los dos árboles
             scratch `graphify-out/` (scoping, vault) — `proposal/pipeline/`
             ya no produce grafo, solo se vacía como parte del scaffolding
             de arriba. CONSERVA
             `proposal/build.sh`, `proposal/scripts/`, `proposal/logos/`.
          6. Continúa con el nuevo run-id (paso "RESOLUCIÓN DE RUN-ID"
             arriba).
        ──→ SIN CORRIDA PREVIA: si no existe una corrida anterior, omite
        GUARDIA DE COLISIÓN y ARCHIVADO-Y-REINICIO por completo; continúa
        directo con el resto de la Fase 0.
        Task → insumos-observador → ingerir insumos (PDFs, papers, links, prompt)
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
        calidad/innovación→§6/§7 (objetivos), §4/§5/§8 (estado del
        arte/hipótesis/marco conceptual), §10 (metodología); formación→§15;
        impacto territorial/ODS→§2; articulación→§2/§15) y escríbela en
        `proposal/estado_propuesta.md` ("Prioridad por sección"). Si no hay
        TDR, omite este paso por completo.
        ──→ RAMA DRAFT: si hay draft-base confirmado → ruta DRAFT-EXISTS.
        Si no, pregunta explícitamente "¿existe un borrador previo?" antes
        de concluir NO-DRAFT; el usuario puede nombrar un archivo para pasar
        a DRAFT-EXISTS.
        ──→ Escribe la decisión de ruta (DRAFT-EXISTS | NO-DRAFT, archivo
        TDR, archivo draft-base y quién confirmó cada uno) en
        `proposal/estado_propuesta.md` ("Clasificación y ruta (Fase 0)").
        ──→ CORROBORACIÓN DE SECCIONES (solo si hay TDR): lee de insumos.md
        "Secciones obligatorias declaradas por el TDR" y registra en
        estado_propuesta.md ("Clasificación y ruta") los 3 campos nuevos (TDR
        especifica secciones, Fuente, Evidencia).
Fase 0.5 [COMPUERTA G0.5] Solo aplica si el campo "Archivo TDR" de la tabla
        "Clasificación y ruta (Fase 0)" quedó con un valor no vacío
        (confirmado auto o resuelto vía el gate de ambigüedad — ambos
        cuentan). Si no hay TDR, omite esta fase por completo: la guía
        aplicable sigue siendo `guiaProyectosIA_Agente.md` sin cambios y el
        dispatcher continúa directo a la Fase 1a.
        ──→ [BLOQUEO DURO — corroboración de secciones] Verifica "TDR
        especifica sus propias secciones":
          - Sí (TDR mismo o `doc-secciones` que aporta la lista) → continúa
            al opt-in; el investigador usará esa lista como estructura
            obligatoria.
          - No y SIN `doc-secciones` con la lista → DETENTE: no opt-in, no
            despacho al investigador; G0.5 NO puede pasar. Muestra el
            mensaje de bloqueo (abajo), registra G0.5 = BLOQUEADA. Exits:
            (a) el usuario aporta el documento → re-corrobora y continúa;
            (b) el usuario opta EXPLÍCITAMENTE por no ajustar → base guide,
            G0.5 = OMITIDA-POR-USUARIO.
          - Si el gate de ambigüedad de la Fase 0 sigue pendiente, combina
            ambas peticiones en UN solo mensaje (misma lógica de combinación
            existente).

        > **Fase 0.5 en pausa — falta el documento de secciones obligatorias.**
        > El TDR clasificado (`<archivo TDR>`) **no enumera explícitamente** la
        > estructura/secciones que la propuesta debe contener; solo trae una tabla de
        > criterios de evaluación ponderados. Para ajustar la guía a la estructura
        > realmente exigida (y no solo a los pesos de los criterios) necesito el
        > documento que liste las secciones obligatorias de la propuesta.
        > Por favor aporta ese documento (un archivo de "secciones"/"estructura" de la
        > propuesta, PDF o .docx) en `info_data/` y confírmame el nombre. Hasta
        > entonces la compuerta **G0.5 queda BLOQUEADA**: no puedo generar
        > `guia_ajustada_TDR.md` por la vía ajustada al TDR.
        > Alternativa explícita: si no existe tal documento y prefieres seguir con la
        > guía base (`guiaProyectosIA_Agente.md`) sin ajuste al TDR, dímelo y lo
        > registro como G0.5 = OMITIDA-POR-USUARIO (no genero una guía "a medias" desde
        > solo los criterios).

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
          3. `graphify export html` (obligatorio, no opcional — genera
             `proposal/scoping/graphify-out/graph.html`, el grafo interactivo
             navegable en el navegador, para facilitar el análisis visual del
             usuario más allá de las 3 secciones de texto del reporte).
          4. La salida queda en `proposal/scoping/graphify-out/` (`graph.json`,
             `graph.html`, `GRAPH_REPORT.md`).
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
          2. El grafo: la ruta del HTML interactivo
             `proposal/scoping/graphify-out/graph.html` (indícale al usuario
             que puede abrirlo en el navegador para explorar visualmente
             nodos/comunidades) + las 3 secciones del `GRAPH_REPORT.md`: God
             Nodes, Surprising Connections, Suggested Questions.
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
        ──→ [NUEVO] DISPATCHER: pipeline-graph (primera inicialización):
        escribe `proposal/pipeline/00-fase0.md` + `10-fase1a.md` (evento de
        esta compuerta) y `proposal/pipeline/_estado.md`.
Fase 1b [COMPUERTA COMBINADA G1b] Expansión de corpus SOTA: se ejecuta
        siempre que la Fase 1a cerró con G1a = APROBADA (ver
        `proposal/estado_propuesta.md`, sub-tabla "G1a — Scoping temprano");
        si G1a no corrió o no cerró en APROBADA, omite esta fase por
        completo y continúa directo a la Fase 1.
        (a) Task → bibliografo-propuesta MODE=sota, sub-paso **corpus** →
        expande el corpus semilla de 5 papers de G1a a 30-40 papers
        abstract-only (`paper-6.md`..`paper-N.md`, dedup por DOI/título
        contra el corpus semilla, `paper-1..5.md` byte-inalterados). Ver
        `bibliografo-propuesta.md`, "MODE=sota" → sub-paso "corpus", para el
        contrato completo (herramientas, esquema de salida, Regla de
        faltante).
        (b) El DISPATCHER (no el subagente) actualiza el grafo sobre el
        corpus ampliado, de forma incremental (NUNCA reconstruye desde
        cero, a diferencia del paso (b) de la Fase 1a). Mecánica exacta:
          1. `cp -R proposal/scoping/graphify-out/ proposal/scoping/graphify-out-g1a-snapshot/`
             (snapshot plano del grafo de G1a — 34 nodos/57 edges/5
             comunidades — antes de tocar nada; esta copia queda fija para
             siempre, NUNCA se reconstruye, sirve de referencia/diff frente
             al grafo ampliado).
          2. NO borres `proposal/scoping/graphify-out/` ni la caché anidada
             `proposal/scoping/papers/graphify-out/cache/` — déjala intacta
             para que `graphify --update` la reutilice en `paper-1..5.md` y
             solo compute embeddings nuevos para `paper-6..N.md`.
          3. `cd proposal/scoping/` (cambio de CWD obligatorio, igual que en
             Fase 1a).
          4. `graphify --update papers/` (incremental — NUNCA `graphify
             papers/` desde cero en esta fase).
          5. `graphify export html` (obligatorio, regenera
             `proposal/scoping/graphify-out/graph.html` sobre el corpus
             ampliado).
        NUNCA uses `--force`. La salida sigue en
        `proposal/scoping/graphify-out/` (ahora refleja el corpus ampliado);
        `proposal/scoping/graphify-out-g1a-snapshot/` queda fijo como la
        foto de G1a.
        (c) Task → bibliografo-propuesta MODE=sota, sub-paso **grouping**
        (solo después de que el paso (b) complete) → propone 3-5
        subsecciones SOTA como tabla de mapeo paper → subsección →
        SP1/SP2/SP3.
        ──→ COMPUERTA COMBINADA G1b: presenta juntos, en una sola solicitud
        de aprobación:
          1. El corpus ampliado: conteo final de papers y parámetros de
             búsqueda (query, filtro de cuartil, rango de años, hits por
             herramienta) del sub-paso corpus.
          2. El grafo actualizado: la ruta del HTML interactivo
             `proposal/scoping/graphify-out/graph.html` + las 3 secciones
             del `GRAPH_REPORT.md` actualizado (God Nodes, Surprising
             Connections, Suggested Questions) sobre el corpus ampliado.
          3. La tabla de mapeo de 3-5 subsecciones SOTA (paper → subsección
             → SP1/SP2/SP3).
        Reglas de iteración por componente (NO es un rechazo en bloque):
          - Cambio solo al CORPUS → re-despacha el sub-paso corpus con el
            ajuste solicitado (repite el paso (a)) → re-ejecuta la
            actualización incremental del grafo (repite el paso (b)) →
            re-deriva la tabla de subsecciones (repite el paso (c) — el
            sub-paso grouping SIEMPRE se re-ejecuta cuando cambia el
            corpus, no es opcional ni un caso de scope creep) → vuelve a
            presentar G1b.
          - Cambio solo a la AGRUPACIÓN (subsecciones) → re-ejecuta
            únicamente el sub-paso grouping (paso (c)) con el feedback
            exacto del usuario; el corpus y el grafo quedan intactos;
            vuelve a presentar G1b.
        Regla de faltante G1b: si el bibliógrafo reporta menos de 30 papers
        Q1/Q2 dentro de la ventana de recencia aplicable, el dispatcher NO
        debe sustituir ni relajar filtros en silencio — preséntale al
        usuario, en vivo, el mismo menú de la Regla de faltante G1a, ahora
        al piso de 30:
          (a) ampliar la ventana de años,
          (b) relajar el cuartil (aceptar solo Q2 o un venue top nombrado),
          (c) ampliar/reformular los términos de búsqueda,
          (d) continuar con menos de 30,
          (e) aceptar un paper específico que el usuario nombre.
        Aplica la opción elegida y vuelve a presentar dentro de G1b.
        ──→ Al aprobar G1b: Task → bibliografo-propuesta MODE=sota, sub-paso
        **WRITE-REFS** → escribe `proposal/refs.bib` en una sola pasada
        cubriendo el corpus completo (prohibido antes de esta aprobación).
        Luego escribe el corpus aprobado + la tabla de subsecciones + G1b =
        APROBADA en `proposal/estado_propuesta.md` ("Compuertas tempranas
        (G0.5, G1a)" → sub-tabla "G1b — Corpus y subsecciones SOTA": conteo
        de papers, parámetros de búsqueda, ruta del grafo actualizado +
        extracto del reporte, tabla de mapeo de subsecciones, y Estado
        G1b).
        ──→ [NUEVO] DISPATCHER: papers-graph refresh (post-WRITE-REFS):
        guardia — ejecuta este bloque solo si `proposal/refs.bib` cambió en
        este sub-paso (WRITE-REFS lo acaba de escribir). Mecánica:
        `cd proposal/scoping/ && graphify --update papers/ && graphify
        export html`. NUNCA `--force`. La salida sigue en
        `proposal/scoping/graphify-out/`.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/11-fase1b.md` (evento de esta compuerta) y
        actualiza `proposal/pipeline/_estado.md`.
        ──→ [NUEVO] Grafo de ideas del vault — build completo (primera vez):
        inmediatamente después de lo anterior, en esta misma transición de
        aprobación final de G1b (NO en cada iteración del bucle de G1b), el
        DISPATCHER ejecuta una construcción completa de `graphify` sobre
        `vault/`. Esta corrida es DISTINTA de la del paso (b) de esta misma
        Fase 1b (que actualiza el grafo del corpus de papers de scoping en
        `proposal/scoping/graphify-out/`): esta nueva corrida indexa el
        mirror Obsidian (`vault/secciones/` + `vault/insumos/`), no el
        corpus de papers, y escribe en una raíz de salida distinta. Ver
        "Grafo de coherencia del vault" arriba para el detalle completo del
        mecanismo asesor. Mecánica exacta:
          1. `cd vault/` (cambio de CWD obligatorio — distinto del `cd
             proposal/scoping/` de la corrida del corpus SOTA; ningún grafo
             corre desde la raíz del repo).
          2. `graphify .` (build completo — baseline: en este punto
             `vault/insumos/` ya tiene notas de insumos de la Fase 0;
             `vault/secciones/` aún no tiene notas de sección, porque las
             Fases 1-7 no han corrido todavía).
          3. `graphify export html` → `vault/graphify-out/graph.html`.
          4. La salida (`graph.json`, `graph.html`, `GRAPH_REPORT.md`) queda
             en `vault/graphify-out/` — gitignored, scratch, nunca se
             commitea.
        NUNCA uses `--force`.
Fase 1  (en AMBAS rutas) Task → bibliografo-propuesta MODE=explore → mapa de
        literatura de amplitud (≥5 obras, devuelto inline al dispatcher, sin
        archivo de salida), despachado ANTES del investigador.
        Task → investigador → §3 descripción del problema (subproblemas +
        pregunta de investigación). Inyecta inline en el prompt de esta Task el mapa de MODE=explore y,
        si existe, el bloque "PRIORIDAD TDR" de la Fase 0.
        Si la Fase 1a corrió y su gate cerró con G1a = APROBADA (ver
        `proposal/estado_propuesta.md`, sub-tabla "G1a — Scoping temprano"),
        inyecta ADEMÁS, inline, el bloque "SUBPROBLEMAS TEMPRANOS APROBADOS
        (G1a)" con los 3 subproblemas tempranos y su justificación
        gap↔`paper-N`. Si la Fase 1a no corrió (o no cerró en APROBADA),
        omite por completo este bloque adicional: el despacho de esta Task
        es entonces idéntico al de hoy.
        Si además la Fase 1b corrió y su gate cerró con G1b = APROBADA (ver
        `proposal/estado_propuesta.md`, sub-tabla "G1b — Corpus y
        subsecciones SOTA"), inyecta ADEMÁS, inline, el bloque "CORPUS Y
        SUBSECCIONES APROBADAS (G1b)" con el conteo del corpus ampliado y la
        tabla de mapeo de subsecciones; si la Fase 1b no corrió (o no cerró
        en APROBADA), omite este bloque adicional y el despacho sigue el
        comportamiento previo al cambio.
        ──→ luego bucle de figura (árbol de problemas):
          Task → disenador-tikz (autor diag_arbol_problemas.tex)
          → Task → tikz-optimizer (compila a PNG, primer ajuste)
          → Task → revisor-figuras (audita, PASS/FAIL)
          → en FAIL, vuelve a Task → tikz-optimizer con los hallazgos
          → en PASS, continúa
        ──→ [NUEVO] DISPATCHER: guardia — reconstruye el grafo solo si
        `vault/secciones/03_descripcion_problema.md` cambió en esta fase
        (recién escrita/actualizada por `investigador`); si no cambió,
        reutiliza el `GRAPH_REPORT.md` existente sin re-ejecutar `graphify`.
        Si cambió: `cd vault/ && graphify --update .` (incremental, NUNCA
        `--force`, NUNCA reconstruye desde cero aquí; sin export HTML — ver
        "Vault graph HTML export limited to G1b and Fase 7") →
        `vault/graphify-out/`; lee `GRAPH_REPORT.md`; arma e inyecta inline
        el bloque `EVIDENCIA DE GRAFO` (formato en "Grafo de coherencia del
        vault" arriba) en el prompt de la Task → revisor de este gate; si
        hay hallazgo de coherencia, agrégalo a `## Hallazgos de coherencia
        (grafo)` en `proposal/estado_propuesta.md`.
        ──→ GATE Task → revisor (con bloque EVIDENCIA DE GRAFO inline) ──→ usuario. NO avances sin aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/20-fase1.md` (evento de esta compuerta) y
        actualiza `proposal/pipeline/_estado.md`.
Fase 2  Task → bibliografo-propuesta → §4 estado del arte (en paralelo)
        Task → investigador → §5 hipótesis
        ──→ [NUEVO] DISPATCHER: guardia — reconstruye el grafo solo si
        `vault/secciones/04_estado_arte.md` o `vault/secciones/05_hipotesis.md`
        cambiaron en esta fase; si no cambiaron, reutiliza el
        `GRAPH_REPORT.md` existente sin re-ejecutar `graphify`. Si cambiaron:
        `cd vault/ && graphify --update .` (sin export HTML — ver "Vault
        graph HTML export limited to G1b and Fase 7") → `vault/graphify-out/`;
        lee `GRAPH_REPORT.md`; arma e inyecta inline el bloque `EVIDENCIA DE
        GRAFO` en el prompt de la Task → revisor de este gate; si hay
        hallazgo, agrégalo a `## Hallazgos de coherencia (grafo)` en
        `proposal/estado_propuesta.md`.
        ──→ GATE Task → revisor (con bloque EVIDENCIA DE GRAFO inline) ──→ usuario. NO avances sin aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/30-fase2.md` (evento de esta compuerta) y
        actualiza `proposal/pipeline/_estado.md`.
Fase 3  Task → redactor → §2 justificación y pertinencia
        ──→ [NUEVO] DISPATCHER: guardia — reconstruye el grafo solo si
        `vault/secciones/02_justificacion.md` cambió en esta fase; si no
        cambió, reutiliza el `GRAPH_REPORT.md` existente sin re-ejecutar
        `graphify`. Si cambió: `cd vault/ && graphify --update .` (sin
        export HTML — ver "Vault graph HTML export limited to G1b and Fase
        7") → `vault/graphify-out/`; lee `GRAPH_REPORT.md`; arma e inyecta
        inline el bloque `EVIDENCIA DE GRAFO` en el prompt de la Task →
        revisor de este gate; si hay hallazgo, agrégalo a `## Hallazgos de
        coherencia (grafo)` en `proposal/estado_propuesta.md`.
        ──→ GATE Task → revisor (con bloque EVIDENCIA DE GRAFO inline) ──→ usuario. NO avances sin aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/40-fase3.md` (evento de esta compuerta) y
        actualiza `proposal/pipeline/_estado.md`.
Fase 4  Task → investigador → §6 objetivo general + §7 objetivos específicos
        ──→ [NUEVO] DISPATCHER: guardia — reconstruye el grafo solo si
        `vault/secciones/06_objetivo_general.md` o
        `vault/secciones/07_objetivos_especificos.md` cambiaron en esta
        fase; si no cambiaron, reutiliza el `GRAPH_REPORT.md` existente sin
        re-ejecutar `graphify`. Si cambiaron: `cd vault/ && graphify
        --update .` (sin export HTML — ver "Vault graph HTML export
        limited to G1b and Fase 7") → `vault/graphify-out/`; lee
        `GRAPH_REPORT.md`; arma e inyecta inline el bloque `EVIDENCIA DE
        GRAFO` en el prompt de la Task → revisor de este gate; si hay
        hallazgo, agrégalo a `## Hallazgos de coherencia (grafo)` en
        `proposal/estado_propuesta.md`.
        ──→ GATE Task → revisor (valida mapeo subproblema↔objetivo específico
        1:1; valida también hipótesis (§5, ya aprobada en la Fase 2)
        ↔objetivo general, con bloque EVIDENCIA DE GRAFO inline) ──→ usuario.
        NO avances sin aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/50-fase4.md` (evento de esta compuerta) y
        actualiza `proposal/pipeline/_estado.md`.
Fase 5  Task → investigador → §8 marco conceptual (en paralelo)
        Task → redactor → §9 equipo de trabajo (deriva roles de §7 objetivos
        específicos; nunca de la metodología)
        Task → redactor → §10 metodología, luego bucle de figuras:
          Task → disenador-tikz (autor diag_metodologico.tex)
          → Task → tikz-optimizer (compila a PNG, primer ajuste)
          → Task → revisor-figuras (audita, PASS/FAIL)
          → en FAIL, vuelve a Task → tikz-optimizer con los hallazgos
          → en PASS, continúa
        ──→ [NUEVO] DISPATCHER: guardia — reconstruye el grafo solo si
        `vault/secciones/08_marco_conceptual.md`,
        `vault/secciones/09_equipo_trabajo.md` o
        `vault/secciones/10_metodologia.md` cambiaron en esta fase; si no
        cambiaron, reutiliza el `GRAPH_REPORT.md` existente sin re-ejecutar
        `graphify`. Si cambiaron: `cd vault/ && graphify --update .` (sin
        export HTML — ver "Vault graph HTML export limited to G1b and Fase
        7") → `vault/graphify-out/`; lee `GRAPH_REPORT.md`; arma e inyecta
        inline el bloque `EVIDENCIA DE GRAFO` en el prompt de la Task →
        revisor de este gate (nota: este paso es distinto del bucle de
        figuras arriba, que usa `revisor-figuras`, no `revisor`, y no recibe
        evidencia de grafo); si hay hallazgo, agrégalo a `## Hallazgos de
        coherencia (grafo)` en `proposal/estado_propuesta.md`.
        ──→ GATE Task → revisor (con bloque EVIDENCIA DE GRAFO inline) ──→ usuario. NO avances sin aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/60-fase5.md` (evento de esta compuerta) y
        actualiza `proposal/pipeline/_estado.md`.
Fase 6  Task → redactor → §11 resultados esperados; Task → redactor →
        §12 consideraciones éticas (sin gate propio; se auditan en la Fase 7
        junto con el resto del documento, igual que antes).
Fase 6.4 [COMPUERTA INTERACTIVA G-Presupuesto] Presupuesto (interactivo).
        Precondición: §10, §11 y §12 ya aprobadas/producidas (el presupuesto
        justifica cada ítem contra la metodología, §10). El Cronograma (§14)
        todavía NO existe en este punto del pipeline —se redacta después,
        en la Fase 6.45— así que la verificación cruzada
        Presupuesto↔Cronograma queda diferida a la auditoría final de la
        Fase 7 (referencia hacia adelante válida, ver "Reglas de
        dependencia"). DEBE cerrar ANTES de la Fase 6.45 y de la Fase 6.5
        (el front-matter sintetiza §1–§16 ya aprobadas).
        ──→ RESOLUCIÓN DE MODO: si `proposal/insumos.md` (o
        `guia_ajustada_TDR.md`) trae un bloque `## Marco presupuestal (TDR)`
        con tope no vacío → MODE=tdr; si trae el sentinel `sin datos
        presupuestales en TDR` o no hay bloque → MODE=base.
        (a) Task → presupuestador (MODE=tdr | MODE=base) → primer borrador de
        `proposal/sections/13_presupuesto.tex` + su mirror de vault, con el
        self-audit aritmético ya aplicado; cada monto/cantidad no derivable de
        un insumo va marcado `[supuesto]`.
        ──→ BUCLE INTERACTIVO (sin tope de rondas; termina SOLO con
        aprobación explícita del usuario):
          1. El DISPATCHER presenta al usuario: (i) la tabla renderizada
             (ítem/cantidad/valor unitario/valor total/justificación,
             subtotales por rubro y total general); (ii) la lista de ítems
             marcados `[supuesto]`; (iii) en MODE=tdr, tope, cofinanciación
             aplicable, duración y el margen restante frente al tope.
          2. El usuario responde por línea (agregar/quitar/editar ítems,
             cantidades, valores unitarios, rubros, justificaciones) o aprueba.
          3. Si hay feedback → Task → presupuestador con las correcciones
             EXACTAS del usuario → regenera la tabla + re-corre el self-audit →
             el DISPATCHER resume los DELTAS respecto de la ronda anterior (qué
             filas/valores cambiaron y el nuevo total) y vuelve al paso 1.
             NUNCA auto-apruebes ni asumas conformidad por silencio.
          4. Si el usuario aprueba explícitamente → sale del bucle.
        ──→ [NUEVO] DISPATCHER: guardia — reconstruye el grafo solo si
        `vault/secciones/13_presupuesto.md` cambió en esta fase (o en la
        ronda interactiva más reciente); si no cambió, reutiliza el
        `GRAPH_REPORT.md` existente sin re-ejecutar `graphify`. Si cambió:
        `cd vault/ && graphify --update .` (sin export HTML — ver "Vault
        graph HTML export limited to G1b and Fase 7") →
        `vault/graphify-out/`; lee `GRAPH_REPORT.md`; arma e inyecta inline
        el bloque `EVIDENCIA DE GRAFO` en el prompt de la Task → revisor de
        este gate; si hay hallazgo, agrégalo a `## Hallazgos de coherencia
        (grafo)` en `proposal/estado_propuesta.md`.
        ──→ GATE Task → revisor (con bloque EVIDENCIA DE GRAFO inline; aplica
        el criterio de Presupuesto del checklist de `revisor.md`: recomputo
        aritmético independiente, tope/cofinanciación, justificación→§10
        (Metodología; el cruce contra §14 Cronograma se valida recién en la
        Fase 7), membresía de rubro) ──→ usuario. NO avances sin aprobación.
        ──→ Al aprobar: el DISPATCHER voltea `gate_status` a `pass` en
        `vault/secciones/13_presupuesto.md` y registra la fila de la fase en
        `proposal/estado_propuesta.md` (tabla "Presupuesto (Fase 6.4)": modo
        [tdr|base], tope [valor+moneda o "n/a (base)"], total general, margen
        frente al tope, cofinanciación/split aplicable + cumplimiento, número
        de rondas interactivas, supuestos `[supuesto]` confirmados por el
        usuario, estado del gate G-Presupuesto [APROBADA (quién/fecha) |
        pending]).
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/65-fase6_4.md` (evento de esta compuerta, misma
        plantilla mínima descrita arriba en "Grafo de pipeline") y actualiza
        `proposal/pipeline/_estado.md`.
Fase 6.45 Task → redactor → §14 cronograma de actividades (Gantt); Task →
        redactor → §15 productos esperados; Task → bibliografo-propuesta →
        §16 bibliografía (BibTeX, consolidación final MODE=deliverable
        §4+§16, cubre todas las referencias citadas a lo largo del
        documento). Sin gate propio (mismo patrón que la Fase 6: se audita
        en conjunto en la Fase 7).
        ──→ [NUEVO] DISPATCHER: papers-graph refresh: guardia — ejecuta este
        bloque solo si `proposal/refs.bib` cambió en esta fase (la
        consolidación MODE=deliverable lo acaba de extender). Mecánica: `cd
        proposal/scoping/ && graphify --update papers/ && graphify export
        html`. NUNCA `--force`. La salida sigue en
        `proposal/scoping/graphify-out/`.
Fase 6.5 Task → redactor → secciones preliminares (front-matter), como síntesis del documento completo (§1–§16 ya aprobadas), siguiendo las instrucciones de guiaProyectosIA_Agente.md (secciones preliminares): Resumen (proposal/sections/00_resumen.tex, máx. 400 palabras), Resumen ejecutivo (proposal/sections/00_resumen_ejecutivo.tex, exactamente 5 párrafos), Palabras clave (proposal/sections/00_palabras_clave.tex, 5 palabras). Mismo mirror de vault que el resto de secciones del redactor.
        ──→ GATE Task → revisor (valida las 3 preliminares contra la guía) ──→ usuario. NO avances sin aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/70-fase6.md` (cubre Fase 6 + Fase 6.45 + Fase 6.5,
        evento de esta compuerta) y actualiza `proposal/pipeline/_estado.md`.
Fase 7  ──→ [NUEVO] DISPATCHER: `cd vault/ && graphify --update .` sobre el vault
        completo (todas las secciones ya escritas) → `graphify export html`
        → `vault/graphify-out/`; lee `GRAPH_REPORT.md`; arma e inyecta
        inline el bloque `EVIDENCIA DE GRAFO` en el prompt de la Task →
        revisor de la auditoría final; si hay hallazgo, agrégalo a `##
        Hallazgos de coherencia (grafo)` en `proposal/estado_propuesta.md`.
        Task → revisor → auditoría final (con bloque EVIDENCIA DE GRAFO inline;
        incluye AHORA la verificación cruzada Presupuesto (§13) ↔ Cronograma
        de actividades (§14) diferida desde la Fase 6.4, ya que ambas
        secciones existen recién en este punto) ──→ usuario. NO avances sin
        aprobación.
        ──→ [NUEVO] DISPATCHER: pipeline-graph: escribe
        `proposal/pipeline/80-fase7.md` (evento de la auditoría final) y
        actualiza `proposal/pipeline/_estado.md`.
        Tú (el asistente primario) ensamblas `proposal/main.tex` una vez aprobado.
        Los 3 archivos `00_*.tex` (Resumen → Resumen ejecutivo → Palabras
        clave, en ese orden) DEBEN incluirse antes del contenido de §2,
        maquetados con `\section*{}`. Orden del cuerpo (`\input{sections/...}`,
        16 secciones en este orden exacto): `02_justificacion`,
        `03_descripcion_problema` (con `diag_arbol_problemas`),
        `04_estado_arte`, `05_hipotesis`, `06_objetivo_general`,
        `07_objetivos_especificos`, `08_marco_conceptual`,
        `09_equipo_trabajo`, `10_metodologia` (con `diag_metodologico`),
        `11_resultados_esperados`, `12_consideraciones_eticas`,
        `13_presupuesto`, `14_cronograma_actividades`,
        `15_productos_esperados`, y por último el bloque de bibliografía
        (`16_bibliografia` + `\bibliographystyle{apalike}` +
        `\bibliography{refs}`, §16). Nota de reordenamiento: `13_presupuesto`
        va ANTES de `14_cronograma_actividades` en el cuerpo ensamblado,
        aunque ambas secciones referencian las mismas fases de la
        Metodología (§10) — es la posición mandada por
        `guiaProyectosIA_Agente.md`, no un error de orden.
        Tras ensamblar y compilar `proposal/main.pdf` (`proposal/build.sh`),
        genera también la versión Word con `./build.sh --docx` desde
        `proposal/`: produce `proposal/main.docx` con los 3 diagramas
        rasterizados como imágenes y §13 Presupuesto como tabla editable (el
        sombreado de §13 no se conserva; el Gantt de §14 Cronograma de
        actividades queda como imagen). Es un paso mecánico
        post-compilación que corres tú (asistente primario), no un agente.
        [NUEVO] Como último paso de la Fase 7, ya con `main.pdf` ensamblado,
        corres una pasada de QA visual asesora: `pixelshot proposal/main.pdf
        -o proposal/pixelshot-out/` y revisas los tiles renderizados en busca
        de posición del logo (encabezado UNAL, pie GCPDS/LabIA), desbordes de
        tablas/Gantt, figuras TikZ rotas o ilegibles, y coherencia general de
        maquetación. Es un paso mecánico que corres tú (asistente primario),
        no un agente ni un Task nuevo — sin ronda interactiva adicional. Si
        detectas un hallazgo, agrega una fila a `## Hallazgos de QA visual
        (pixelshot)` en `proposal/estado_propuesta.md` (crea la sección la
        primera vez que se usa), con página, tipo
        (logo/desborde/TikZ-roto/otro) y detalle. Este hallazgo es puramente
        asesor: NUNCA altera el VEREDICTO PASS/FAIL de la auditoría de
        `revisor` (ya emitido antes de este paso) ni bloquea el
        ensamblado/build/cierre de la Fase 7. Si `pixelshot` no está
        disponible o falla (dependencia faltante, error de Playwright/CDP,
        timeout), registra una fila "QA visual no disponible en esta corrida:
        `<razón>`" en la misma sección y continúa — la Fase 7 se da por
        completa igual.
```

## Reglas de dependencia (haz que `revisor` las valide en cada gate)

- 3 subproblemas (§3) ↔ 3 objetivos específicos (§7), mapeo 1:1.
- Pregunta de investigación (cierre §3) ↔ objetivo general (§6).
- Hipótesis (§5) ↔ objetivo general (§6).
- Metodología (§10) ↔ objetivos específicos (§7), marco conceptual (§8) y
  equipo de trabajo (§9), cadena de valor. El punto 2 de Metodología nombra
  el enfoque/algoritmo por subproblema con razonamiento causa-efecto
  explícito referenciando el marco conceptual (§8) — función que antes
  cubría el desaparecido §5.3 Enfoques teóricos.
- Equipo de trabajo (§9) deriva sus roles de los objetivos específicos (§7);
  nunca de la Metodología (§10).
- Cronograma de actividades (§14) ↔ fases de la Metodología (§10).
- Resultados esperados (§11) ↔ productos entregados en hitos del cronograma
  (§14) — referencia hacia adelante en el pipeline (§11 se redacta en la
  Fase 6, antes de que §14 exista en la Fase 6.45); se verifica en firme en
  la auditoría final de la Fase 7.
- Presupuesto (§13) ↔ Metodología (§10) y Cronograma (§14) — misma
  referencia hacia adelante, verificada en firme en la Fase 7.
- TRL 6 o 7 debe ser explícito en pertinencia (§2) y resultados esperados
  (§11); **nunca** se nombra en objetivo general (§6) ni en objetivos
  específicos (§7).

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
- En FAIL, vuelve a despachar con `task` al agente responsable de la sección
  con las correcciones exactas del revisor, y repite el gate.
- No reescribas contenido de sección tú mismo; ese trabajo es de los
  subagentes especialistas.
- Tras el veredicto PASS de cada gate, actualiza tú (el dispatcher) el campo
  `gate_status` de `pending` a `pass` en el frontmatter de la(s) nota(s)
  `vault/secciones/*.md` correspondientes a esa fase — el `revisor` solo tiene
  herramientas de lectura (Read/Grep/Glob) y no puede escribir archivos, así
  que esta responsabilidad es tuya, igual que ya lo es para
  `proposal/estado_propuesta.md`. En FAIL, deja `gate_status` en `pending` (o
  cámbialo a `fail` si el re-despacho vuelve a fallar) hasta que el
  re-despacho apruebe.

Comienza ahora confirmando la idea del usuario y listando los insumos
detectados, luego arranca la Fase 0 despachando `insumos-observador` con
`task`.
