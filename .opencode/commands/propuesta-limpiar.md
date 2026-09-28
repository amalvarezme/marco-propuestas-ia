---
description: Cierra la corrida activa de /propuesta. Con el layout por corrida es un cambio de estado; en el layout heredado de la raíz archiva y resetea el árbol.
---

# /propuesta-limpiar — Cerrar la corrida activa

Deja el repo listo para arrancar una corrida nueva, sin tener que lanzar
`/propuesta` primero. Hace una de **dos cosas distintas** según el layout de la
corrida activa, así que lo primero es decidir cuál aplica.

## Paso 0 — Determiná el layout

Leé `proposals/.current-run`:

- **Existe** → layout por corrida (`proposals/<run-id>/` con `insumos/`,
  `artefactos/`, `grafos/`, `redaccion/`). Seguí la **Vía A**.
- **No existe**, pero la raíz del repo tiene un `proposal/estado_propuesta.md`
  con `estado: activa` → layout heredado (árbol plano `proposal/` + `vault/`
  en la raíz). Seguí la **Vía B**.
- **Ninguno de los dos** → no hay nada que cerrar. Respondé "No hay ninguna
  corrida activa; podés arrancar una nueva con `/propuesta-init <idea>`" y
  DETENÉTE sin tocar ningún archivo.

---

## Vía A — Layout por corrida (cierre por cambio de estado)

Acá **no se copia ni se borra contenido**: la carpeta de la corrida ya es el
archivo permanente, con su `main.pdf`/`main.docx` y todos sus artefactos
dentro. Cerrar es marcarla como terminada.

1. **Mostrale al usuario, antes de tocar nada**: `run_id`, fecha de creación,
   qué compuertas están cerradas vs. pendientes (leé
   `proposals/<run-id>/artefactos/estado_propuesta.md`), cuántas secciones hay
   en `proposals/<run-id>/redaccion/sections/*.tex`, y si existe
   `redaccion/main.pdf`. Preguntá explícitamente: "Esto va a cerrar la corrida
   `<run_id>` como `archivada`. Su carpeta `proposals/<run_id>/` queda intacta
   con todo su contenido. ¿Confirmás? (sí/no)". NO continúes sin un "sí"
   explícito.

2. **Tras la confirmación**, ejecutá exactamente estos cuatro pasos (los
   mismos de "CIERRE DE LA CORRIDA PREVIA" en `propuesta.md`, Fase 0 — ese
   bloque es la fuente de verdad):
   1. En `proposals/<run-id>/_run.md`: `estado: archivada` y
      `cerrada: <YYYY-MM-DD>`.
   2. En `proposals/registry.md`: misma fila a `archivada`, con `cerrada` y
      `archivo` (ruta local `proposals/<run-id>/`, nunca una URL de GitHub).
   3. `delete_project("<run-id>-papers")` y `delete_project("<run-id>-vault")`
      para no dejar índices de `codebase-memory` huérfanos.
   4. Commit **solo** de `proposals/registry.md`:
      `chore(proposals): record archive of run <run-id>`. Sin `git add -f` de
      nada bajo `proposals/<run-id>/`.

3. **Borrá el puntero** `proposals/.current-run` (ya no hay corrida activa).

4. **Confirmá**: la corrida quedó archivada en `proposals/<run_id>/` (intacta,
   solo en disco local), el hash del commit del registro, y que el siguiente
   paso es `/propuesta-init <idea>` para la corrida nueva.

---

## Vía B — Layout heredado (archivar el árbol plano de la raíz)

Solo para corridas anteriores a las subcarpetas por corrida. Acá sí hay copia y
reseteo, porque el contenido vive en el árbol compartido de la raíz.

1. **Mostrale al usuario, antes de tocar nada**: `run_id`, fecha de creación,
   compuertas cerradas vs. pendientes (leé `proposal/estado_propuesta.md`), y
   cuántos archivos de sección existen en `proposal/sections/*.tex`. Preguntá
   explícitamente: "Esto va a archivar la corrida heredada `<run_id>` en
   `proposals/<run_id>/` y vaciar el árbol activo de la raíz. ¿Confirmás?
   (sí/no)". NO continúes sin un "sí" explícito — el archivado no borra
   contenido (todo queda preservado en `proposals/<run_id>/`), pero el árbol
   de la raíz sí se vacía.

2. **Tras la confirmación**, ejecutá estos pasos:
   1. Leé el `run_id` de `proposal/estado_propuesta.md`.
   2. `mkdir -p proposals/<run_id>/`; copiá `proposal/` y `vault/` a
      `proposals/<run_id>/proposal/` y `proposals/<run_id>/vault/`. Es una
      copia **solo local**: `proposals/*/` está en `.gitignore` y ese
      contenido nunca se sincroniza con GitHub.
   3. Escribí `proposals/<run_id>/_run.md` (manifiesto: run-id, idea, fechas,
      estado final de cada compuerta, conteo de referencias) y marcá la fila de
      `proposals/registry.md` como `archivada`, completando `cerrada` y
      `archivo` (ruta local).
   4. `delete_project("<run_id>-papers")` y `delete_project("<run_id>-vault")`
      si esa corrida dejó índices de `codebase-memory`.
   5. Commit **solo** de `proposals/registry.md`:
      `chore(proposals): record archive of run <run_id>`. Sin `git add -f` de
      nada bajo `proposals/<run_id>/`.
   6. Reseteá el árbol de la raíz al estado de un clon nuevo: vaciá
      `proposal/sections/`, `proposal/scoping/papers/`, `proposal/pipeline/`,
      `vault/secciones/`, `vault/insumos/` (conservando sus `.gitkeep`);
      reescribí vacíos `proposal/estado_propuesta.md`, `proposal/refs.bib`,
      `proposal/insumos.md`; borrá `proposal/guia_ajustada_TDR.md`,
      `proposal/main.tex/.pdf/.docx` y todo build auxiliar de LaTeX
      (`main.aux/.bbl/.blg/.fdb_latexmk/.fls/.log/.out/.synctex.gz`),
      `proposal/pixelshot-out/`, los reportes de grafo heredados y
      `proposal/scripts/__pycache__/`. Es limpieza de disco, no de git: hay
      que borrarlos aunque ya estén gitignored. **Conservá siempre**
      `proposal/build.sh`, `proposal/scripts/*.py`, `proposal/logos/`,
      `proposal/templates/`, y nunca toques `vault/.obsidian/`.

3. **Confirmá**: dónde quedó archivada la corrida
   (`proposals/<run_id>/`, solo en disco), el hash del commit del registro, que
   el árbol de la raíz quedó vacío sin residuos de build, y que la corrida
   nueva ya no usa ese árbol: arranca con `/propuesta-init <idea>`, que crea su
   propia carpeta de proyecto.

---

## Qué nunca hace este comando, en ninguna de las dos vías

- Nunca borra `proposals/<run_id>/` una vez archivado — el archivo queda
  permanente en el disco local (nunca en GitHub: `proposals/*/` está
  gitignored a propósito).
- Nunca hace `git add -f`/force-add de contenido de la propuesta (activa o
  archivada) para meterlo en git — solo `proposals/registry.md` se versiona.
- Nunca toca el esqueleto del framework (`proposal/build.sh`,
  `proposal/scripts/*.py`, `proposal/logos/`, `proposal/templates/`),
  `guiaProyectosIA_Agente.md`, ni ningún archivo fuera de la corrida que está
  cerrando y `proposals/registry.md`.
- Nunca hace `git push` — el commit de `proposals/registry.md` queda local
  hasta que el usuario decida pushearlo explícitamente.
- Nunca se ejecuta sin la confirmación explícita del paso 1 de su vía.
