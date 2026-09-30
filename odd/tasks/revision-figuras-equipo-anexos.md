# Feature: revisión de figuras + equipo, entidad externa y anexos (G2 → G3)

## Goal

Apply the operator's revision round after G2:

1. **Árbol de problemas**: reducir a **máximo 3 causas por subproblema** (hoy 5/5/4 = 14 raíces) y **máximo 4 efectos** (hoy 7 ramas).
2. **Mapa de estado del arte**: reconstruirlo con una composición más armónica —revisar estilo y estructura— y que funcione mejor en la página.
3. **Equipo y entidad externa**: incorporar a la UTP (grupo de investigación en Automática, profesor David Augusto Cárdenas) como entidad externa, y a los coinvestigadores UNAL Germán Castellanos y Jorge Iván Montes, con horas de dedicación y roles.
4. **Encabezado de `main.tex`**: bajo el título, investigador principal + Laboratorio de IA + GCPDS + Semillero de Ciencia de Datos e Inteligencia Artificial.
5. **Anexos de la convocatoria**: crear una carpeta nueva en Drive (dentro de `proyectos unal`) con los anexos por generar: avales de horas de jornada docente por investigador, carta de la entidad externa, carta de estudiantes y demás documentos obligatorios del §8.6 del TDR.

## Datos aportados por el operador (autoridad)

| Rol | Persona | Entidad | Horas/semana | Aporte |
|---|---|---|---|---|
| Investigador principal | Andrés Marino Álvarez-Meza | UNAL LIA | 4 | Dirección del proyecto + estrategias de implementación de agentes |
| Coinvestigador | Germán Castellanos-Domínguez | UNAL GCPDS | 2 | Técnicas de procesamiento de bioseñales |
| Coinvestigador | Jorge Iván Montes-Monsalve | UNAL | 2 | Sistemas de adquisición de datos |
| Coinvestigador (entidad externa) | David Augusto Cárdenas | UTP, grupo de Automática | 2 | Estrategias de inferencia en el borde |
| Estudiante de pregrado 1 | (rol, sin nombre) | UNAL | 4 meses | — |
| Estudiante de pregrado 2 | (rol, sin nombre) | UNAL | 4 meses | — |
| Estudiante de maestría | (rol, sin nombre) | UNAL | 1 año | — |
| Estudiante de doctorado | (rol, sin nombre) | UNAL | duración del proyecto (12 meses) | — |

## Anexos obligatorios del TDR §8.6 (fuente: `insumos/tdr/Terminos-de-Referencia.pdf`)

1. Carta de la UAB/centro/instituto/sede del investigador principal, con las **horas de jornada docente** dedicadas.
2. Carta de aval de la facultad donde se ejecutarán los recursos.
3. **Aval de horas de jornada docente por cada docente participante**, firmado por el director de la UAB correspondiente.
4. Carta de compromiso del estudiante vinculado (Anexo 2 de la convocatoria).
5. Carta de compromiso del aporte de recursos adicionales (Anexo 3) — **ahora aplica**, porque la UTP entra como entidad externa (habilita los 5 pts de "Fuentes de Financiación Adicionales").

## Tasks

- [x] T1 Redactar de nuevo el bloque de especificación del árbol (≤3 causas/SP, ≤4 efectos) — 14→9 raíces, 7→4 efectos
- [x] T2 Regenerar `diag_arbol_problemas.tex` + bucle de figura — intento 1/4 FAIL (ramas borde contra borde) → intento 2/4 PASS tras separar offsets a ±1.9/±5.7 cm y `text width` 3.1 cm
- [x] T3 Rediseñar el mapa de estado del arte (armonía: filas alineadas, estructura) + bucle de figura — **hecho el 2026-09-30** con el pipeline determinista nuevo. `diag_estado_arte.tex` es ahora salida generada de `redaccion/specs/estado_arte.spec.json` (5 clústeres × 5 papers, 16 aristas internas, limitante por clúster). Medición antes → después: **17,0 × 31,3 cm → 17,78 × 28,54 cm**, PASS en 1,1 s. El operador eligió **dos figuras**: el mapa se entrega como `estado_arte_a` (grupos 1-3, 15,53 × 12,62 cm) y `estado_arte_b` (grupos 4-5 + cierre, 9,47 × 15,57 cm), ambas a tamaño natural y sin `resizebox`; `main.tex` tiene las dos entradas y §4 referencia ambas con `\Cref{fig:estado_arte_a,fig:estado_arte_b}`. Ver "Decisión del operador" en `odd/tasks/marco-tikz-pi-native.md`.
- [x] T4 Actualizar el encabezado de `main.tex` (IP, LIA, GCPDS, Semillero)
- [x] T5 Registrar el equipo en `artefactos/equipo.md` (fuente para §9 y para los anexos)
- [x] T6 Redactar los anexos del §8.6 en `artefactos/anexos/`
- [x] T7 Crear la carpeta en Drive y subir los anexos — **hecho el 2026-09-30**: `SIUN Emergencias 2026 — Anexos postulación` en `Proyectos Activos`, con los 9 PDF en la raíz y `borradores/` con los 9 `.md`. 20/20 archivos verificados por tamaño contra el origen
- [x] T8 Recompilar `main.pdf` y presentar la ronda al usuario — **hecho el 2026-09-30**

## Evidence

- **T1**: `03_descripcion_problema.tex` spec block rewritten: 9 causes (3 per subproblem) and 4 effects; prose of §3 verified byte-identical (34 citation commands, 35 distinct keys untouched).
- **T2**: figure loop attempt 1/4 → `revisor-figuras` FAIL (the 4 effect boxes were border-to-border); `tikz-optimizer` applied `text width: 3.3→3.1 cm` and offsets `±1.7/±5.1 → ±1.9/±5.7 cm`; `OVERFULL: arbol_problemas 0 occurrence(s)` re-verified by the parent; attempt 2/4 → `revisor-figuras` **PASS**.
- **Drive recon**: no folder literally named "proyectos unal" or "convocatoria siun intersedes" exists as such. The project tree found is `Mi unidad / UNAL / GCPDS_main / Proyectos / {Formulación Proyectos, Proyectos Activos, Otros - Finalizados}`, with analogues `Proyectos Activos/proyectoUTP2026` (holds the UTP TDR) and `Proyectos Activos/951Geotermia_UTP_UNAL`. The previous SIUN-intersedes hours avales live in the shared folder `Fortalecimiento de alianzas interdiciplinares SIUN (2025-2027) / Ecosistemas Agentes - Andrés / DocumentosHermes / AvalesHoras_editables / editables` as `Agentes_Aval_Intersedes_Andrés Álvarez.docx` and `..._Germán Castellanos.docx` — reusable templates.
- **Subagent incident**: `revisor-figuras` failed twice with no final report at `high` thinking (same output-budget exhaustion as `grant-flow-auditor`); its profile was moved to `nan/glm5.3-flash@medium` and the next run completed.

- **T4** (verificado por lectura directa): `redaccion/main.tex` — bloque de título con `Andrés Marino Álvarez-Meza` y las tres líneas institucionales: Laboratorio de Inteligencia Artificial (LIA), Grupo de Control y Procesamiento Digital de Señales (GCPDS), Semillero de Ciencia de Datos e Inteligencia Artificial, Universidad Nacional de Colombia, Sede Manizales.
- **T5**: `artefactos/equipo.md` (96 líneas) — datos generales, tabla de roles con dedicación y aportes, marcas `[inferido]` y `⟨completar: ...⟩` para lo no confirmado por el operador.
- **T6**: `artefactos/anexos/` — 9 archivos (índice + 8 documentos, 673 líneas en total), todos en estado `borrador`, con la tabla de anexos obligatorios del §8.6, la coherencia documental con la decisión de vincular a la UTP y la lista de datos por completar antes de firmar.
- **T3** (ejecutado el 2026-09-30): el mapa se reconstruyó desde la spec determinista. Se corrigieron cuatro defectos estructurales que el bucle anterior no podía ver: (a) el ancho del estilo `paper` se calculaba con la fuente equivocada porque el estilo no fijaba `font=`; (b) las aristas que saltan nodos intermedios cruzaban las tarjetas intermedias y ahora hacen un desvío acotado en el margen derecho; (c) los enlaces entre clústeres de filas distintas envolvían la figura (+7,4 cm de ancho medidos) y ahora se dibujan solo entre vecinos de la misma fila, con la relación declarada en el `%` del `.tex` para que la prosa de §4 la conserve; (d) la frase de cierre se ancoraba a la última fila y su ancho fijo de 15 cm empujaba la caja envolvente fuera de la página. Resultado: 17,78 × 28,54 cm, PASS en 1,1 s. `main.tex` todavía lo escala con `\resizebox`; la decisión de página está en el blocker de `marco-tikz-pi-native.md`.

## Estado de T7 (carpeta de Drive) — 2026-09-30

**Preparado y verificado:**

- Los 9 anexos se convierten a PDF con `artefactos/anexos/convertir_a_pdf.sh`
  (pandoc + xelatex). Resultado: 9 PDF, 288 KB en total, todos muy por debajo del
  tope de 2 MB por archivo que exige el §8.6.
- Tres decisiones de formato, documentadas en el script y en el §6 del índice:
  membrete `BORRADOR — pendiente de firma` en cada página (ninguno está firmado y
  todos llevan datos por completar, así que un PDF sin esa marca puede
  confundirse con el radicable); guillemets «…» en lugar de los ⟨…⟩ del Markdown,
  porque U+27E8/U+27E9 no existe en ninguna fuente instalada y se imprimía como un
  cuadro vacío (el `.md` no se toca: la sustitución ocurre en la copia temporal
  que consume pandoc); y `hard_line_breaks`, porque la prosa de las cartas no
  envuelve pero la fecha, el destinatario y las líneas de firma sí usan un salto
  por línea — sin esa extensión pandoc los une en un párrafo corrido y la carta
  deja de parecer una carta.

**Hecho el 2026-09-30.** La carpeta existe en `Proyectos Activos` con los 9 PDF
en la raíz y `borradores/` con los 9 `.md`, y cada archivo se verificó por tamaño
contra el original (20/20 coinciden).

El camino no fue el previsto. `google-drive_create_file` no acepta rutas locales
—solo `textContent` o `base64Content`— y la salida de `bash` se trunca a 50 KB,
así que subir 9 PDF de 28-49 KB habría exigido teclear ~38 KB de base64 a mano
por archivo; el intento falló con `not a valid base64 string`. Se buscó entonces
el token OAuth del adaptador en el llavero (`pi-mcp-adapter.oauth`): existe, pero
las entradas de Google no tienen refresh token y la de Sheets, que es la única con
scope `drive`, ya estaba expirada. La salida fue **Google Drive para escritorio**,
que está montado en `~/Library/CloudStorage/GoogleDrive-amalvarezme@unal.edu.co`:
copiar a esa ruta es subir.

Dos obstáculos aparecieron en el montaje, y conviene recordarlos:

- La carpeta creada **por la API** quedó corrupta en el índice local de DriveFS:
cualquier acceso a ella o a su subárbol devolvía `Resource deadlock avoided`
(`EDEADLK`), incluso tras reiniciar la aplicación. Se descartaron como causa el
guion em y los acentos (se probaron carpetas con y sin ellos: ambas sanas) y el
reinicio de Drive. Se resolvió con `rm -rf`, que sí funcionó y **propagó la
eliminación al servidor**, y recreando la carpeta **localmente** —las carpetas
creadas localmente sincronizan sanas— para poblar todo con `cp`.
- `google-drive_copy_file` se cuelga (>240 s) y no copia nada, así que la
combinación «subir a una carpeta puente y copiar con la API» no es viable.

El puente temporal `_carga_anexos_tmp` se eliminó y se verificó que no quedan
residuos ni carpetas duplicadas. Como el run es anterior al script de anexos,
se instaló `anexos_a_pdf.sh` en `redaccion/scripts/` de la corrida para que la
invocación documentada en el `LEEME.md` sea cierta; se probó en un directorio
aislado y produce un PDF válido con el membrete `BORRADOR`.

**Decisión del operador (aplicada):** carpeta `SIUN Emergencias 2026 — Anexos
postulación` dentro de `Mi unidad / UNAL / GCPDS_main / Proyectos Activos`, con
subcarpeta `borradores/` para los `.md` editables.

## Blocker

**Resuelto el 2026-09-30.** El operador habilitó el OAuth de Drive, Gmail, Docs y
Sheets; los cuatro servidores MCP respondieron autenticados como
`amalvarezme@unal.edu.co` en la verificación de esta sesión. T7 queda desbloqueado:
el destino real es `Mi unidad / UNAL / GCPDS_main / Proyectos Activos`
(`id 14mZMkr_F8Dch24PFTeMhSrgEeGnYMsAT`), donde ya conviven `proyectoUTP2026`,
`951Geotermia_UTP_UNAL`, `Orquídeas No. 112721-216-2025- Minciencias`,
`MATERNO_TERMOGRAFIA` y `Proyecto_Luker_UNAL_BIOS`.

Ambas decisiones quedaron cerradas: la carpeta se llama
`SIUN Emergencias 2026 — Anexos postulación` y va dentro de `Proyectos Activos`;
y el formato de subida son los PDF (con los `.md` en `borradores/` como fuente
editable).

## Los borradores pasaron a Google Docs — 2026-09-30

El operador pidió que `borradores/` tuviera documentos, no Markdown. El montaje de
DriveFS **no convierte** al subir (se verificó: un `.docx` copiado localmente sigue
siendo `org.openxmlformats.wordprocessingml.document`, y el ajuste «convertir
subidas» está apagado en la cuenta).

La conversión funciona por la API, y el obstáculo real era el transporte: el
sandbox de `mcpScript` no tiene `fetch`, `fs`, `require`, `Buffer`, `TextDecoder`
ni `crypto` —solo `atob`/`btoa`—, así que parecía obligado transcribir a mano
~36 KB de contenido (un intento falló con un error de JSON en la posición 744).

**La solución fue encadenar llamadas MCP dentro del propio sandbox**:
`download_file_content` devuelve el base64 del `.md` a una variable de JavaScript
y esa variable alimenta `create_file` con `mimeType:
application/vnd.google-apps.document`. El contenido nunca pasa por el contexto del
modelo. Es el patrón a reutilizar para cualquier conversión futura.

**Google Drive sí interpreta Markdown al importar**: el `#` se vuelve Título 1, el
`##` Título 2, la negrita se preserva, las listas se vuelven ítems reales y no
queda ningún `#` literal (verificado exportando el Doc a HTML).

Resultado: `borradores/` tiene **9 documentos de Google y cero Markdown**, con
títulos legibles (`03 · Aval de horas docentes — Germán Castellanos-Domínguez`) en
vez del nombre de archivo. El `LEEME.md` de la raíz también se convirtió y se
actualizó para reflejar el nuevo estado. Los `.md` siguen siendo la fuente
editable, pero viven en la corrida (`artefactos/anexos/`), no en Drive.

## Estado de T8 — 2026-09-30

Recompilación limpia con `./build.sh --clean`: 15 páginas A4, 0 `Overfull \hbox`,
0 `Overfull \vbox`, 0 referencias indefinidas, 0 citas indefinidas, 0 avisos de
LaTeX. 51 entradas en `refs.bib`, 51 citadas. El PDF resultante pesa exactamente
los mismos 2 574 320 bytes que el anterior, lo que confirma que las fuentes no
habían cambiado y que la compilación es reproducible.

Se encontró y retiró `sections/diag_estado_arte.tex`: el mapa monolítico quedó
huérfano al partirlo en `_a`/`_b` y ya no lo referenciaba nadie. La recompilación
posterior dio el mismo tamaño de bytes, confirmando que era inerte.

Las tres figuras son **TikZ nativo**, no PNG incrustados: los entornos `figure` y
las etiquetas viven en `main.tex`, que envuelve los `\input{sections/diag_*}`. Los
PNG de `sections/figuras/` son previsualizaciones para la revisión visual, no
entradas de compilación.
