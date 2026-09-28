---
description: Crea la carpeta de proyecto de una corrida nueva de /propuesta (proposals/<run-id>/ con docs, artefactos, grafos y redaccion) y la deja activa.
argument-hint: [idea breve de la propuesta] | run-id=<valor> [idea breve]
---

# /propuesta-init — Crear la carpeta de proyecto de una corrida

Crea **una sola carpeta de proyecto por corrida** —`proposals/<run-id>/`— con
sus artefactos repartidos en exactamente cuatro subcarpetas. Nada de la corrida
queda suelto fuera de ahí, y archivarla deja de ser una copia: la carpeta ya
**es** el archivo.

Entrada del usuario:

$ARGUMENTS

## Qué hacés vos (el asistente primario) al recibir este comando

1. **Resolvé el run-id.** Esquema `<YYYY-MM>-<slug>` (p. ej.
   `2026-09-siun-alianzas`): `<YYYY-MM>` de la fecha del sistema, `<slug>` =
   2-4 palabras clave en kebab-case, minúsculas, ASCII-folded (sin tildes ni
   ñ), derivadas de la idea en `$ARGUMENTS` descartando stopwords. Override:
   si `$ARGUMENTS` empieza con `run-id=<valor>` o `--run-id <valor>`, validá
   `<valor>` contra `[a-z0-9-]+` y usalo tal cual (el resto es la idea).
   Es el mismo esquema que la "RESOLUCIÓN DE RUN-ID" de `propuesta.md`, Fase 0.

2. **Guardia de corrida activa.** Leé `proposals/.current-run` (si existe) y
   el `_run.md` de esa corrida. Si hay una corrida con `estado: activa`
   distinta de la que se va a crear, **DETENETE** y preguntá explícitamente:
   "Existe la corrida activa `<run-id-activo>` (última compuerta `<Gx>`).
   ¿Cerrarla como `archivada` y activar `<run-id-nuevo>`? (sí/no)". Solo "sí"
   continúa; con "no", ofrecé reanudar la corrida existente. Cerrarla es
   únicamente editar su `_run.md` (`estado: archivada`, `cerrada:
   <YYYY-MM-DD>`) y su fila en `proposals/registry.md` — **nunca** se copia ni
   se borra contenido: la carpeta de esa corrida ya lo conserva todo.
   Si además existe una corrida heredada en la raíz del repo (`proposal/` y
   `vault/` planos, esquema previo a las subcarpetas por corrida), no la
   toques: avisá que quedó ahí y que `/propuesta-limpiar` es el camino para
   archivarla.

3. **Creá la carpeta con el script determinista** (no lo hagas a mano, no
   reimplementes el scaffolding):

   ```bash
   scripts/init-run.sh <run-id> "<idea breve>"
   ```

   El script es idempotente: sobre una carpeta existente crea solo lo que
   falta y nunca trunca un archivo ya escrito. Crea:

   ```
   proposals/<run-id>/
     _run.md                      # único archivo en la raíz: manifiesto de la corrida
     insumos/                        # INSUMOS DEL USUARIO: TDR, papers, propuestas base
     artefactos/                  # todo lo generado que no es fuente LaTeX
       estado_propuesta.md        #   estado del pipeline y de cada compuerta
       insumos.md                 #   insumos estructurados por insumos-observador
       pipeline/                  #   log de fases/compuertas (+ _estado.md)
       scoping/papers/            #   corpus de papers del scoping (G1a/G1b)
       vault/                     #   espejo Obsidian: secciones/, insumos/, .cbmignore
     grafos/                      # reportes de codebase-memory (papers y vault)
     redaccion/                   # el proyecto LaTeX
       sections/  refs.bib        #   fuentes de la propuesta
       build.sh  scripts/  logos/  templates/   # copiados del esqueleto del framework
   ```

   `main.tex`, `main.pdf` y `main.docx` aparecen en `redaccion/` cuando el
   pipeline los genera (Fase 7 y cada compilación de compuerta).

   El script además activa la corrida escribiendo el run-id en
   `proposals/.current-run` (el puntero que el dispatcher lee para resolver
   `RUN_ROOT`) y agrega una fila a `proposals/registry.md`.

4. **Llevá los insumos a `insumos/`.** Si el usuario ya dejó archivos en el
   `info_data/` de la raíz o los mencionó en el mensaje, preguntá si los
   copiás (`cp`, no `mv`, salvo que pida moverlos) a
   `proposals/<run-id>/insumos/`. Los insumos de una corrida viven dentro de su
   corrida; `insumos/` es la única subcarpeta que llena el usuario.

5. **Commit del registro, nada más.** `proposals/*/` está en `.gitignore`: el
   contenido de la corrida nunca se sincroniza con GitHub. Commiteá
   únicamente `proposals/registry.md`:
   `chore(proposals): register run <run-id>`. Nunca uses `git add -f` sobre
   nada bajo `proposals/<run-id>/`.

6. **Cerrá informando**: run-id, `RUN_ROOT`, las cuatro subcarpetas, los dos
   nombres de índice de `codebase-memory` que usará la corrida
   (`<run-id>-papers` sobre `artefactos/scoping/papers`, `<run-id>-vault`
   sobre `artefactos/vault`) y el siguiente paso literal: dejar los insumos en
   `proposals/<run-id>/insumos/` y correr `/propuesta <idea>`.

## Qué NO hace este comando

- No despacha ningún subagente ni arranca el pipeline. Eso es `/propuesta`.
- No borra ni copia contenido de corridas anteriores. Archivar es un cambio de
  estado en `_run.md` + `registry.md`.
- No crea índices de `codebase-memory`. Los crea el dispatcher en las Fases
  1a/1b, con `repo_path` absoluto al corpus (ver "Cómo usar `codebase-memory`"
  en `propuesta.md`).
