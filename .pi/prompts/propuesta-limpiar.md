---
description: Archiva la corrida activa de /propuesta (si existe) y deja proposal/ y vault/ limpios para una corrida nueva, sin tener que arrancar /propuesta primero.
---

# /propuesta-limpiar — Archivar y resetear la corrida activa

Ejecuta, de forma standalone, el mismo procedimiento de archivado que
`propuesta.md` (Fase 0, bloque "GUARDIA DE COLISIÓN" / "ARCHIVADO-Y-REINICIO")
ya dispara automáticamente cuando detecta una corrida sin terminar — pero
invocable directamente, sin necesidad de arrancar una corrida nueva primero.
Fuente de verdad del procedimiento de archivado: ese bloque en `propuesta.md`.
Este comando no lo duplica; lo ejecuta.

## Qué hacés vos (el asistente primario) al recibir este comando

1. **Lee `proposal/estado_propuesta.md`.** Si el archivo no existe, no tiene
   bloque "## Identidad de la corrida (run-id)", o su campo `estado` no es
   `activa`, NO hay nada que limpiar — respondé "No hay ninguna corrida
   activa; el árbol ya está listo para una corrida nueva" y DETENÉTE sin
   tocar ningún archivo.

2. **Si hay una corrida activa**, mostrale al usuario, antes de tocar nada:
   `run_id`, fecha de creación, qué compuertas están cerradas (PASS/APROBADA)
   vs. pendientes (lee `## Compuertas tempranas` y las secciones de gate de
   `proposal/estado_propuesta.md`), y cuántos archivos de sección existen en
   `proposal/sections/*.tex`. Preguntá explícitamente: "Esto va a archivar
   la corrida `<run_id>` en `proposals/<run_id>/` y vaciar el árbol activo
   para una corrida nueva. ¿Confirmás? (sí/no)". NO continúes sin un "sí"
   explícito — el archivado en sí nunca borra contenido (todo queda
   preservado en `proposals/<run_id>/`), pero el árbol activo sí se vacía, y
   eso requiere confirmación previa.

3. **Tras la confirmación**, releé el bloque "ARCHIVADO-Y-REINICIO" completo
   de `propuesta.md` (Fase 0) y ejecutá sus 6 pasos exactamente como están
   escritos ahí: (1) leer el `run_id` previo; (2) copiar el contenido de
   `proposal/` y `vault/` a `proposals/<run-id-previo>/proposal/` y
   `proposals/<run-id-previo>/vault/` — **solo local**, `proposals/*/` está
   en `.gitignore`, ese contenido nunca se sincroniza con GitHub; (3)
   escribir `proposals/<run-id-previo>/run.md` (manifiesto: run-id, idea,
   fechas, estado final de cada compuerta, conteo de referencias) y marcar la
   fila correspondiente de `proposals/registry.md` como `archivada`
   (completar `cerrada` y `archivo`, ruta local); (4) commit **solo** de
   `proposals/registry.md` — nunca del contenido archivado, que queda
   gitignored — `chore(proposals): record archive of run <run-id-previo>`;
   sin `git add -f`/force-add de nada bajo `proposals/<run-id-previo>/`; (5)
   resetear `proposal/` y `vault/` a exactamente el estado de un clon nuevo
   del repo más las carpetas vacías de trabajo — no solo los 3 directorios
   de contenido, también todo build auxiliar y residuo de la corrida
   cerrada (main.pdf/.docx/.tex y build de LaTeX, `guia_ajustada_TDR.md`,
   `pixelshot-out/`, snapshots de grafo, `__pycache__/`), aunque ya estén
   gitignored — es limpieza de disco, no de git; ver la lista exacta en el
   paso 5 de `propuesta.md`. El paso (6) del bloque original ("continuar con
   el nuevo run-id") no aplica acá: este comando termina en el paso (5) — el
   nuevo run-id se resuelve recién cuando el usuario arranque `/propuesta`
   de nuevo.

4. **Al terminar**, confirmá al usuario: la ruta local donde quedó
   archivada la corrida (`proposals/<run_id>/`, solo en disco, no en
   GitHub), que el commit de `proposals/registry.md` se hizo (mostrale el
   hash), y que el árbol activo (`proposal/`, `vault/`) quedó vacío —sin
   residuos de build ni cachés— y listo. Sugerile correr `/propuesta` cuando
   quiera arrancar la corrida nueva.

## Qué nunca hace este comando

- Nunca borra `proposals/<run_id>/` una vez archivado — el archivo queda
  permanente en el disco local (nunca en GitHub: `proposals/*/` está
  gitignored a propósito).
- Nunca hace `git add -f`/force-add de contenido de la propuesta (activa o
  archivada) para meterlo en git — solo `proposals/registry.md` se versiona.
- Nunca toca `proposal/build.sh`, `proposal/scripts/*.py`,
  `proposal/logos/`, `proposal/templates/`, `guiaProyectosIA_Agente.md`, ni
  ningún archivo fuera de `proposal/`, `vault/` y `proposals/registry.md`.
- Nunca hace `git push` — el commit de `proposals/registry.md` queda local
  hasta que el usuario decida pushearlo explícitamente.
- Nunca se ejecuta sin la confirmación explícita del paso 2.
