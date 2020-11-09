# Práctica 1: Web scraping
## Descripción
Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de web scraping mediante el lenguaje de programación Python para extraer así datos de la liga de futbol profesional LFP de la web https://es.fcstats.com/partidos,primera-division-espana,19,1,3023.php y generar 3 dataset.

## Inspiración
El motor principal que nos ha llevado a recoger este tipo de datos ha sido nuestra afición por este deporte. Con este trabajo no solo publicamos datos abiertos sobre la liga española, con los que se pueden hacer consultas específicas o globales y elaborar gráficos interesantes, sino que también presentamos un método de web scraping a partir del cuál es posible obtener la información de otras temporadas u otras ligas almacenada en la estructura html de la web. Con respecto a los datasets publicados, de cada uno de ellos es posible obtener la siguiente información:

**partidos.csv**: se podrán realizar consultas concretas sobre resultados, estadio, árbitro, etc. Aunque la parte más interesante es aquella destinada a recoger las estadísticas de cada equipo durante el partido. Se puede estudiar la evolución temporal de las mismas, la correlación entre ellas o incluso la correlación entre ellas y el rendimiento de ciertos jugadores, si usamos también el dataset 'alineaciones.csv'.  
**alineaciones.csv**: con estos datos es posible realizar análisis del rendimiento de los jugadores y cómo influye éste en las estadísticas de cada partido o si se ve influenciado por ciertas circunstancias como el sistema de juego, la posición o partir como titular.  
**eventos.csv**: en este dataset se recoge información más detallada de circunstancias que se dan en cada partido. Como tarjetas, goles, cambios, etc. Lo interesante de este juego de datos es que podemos conocer la autoría de cada uno de estos eventos, y estudiar el impacto que éstos tienen sobre el rendimiento del jugador, el resultado o las estadísticas de los partidos.  

En conclusión, queda de manifiesto la gran cantidad de posibilidades de análisis que puede barajar el futuro usuario de éstos datos. Aparte de facilitar estos datos al público (consultar publicación), queremos expresar nuestro deseo de que más personas contribuyan a la publicación abierta de datasets de ámbito deportivo.

## Ficheros del código fuente
src/main.py: punto de entrada al programa. Inicia el proceso de scraping.  
src/LFP.py: contiene la implementación de la clase LFP_Scraper cuyos métodos extraen la información de la web creando los 3 datasers.  
csv/Partidos.csv: Dataset resultante con la información de los paridos.  
csv/Alineaciones.csv: Dataset resultante con la información de las alineaciones de los partidos.   
csv/Eventos.csv: Dataset resultante con la información de los eventos de los partidos.   
pdf/WS.pdf:  Fichero con las respuestas de dicha práctica.   

## Miembros del equipo
La actividad ha sido realizada por
* Rodrigo Rico Gómez
* Roger Cervantes Sentenà

## Recursos
* Subirats, L., Calvo, M. (2019). Web Scraping. Editorial UOC.
* Masip, D. (2010). El lenguaje Python. Editorial UOC.
* Tutorial de Github https://guides.github.com/activities/hello-world.
* Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
* Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
