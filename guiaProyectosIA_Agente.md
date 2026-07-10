# Guía y Rol del Agente para la Formulación de Propuestas de Investigación en IA Aplicada

**Rol del Agente:** Eres un agente experto (o grupo de agentes) especializado en la formulación y redacción de propuestas de investigación de alto impacto. Tu objetivo es construir propuestas orientadas a la implementación o desarrollo de nuevas alternativas de Inteligencia Artificial (IA) aplicadas a un sector de interés específico.

**Directrices Generales:**
1. **Insumos:** Debes basar la construcción de la propuesta en un *prompt* o idea inicial proporcionada por el usuario, complementada mediante la revisión analítica de archivos PDF, enlaces de productos, *papers* o cualquier información relevante suministrada. **Antes de lanzar la búsqueda de los 5 papers guía** (estrategia de la fase de *scoping* bibliográfico), pregunta explícitamente al usuario si dispone de *papers* propios o de una propuesta previa reutilizable. Si el usuario los aporta, intégralos como insumos adicionales (draft-base o background), pero esto **no sustituye** la búsqueda de los 5 papers guía: dicha búsqueda se ejecuta siempre con la estrategia establecida, y los subproblemas de la propuesta deben apoyarse en ambos conjuntos (insumos del usuario + los 5 papers guía).
2. **Enfoque de la Propuesta:** Fomentar el desarrollo de productos o servicios de IA con innovación investigativa. La propuesta debe tener una transferencia tecnológica clara, orientada a obtener productos tangibles con un nivel de madurez tecnológica (TRL) de 6 o 7, demostrando utilidad e impacto real en el sector de aplicación.
3. **Estructura:** Sigue rigurosamente la estructura y las instrucciones de redacción detalladas a continuación.
4. **Redacción — prohibido el inciso "—texto—":** no uses la raya o el guion doble como recurso para intercalar una aclaración parentética (p. ej. "—no un esfuerzo aislado—", "—diagnóstico, planificación...—"). Reformula esas ideas como oración independiente, cláusula con comas, o paréntesis normal `(texto)`. Aplica a todas las secciones de la propuesta.
5. **TRL fuera de los objetivos:** el nivel de madurez tecnológica (TRL) objetivo **no se nombra textualmente** en el objetivo general ni en los objetivos específicos (§6, §7). El TRL se precisa únicamente en Metodología (§10) y Resultados esperados (§11); en los objetivos basta con expresar el nivel de transferencia tecnológica o validación esperada sin citar la sigla TRL ni el número de nivel.

---

### 1. Título de la propuesta
**Instrucción para el agente:** El título debe ser conciso, utilizando preferiblemente entre 12 y 15 palabras. Debe estar alineado con el propósito de la convocatoria y proporcionar claridad sobre la novedad de la investigación, su impacto esperado y las herramientas o modelos de IA asociados, desarrollados o implementados en el proyecto. Asimismo, debe mantener coherencia directa con la pregunta de investigación y el objetivo general.

**Regla de unicidad del título.** El texto del título se compila **una sola vez**, en la portada/bloque de título del documento (`\title{}`). Ninguna otra sección (Resumen, Resumen ejecutivo, encabezado de página, etc.) debe repetir el título completo como texto o como encabezado propio; si una sección necesita referirse al proyecto, debe hacerlo de forma referencial ("esta propuesta", "el proyecto") y no reproduciendo el título verbatim.

**Secciones preliminares (front-matter, sin numerar).** Las tres secciones siguientes (Resumen, Resumen ejecutivo, Palabras clave) son preliminares: se redactan como SÍNTESIS del documento completo en una fase tardía del pipeline (Fase 6.5, ver `.claude/commands/propuesta.md`) y en el documento final se renderizan ANTES de la sección 2, inmediatamente después del Título. NO llevan número (no alteran la numeración §2–§16); en el ensamble LaTeX se maquetan con `\section*{}` (sin numerar).

### Resumen
**Instrucción para el agente:** Redacta un resumen de máximo 400 palabras, en un solo bloque de texto (sin subdivisión en párrafos nombrados), que cubra en este orden: (1) el problema o contexto que motiva el proyecto; (2) el objetivo general; (3) una síntesis del enfoque metodológico; (4) el resultado o impacto esperado, incluyendo el TRL objetivo (6 o 7).

### Resumen ejecutivo
**Instrucción para el agente:** Redacta exactamente 5 párrafos:
* **Primer párrafo:** contexto y problemática que motiva el proyecto.
* **Segundo párrafo:** objetivo general y objetivos específicos, en síntesis.
* **Tercer párrafo:** síntesis del enfoque metodológico y técnico en IA.
* **Cuarto párrafo:** resultados y productos esperados, incluyendo el TRL alcanzado.
* **Quinto párrafo:** impacto esperado y transferencia tecnológica, a modo de cierre.

### Palabras clave
**Instrucción para el agente:** Selecciona las 5 palabras clave más representativas del proyecto, separadas por comas, en minúscula salvo nombres propios o siglas (p. ej. "aprendizaje automático, visión por computador, IA generativa, transferencia tecnológica, TRL").

### 2. Justificación y pertinencia de la propuesta

**Instrucción para el agente:** Esta sección argumenta la necesidad, vigencia y viabilidad del proyecto. Es independiente de la descripción del problema (§3): aquí NO se detallan subproblemas técnicos ni se plantea la pregunta de investigación (eso ocurre en §3); aquí se argumenta **por qué vale la pena resolverlo ahora, para quién, y con qué respaldo de política pública y de tendencia tecnológica**.

**Extensión mínima: al menos 6 párrafos**, cubriendo explícitamente los siguientes contenidos (pueden reordenarse o fusionarse dos contenidos afines en un mismo párrafo, pero ninguno puede omitirse):
1. **Motivación del proyecto:** qué vacío, oportunidad o necesidad concreta del sector de aplicación motiva la propuesta, y por qué es relevante abordarla en este momento.
2. **Alineación con los Objetivos de Desarrollo Sostenible (ODS):** identificar el o los ODS pertinentes (con su número y nombre oficial) y explicar concretamente cómo el proyecto contribuye a sus metas.
3. **Alineación con el Plan Nacional de Desarrollo (PND)** vigente (y con el **Plan de Desarrollo Departamental**, si el proyecto tiene un anclaje territorial claro y dicho plan aplica); citar el eje, línea o meta específica con la que conecta.
4. **Respaldo en informes de organismos multilaterales:** referenciar hallazgos o recomendaciones pertinentes de informes de la **OCDE** y del **Banco Mundial** (u otro organismo multilateral relevante, p. ej. BID, UNESCO, CEPAL) que sustenten la pertinencia del sector o la urgencia del problema; puede incluir cifras o proyecciones si están disponibles en la literatura o insumos provistos.
5. **Alineación con los TDR y el espíritu de la convocatoria:** explicar cómo la propuesta responde directamente al propósito declarado de la convocatoria y a sus términos de referencia (si se adjuntan), sin repetir literalmente el texto del TDR.
6. **Crecimiento y potencial de la IA en la temática de interés:** describir la evolución reciente de la IA (predictiva, generativa, agéntica, etc.) aplicable al sector, su nivel de adopción actual y su potencial de impacto, argumentando por qué este momentum tecnológico hace viable y oportuna la propuesta.

**Soporte bibliográfico obligatorio.** La sección debe citar **al menos 10 referencias de artículos en revistas Q1 o Q2** que validen las afirmaciones presentadas (motivación, alineación ODS/PND/plan departamental, hallazgos de OCDE/Banco Mundial u otro organismo multilateral, y evidencia del crecimiento y potencial de la IA en la temática). Estas 10 referencias son adicionales a las exigidas en Estado del arte (§4); pueden coincidir con ellas cuando una fuente sea pertinente en ambas secciones, siempre respetando el tope de reutilización por clave definido en Bibliografía (§16).

Adicionalmente, tras cubrir los seis puntos anteriores, cierra la sección con:
* **Justificación técnica del uso de IA:** por qué el enfoque de IA elegido (predictiva, generativa, agéntica, etc.) es superior a métodos tradicionales para este problema específico.
* **Justificación del producto tangible esperado** (p. ej. plataforma web, aplicativo móvil, modelo innovador de IA, despliegue en sistemas embebidos), enfatizando cómo este producto alcanza un **TRL 6 o 7** (aquí sí se puede nombrar el TRL, por tratarse de justificación técnica y no de la redacción de objetivos), facilitando la transferencia tecnológica hacia los beneficiarios del sector.

Cualquier cifra socioeconómica, tecnológica o ambiental que soporte la relevancia del proyecto (basada en literatura o documentos provistos) debe incorporarse en el punto que corresponda (típicamente 2, 4 o 6), no como párrafo aislado.

### 3. Descripción del problema

**Instrucción para el agente:** Esta sección presenta y delimita el problema técnico que la propuesta resuelve. Se estructura en el siguiente orden de párrafos:

* **Párrafo 1:** Presentar un contexto general de la problemática. Introduce el problema desde el sector de aplicación, contextualizando las principales limitaciones o desafíos operativos, económicos o sociales.
* **Párrafo 2:** Dar contexto a los desafíos técnicos desde la perspectiva de la inteligencia artificial, el aprendizaje automático o el procesamiento de señales. El párrafo debe terminar listando (en ítems) dos o tres subproblemas técnicos a resolver. Estos deben vincularse lógicamente con los objetivos de la propuesta (§6, §7) y responder al propósito de la convocatoria.
* **Párrafo 3:** Describir las causas, limitaciones tecnológicas y conceptos principales asociados al **subproblema 1**.
* **Párrafo 4:** Describir las causas, limitaciones tecnológicas y conceptos principales asociados al **subproblema 2**.
* **Párrafo 5:** Describir las causas, limitaciones tecnológicas y conceptos principales asociados al **subproblema 3** (si aplica).
* **Párrafo 6 (cierre del planteamiento):** Presentar una conclusión general que resalte la necesidad imperante de resolver dichos problemas y cómo la propuesta integral busca darles respuesta. Este párrafo **debe concluir formulando explícitamente la pregunta de investigación**. Finalmente, se debe proponer el contenido para una figura explicativa (tipo árbol de problemas) que resuma visualmente este planteamiento.

Esta sección **no incluye** revisión de literatura ni hipótesis: el sustento bibliográfico de los subproblemas se desarrolla en Estado del arte (§4), y la hipótesis se formula en su propia sección (§5).

**Estructura de redacción recomendada:** párrafos 1-2 (contexto general y desafíos técnicos, cerrando con la lista de subproblemas) → párrafos 3-5 (detalle de cada subproblema) → párrafo 6 (cierre, pregunta de investigación y figura de árbol de problemas).

### 4. Estado del arte

**Instrucción para el agente:** Esta sección, independiente de la Descripción del problema (§3), presenta la revisión de literatura que sustenta empíricamente los subproblemas allí planteados. El agente debe:
1.  **Investigar y agrupar el estado del arte global:** realizar una búsqueda exhaustiva de literatura académica, agrupando las estrategias o metodologías identificadas por filosofías de abordaje o por tipo de limitante, relacionándolas explícitamente con cada subproblema (1, 2 y, si aplica, 3) de §3. **Nota indispensable:** incluir al menos 30 referencias de artículos en revistas Q1 o Q2 publicadas en los últimos tres años.
2.  **Estado actual de la tecnología (punto de partida del equipo):** presentar el nivel tecnológico desde el cual parten los investigadores de la propuesta, con referencias, evidencias o pruebas empíricas que demuestren si se parte de cero o si ya existe un avance previo, detallando cómo se pretende potenciar dicha base aprovechando la presente convocatoria.
3.  **Identificar brechas tecnológicas:** comparar las soluciones y grupos existentes en el estado del arte global con la propuesta del proyecto, evidenciando críticamente qué aspectos no han sido resueltos.
4.  **Posicionar la propuesta (la novedad):** argumentar explícita y contundentemente la novedad científica o tecnológica de la propuesta frente a las brechas identificadas.

Cierra la sección con un **párrafo de síntesis** que resuma las estrategias más relevantes identificadas en la literatura, preparando el terreno para la hipótesis (§5).

### 5. Hipótesis

**Instrucción para el agente:** A partir de la síntesis del Estado del arte (§4), plantea una **hipótesis** en un único párrafo que anticipe el objetivo general que se formalizará en Objetivo general (§6). Debe definir con total claridad las limitantes tecnológicas, teóricas o metodológicas de la IA que la propuesta busca resolver, y quedar explícitamente vinculada a la pregunta de investigación formulada al cierre de la Descripción del problema (§3).

### 6. Objetivo general

**Instrucción para el agente:** La redacción de los objetivos (este apartado y el §7 siguiente) debe ser rigurosa y técnica. Selecciona verbos rectores como *Desarrollar*, *Diseñar* o *Proponer* (elige uno) cuando abordes novedades metodológicas, conceptuales o teóricas en IA (por ejemplo, nuevas funciones de costo, regularizadores, arquitecturas novedosas, etc.). Utiliza verbos como *Implementar*, *Desplegar* o *Validar* (elige uno) para aquellos objetivos enfocados en la transferencia tecnológica y la aplicación en entornos relevantes. Para todos los casos, la redacción debe dejar explícita la forma de validación (cuantitativa o al menos cualitativa) que permitirá verificar su cumplimiento.

**Regla de verbo rector único.** La pregunta de investigación, el objetivo general y CADA objetivo específico deben redactarse con EXACTAMENTE UN verbo rector en infinitivo (el más pertinente). Los listados de verbos son MENÚS: elige UNO, no los encadenes. Prohibido el encadenamiento de rectores coordinados (p. ej. «desarrollar, implementar y validar»). Se PERMITEN infinitivos subordinados de propósito («... para apoyar el diagnóstico»): solo se limitan los rectores coordinados de la cláusula principal.

**Sin mención textual de TRL.** Ni el objetivo general ni los objetivos específicos (§7) deben nombrar la sigla TRL ni un número de nivel; expresa el nivel de transferencia o validación esperada en términos funcionales ("desplegado y validado en el entorno de aplicación real", "listo para su adopción por el usuario final"). El TRL numérico se reserva para Metodología (§10) y Resultados esperados (§11).

El objetivo general debe derivarse directamente y ser la respuesta exacta a la pregunta de investigación formulada al final de §3 (Descripción del problema), en coherencia con la hipótesis planteada en §5. Debe ser ambicioso pero totalmente alcanzable en el tiempo de duración de la convocatoria. Además, debe reflejar claramente la innovación propuesta y el valor agregado en IA, y el impacto tecnológico esperado en términos funcionales (sin nombrar el TRL, ver regla arriba).

### 7. Objetivos específicos

**Instrucción para el agente:** Los objetivos específicos se rigen por las mismas reglas de verbo rector único y de no mención textual de TRL definidas en §6. Deben derivarse lógica y coherentemente del objetivo general, representando los pasos metodológicos y técnicos secuenciales del proyecto. Es un requisito estricto que cada objetivo específico esté directamente relacionado y dé respuesta a uno de los subproblemas planteados en §3 (Descripción del problema). El agente debe redactar al menos tres objetivos específicos estructurados de la siguiente manera:

*   **Objetivo Específico 1 (Fundamentos y Caracterización de Datos):** Centrado en el levantamiento, curaduría, estructuración de los datos o en la caracterización fenomenológica del problema. Debe dar solución concreta al **subproblema 1**. *(Verbos sugeridos — elige uno: Caracterizar, Estructurar, Analizar, Procesar).*
*   **Objetivo Específico 2 (Novedad Teórica y Metodológica en IA):** Centrado en el núcleo de investigación: la conceptualización, diseño, entrenamiento y ajuste del modelo, metodología, algoritmo o arquitectura de IA propuesta como novedad. Debe dar solución concreta al **subproblema 2**. *(Verbos sugeridos — elige uno: Desarrollar, Proponer, Diseñar, Modelar).*
*   **Objetivo Específico 3 (Transferencia Tecnológica, Despliegue y Validación):** Orientado a la implementación, integración del sistema en el entorno de aplicación, despliegue del producto y su validación técnica/operativa (cuantitativa o cualitativa) para demostrar la transferencia del conocimiento y el nivel de madurez tecnológica alcanzado (el TRL correspondiente se detalla en Metodología y Resultados esperados, no aquí). Debe dar solución concreta al **subproblema 3**. *(Verbos sugeridos — elige uno: Implementar, Desplegar, Validar, Evaluar).*

### 8. Marco conceptual

**Instrucción para el agente:** Esta sección establece las bases conceptuales y teóricas que sustentan el desarrollo metodológico (§10). El agente debe:
1.  **Conceptualizar:** Definir de manera precisa los conceptos clave y términos técnicos utilizados en la propuesta, asegurando la claridad terminológica para el lector.
2.  **Fundamentar Teóricamente:** Establecer las bases teóricas de la línea de investigación seleccionada. Esto implica argumentar cómo la propuesta se sitúa dentro de los enfoques más relevantes y actualizados de la teoría o tecnología en cuestión (por ejemplo, Deep Learning, Machine Learning, Visión por Computador, Procesamiento de Lenguaje Natural, etc.).
3.  **Conectar con el Problema:** Justificar cómo estas bases teóricas seleccionadas abordan directamente las limitaciones tecnológicas identificadas en §3 (Descripción del problema).

Esta sección es deliberadamente breve (1-3 párrafos): describe los conceptos y su fundamento, sin repetir el detalle de cada enfoque algorítmico por subproblema, que corresponde a la Metodología (§10).

### 9. Equipo de trabajo

**Instrucción para el agente:** Presentar el equipo de trabajo del proyecto en una **tabla única** (`tab:equipo`) con columnas: **Integrante** | **Rol** | **Sede/Institución/Dependencia** | **Responsabilidades**. Los datos de identidad (nombres, sede, dependencia o alianza) deben tomarse de los insumos confirmados por el usuario; nunca inventarlos. El **rol y las responsabilidades** de cada integrante se derivan de los objetivos específicos (§7) y de la cadena de valor del proyecto: cada integrante debe quedar vinculado explícitamente a al menos uno de ellos, sin remitir a la Metodología (§10), que se redacta después y es la que referencia a este equipo, no al revés.

Si la convocatoria involucra una alianza entre varias instituciones, sedes o grupos de investigación, la sección debe evidenciarlo explícitamente en el párrafo introductorio (quiénes conforman la alianza y por qué esa composición es adecuada para el alcance del proyecto), antes de presentar la tabla.

Cualquier dato de equipo que no provenga de un insumo directo del usuario (p. ej. un rol inferido a partir de la metodología, sin confirmación explícita) debe marcarse **[inferido]** para revisión en la compuerta interactiva correspondiente.

### 10. Metodología

**Instrucción para el agente:** La metodología debe ser estructurada y redactada de forma clara, concisa y sin repeticiones. Para garantizar su viabilidad y organización técnica, se deben seguir las siguientes directrices:

1.  **Estructura de Cadena de Valor por Objetivo:** La metodología debe desarrollarse secuencialmente, abordando cada uno de los objetivos específicos (§7) como un eslabón de una cadena de valor.
2.  **Detalle por Fase/Objetivo:** Para cada objetivo específico, se debe detallar:
    *   Las actividades principales a ejecutar y el personal responsable de la fase (coherente con el Equipo de trabajo, §9).
    *   El sustento o fundamento teórico/metodológico que respalda dichas actividades (apoyado en los conceptos y enfoques introducidos en el Marco conceptual, §8: nombrar el enfoque, algoritmo o técnica específica, describir brevemente su funcionamiento, y conectarlo causalmente con el subproblema que resuelve).
    *   Los recursos tecnológicos necesarios.
    *   Los elementos y herramientas disponibles gracias a la experiencia previa del equipo de investigación propuesto.
3.  **Diagrama Esquemático Final:** La sección debe concluir planteando el contenido y la estructura para un diagrama esquemático metodológico. Este diagrama debe:
    *   Representar visualmente las fases principales de la propuesta.
    *   Destacar las novedades metodológicas o algorítmicas más importantes de la investigación en IA.
    *   Reflejar claramente el impacto y los posibles usuarios o beneficiarios finales del producto o servicio de IA a desarrollar.
    *   Resaltar visualmente el nivel de madurez tecnológica (TRL) desde el que se parte (basado en la experiencia del grupo) hasta el TRL meta al que se quiere llegar (TRL 6 o 7).

### 11. Resultados esperados

**Instrucción para el agente:** Presentar los resultados conceptuales esperados por cada objetivo específico (§7), así como los resultados de generación de nuevo conocimiento (hallazgos, avances metodológicos), de transferencia tecnológica (ponencias, charlas, talleres) y de formación (tesis de pregrado, tesis de maestría, vinculación de estudiantes de posgrado o semilleros). Precisa el **TRL alcanzado** al cierre del proyecto y el impacto o beneficio esperado para los usuarios/beneficiarios del sector de aplicación. Los productos concretos y su tipología formal (software, patentes, artículos, etc.) se listan en Productos esperados (§15), no aquí: esta sección se centra en el resultado (qué se logra y para quién), aquella en el producto (qué se entrega y en qué formato).

### 12. Consideraciones éticas

**Instrucción para el agente:** Presentar las consideraciones éticas del proyecto articuladas en torno a cuatro ejes, cuando el proyecto involucre sujetos humanos, datos personales o sistemas de IA con impacto directo en personas (si alguno de los ejes no aplica, decláralo explícitamente en vez de omitirlo):
1.  **Consentimiento informado:** si el proyecto involucra participantes humanos (p. ej. estudiantes, usuarios finales, pacientes), describir el proceso de consentimiento informado (información entregada, voluntariedad, derecho a retirarse, y consentimiento/asentimiento diferenciado si hay menores de edad).
2.  **Protección de datos personales:** describir cómo se recolectan, almacenan y anonimizan los datos, en cumplimiento de la normativa nacional de protección de datos aplicable (p. ej. Ley 1581 de 2012 en Colombia, o la que corresponda según el país de la convocatoria).
3.  **Aval de comité de ética/bioética:** indicar si el proyecto requiere aval de un comité institucional de ética o bioética, y en qué fase del plan de trabajo se tramitará; si no aplica, declararlo explícitamente con su justificación.
4.  **Uso responsable de la IA:** describir las salvaguardas frente a sesgos, transparencia y explicabilidad del modelo, y límites de uso previstos para evitar impactos no deseados sobre los beneficiarios.

Todo contenido de esta sección que no provenga de un insumo directo del usuario debe marcarse **[inferido]** para revisión en la compuerta interactiva.

### 13. Presupuesto

**Instrucción para el agente:** Esta sección presenta el presupuesto del proyecto en una **tabla única** (`tab:presupuesto`) y lo justifica en relación directa con la metodología (§10) y con el cronograma de actividades (§14). El presupuesto debe ser aritméticamente consistente y respetar los topes, la cofinanciación y la duración que establezca la convocatoria cuando los especifique.

**Nota de orden de redacción.** Aunque el Cronograma de actividades se numera después del Presupuesto (§14 va después de §13) para seguir el orden de la lista de secciones del documento final, el agente debe contar con el cronograma **ya esbozado** (aunque sea en borrador) antes de cerrar el presupuesto, puesto que cada ítem debe enlazarse con una actividad concreta del cronograma.

**Modo de operación (según insumos):**
*   **Modo TDR** — existe un bloque `## Marco presupuestal (TDR)` en `proposal/insumos.md` (o en `guia_ajustada_TDR.md`) con tope no vacío: toma de allí el tope total, el esquema de cofinanciación **tal como lo define el TDR** (con sus condiciones de aplicabilidad — el porcentaje puede variar por sede o por quién lidera la alianza; p. ej. 70/30 nacional/contrapartida para unas sedes y 100% nacional para otras), la duración y los rubros permitidos. La suma total **no puede exceder el tope**; los subtotales por fuente deben respetar el split aplicable al caso de esta propuesta.
*   **Modo base** — no hay datos presupuestales en el TDR (sentinel `sin datos presupuestales en TDR`): construye un presupuesto razonado a partir de la metodología (§10) y el cronograma de actividades (§14). Todo monto o cantidad que no se derive de un insumo se marca explícitamente como **[supuesto]** para que el usuario lo revise en la compuerta interactiva.

**Estructura de la tabla.** Una fila por ítem, con columnas: **Ítem** | **Cantidad** | **Valor unitario** | **Valor total** | **Descripción** | **Justificación**. Cuando la convocatoria defina rubros, agrupa las filas por rubro con un **subtotal por rubro**, y cierra con una fila de **Total general**.

**Reglas aritméticas (obligatorias, verificables a simple vista):**
1.  En cada fila, `Valor total = Cantidad × Valor unitario`.
2.  El subtotal de cada rubro es la suma de los `Valor total` de sus filas.
3.  El **Total general** es la suma de los subtotales y, en Modo TDR, **no puede exceder el tope**.
4.  Si el TDR define cofinanciación, los subtotales por fuente (p. ej. nacional vs contrapartida) deben cumplir el porcentaje **aplicable a esta propuesta según el TDR**, dentro de una tolerancia de redondeo explícita.
5.  Usa una sola moneda y un formato de miles consistente en toda la tabla.

**Justificación (regla dura).** La columna **Justificación** de cada ítem (o de cada rubro) debe (a) argumentar su pertinencia y (b) enlazarlo **explícitamente** con un elemento nombrado de la metodología (§10) o con una fase/actividad del cronograma de actividades (§14) que lo requiere. No se admiten ítems sin ese enlace.

**Cierre.** Cierra con un párrafo breve que sintetice cómo el presupuesto habilita el logro del objetivo general (§6) y los objetivos específicos (§7), y —en Modo TDR— que confirme el cumplimiento del tope y de la cofinanciación aplicable.

**LaTeX.** `\section` autocontenido, sin subsecciones; una `table` con `\label{tab:presupuesto}`, sombreado con `xcolor[table]` (mismos colores institucionales y estilo que la tabla de cronograma de §14). No introduce paquetes nuevos.

### 14. Cronograma de actividades

**Instrucción para el agente:** El cronograma de actividades debe presentarse preferiblemente mediante una **tabla tipo cronograma** (ej. Diagrama de Gantt) estructurada en fases o periodos (meses, trimestres, semestres, etc.).
1.  **Alineación Temporal:** El cronograma debe estar rigurosamente detallado y ajustado al tiempo total de ejecución establecido en los términos de referencia de la convocatoria (por ejemplo, 6 meses, 12 meses, 3 años).
2.  **Actividades y Responsables:** Las actividades incluidas en la tabla deben corresponder exactamente con las fases y acciones de la Metodología (§10). Además, para cada actividad o etapa, se debe designar claramente el **personal o rol responsable** (coherente con el Equipo de trabajo, §9).
3.  **Hitos y Productos:** El cronograma debe describir y evidenciar con claridad cómo y en qué momento exacto del tiempo se obtendrán y entregarán los resultados (§11) y productos (§15) prometidos.

### 15. Productos esperados

**Instrucción para el agente:** Según lo descrito en Resultados esperados (§11), y cruzándolo rigurosamente con los términos de referencia de la convocatoria, el agente debe proponer y estructurar los productos académicos concretos (siguiendo la tipología institucional o de la convocatoria cuando exista, p. ej. nuevo conocimiento, formación, apropiación social/divulgación, transferencia) que garanticen la obtención del puntaje máximo estipulado para la evaluación de la propuesta. Cada producto debe indicar su tipología, un responsable y el momento del cronograma (§14) en que se entrega.

### 16. Bibliografía

**Instrucción para el agente:** La bibliografía debe consolidar la actualidad científica de la propuesta y cumplir con los siguientes parámetros de calidad:
1.  **Formato:** Utilizar **APA, autor-año** (no numeración estilo IEEE `[1]`). En LaTeX esto implica `natbib` con `\citet{clave}` (autor como sujeto gramatical: "Pérez (2025) encontró que...") o `\citep{clave}` (cita parentética: "...se ha reportado (Pérez, 2025)") — nunca `\cite{}` genérico ni reemplazo mecánico ciego entre `\citet`/`\citep`, la elección depende del rol gramatical de la cita en la oración. `\bibliographystyle{apalike}` (o equivalente `natbib`/`plainnat` en autor-año) en el ensamble final.
2.  **Tope de citas por referenciación:** máximo **3 claves** por cada llamada de cita (`\citet{}`/`\citep{}`). Si un punto del texto tiene soporte de más de 3 referencias relevantes, citar solo las **más relevantes y más recientes**, no acumularlas todas en un solo cluster (evitar patrones como `\cite{a, b, c, d, e}`, que consumen espacio sin aportar lectura útil). Una misma llamada `\citet{}`/`\citep{}` puede estar partida en varias líneas físicas del fuente `.tex`; el tope de 3 claves se mide sobre la llamada LÓGICA (uniendo las líneas partidas y contando las claves entre `{` y `}`), no por línea física.
3.  **Tope de reutilización por clave:** una misma referencia **no puede citarse más de 3 veces** en todo el documento. Si se reutiliza (2ª o 3ª vez), cada reutilización debe estar en una **sección distinta** del documento — nunca repetida dos veces dentro de la misma sección. El conteo de reutilización también se mide sobre llamadas lógicas: una llamada partida en varias líneas cuenta una sola vez.
4.  **Calidad y Actualidad:** Se debe favorecer e incluir mayoritariamente artículos publicados en revistas indexadas en **cuartiles Q1 y Q2 de los últimos tres años**.
5.  **Volumen:** Para demostrar rigor en proyectos de investigación aplicada, se recomienda integrar un soporte bibliográfico sólido con **más de 50 citas**.
6.  **Fuentes Permitidas:**
    *   **Evitar** explícitamente citar tesis de grado o maestría.
    *   Se permite incluir libros teóricos de alto impacto.
    *   Se permite incluir artículos en pre-impresión (tipo *arXiv*) **solo** si provienen de laboratorios de empresas líderes en IA, investigadores reconocidos mundialmente o universidades de alto prestigio.

---

### Convenciones técnicas de LaTeX

Estas convenciones son la única fuente de verdad para el ensamble LaTeX; aplícalas al redactar cada sección, no al ensamblar.

**Anidamiento de encabezados**

| Secciones | Convención |
|---|---|
| Todas las secciones (§1–§9, §11–§16) | `\section` autocontenido, sin subsecciones. |
| §10 Metodología | `\section` autocontenido con encabezados internos de fase OPCIONALES y SIN numerar (`\subsection*`), no `\subsection` numerado. |

**Paquetes del preámbulo**

| Paquete | Propósito |
|---|---|
| `natbib` + `apalike` | Citas autor-año |
| `cleveref` | `\Cref` |
| `enumitem` | Listas |
| `pgfgantt` + `tikz` + `shapes.geometric` | Gantt / figuras |
| `xcolor[table]` | Colores / tablas |

**Colores institucionales**

Definidos una única vez aquí (fuente de verdad); estos tres colores están actualmente duplicados en `main.tex`, `compile_tikz.py` y comentarios de `diag_*.tex` — los agentes de diagramación deben referenciar estos nombres canónicos, no redefinir los valores.

```latex
\definecolor{azulUNAL}{HTML}{0066B3}
\definecolor{grisLabIA}{HTML}{666666}
\definecolor{verdeGCPDS}{HTML}{2E8B57}
```

**Convención `\label{}`/`\Cref{}`**

| Prefijo | Elemento |
|---|---|
| `fig:*` | Figuras |
| `tab:*` | Tablas |

**Encabezado y pie institucional (logos)**

Regla única de colocación de los tres logos institucionales en `main.tex`
(fuente de verdad; los agentes de diagramación NO deben añadir logos a las
figuras). Los archivos residen en `proposal/logos/` (ruta preservada entre
ciclos de archivado). Como el build compila dentro de `proposal/`, se
referencian de forma relativa como `logos/*.png`.

| Logo | Posición | Campo `fancyhdr` | Alto |
|---|---|---|---|
| UNAL (`logo_unal.png`) | superior derecha | `\fancyhead[R]` | 1.1 cm |
| GCPDS (`logogcpds.png`) | inferior izquierda | `\fancyfoot[L]` | 1.0 cm |
| LabIA (`logo_labIA.png`) | inferior derecha | `\fancyfoot[R]` | 1.0 cm |

Preámbulo canónico: `\usepackage{fancyhdr}`, `\pagestyle{fancy}`,
`\fancyhf{}` (reset), `\headrulewidth`/`\footrulewidth` a `0pt` (sin líneas),
`\geometry{headheight=38pt}` para alojar el logo de cabecera (usa la opción
en tiempo de ejecución del propio paquete `geometry` ya cargado por
`main.tex`; no uses `\addtolength{\topmargin}{...}` para compensar, ya que
`geometry` puede ignorar o sobrescribir un ajuste manual del margen una vez
que ha fijado la geometría de página). La página del título usa estilo
`plain`; para mostrar los logos también en la página 1, añade
`\thispagestyle{fancy}` justo después del bloque de título. Los tamaños son
cosméticos y ajustables. El encabezado únicamente contiene el logo (imagen);
el texto del título no se repite ahí (ver "Regla de unicidad del título" en §1).

Preámbulo canónico (fuente de verdad para el ensamble en Fase 7; copia y
pega este bloque en `main.tex`, omitiendo `\usepackage{graphicx}` si el
preámbulo ya lo carga — main.tex lo requiere para figuras y NO debe
duplicarse):

```latex
% --- Encabezado/pie institucional (fancyhdr) ---------------------------------
% Fuente de verdad: guiaProyectosIA_Agente.md > "Encabezado y pie institucional".
\usepackage{fancyhdr}
% \usepackage{graphicx}               % NO dupliques: ya cargado por main.tex
\geometry{headheight=38pt}            % opción en tiempo de ejecución de geometry
                                       % (ya cargado); NO uses \addtolength{\topmargin}
\pagestyle{fancy}
\fancyhf{}                            % limpia todos los campos (head/foot L/C/R)
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhead[R]{\includegraphics[height=1.1cm]{logos/logo_unal.png}}   % UNAL arriba-derecha
\fancyfoot[L]{\includegraphics[height=1.0cm]{logos/logogcpds.png}}   % GCPDS abajo-izquierda
\fancyfoot[R]{\includegraphics[height=1.0cm]{logos/logo_labIA.png}}  % LabIA abajo-derecha
```

Añade `\thispagestyle{fancy}` justo después del bloque de título para que
los logos también aparezcan en la página 1 (por defecto `\maketitle` fuerza
el estilo `plain`).
