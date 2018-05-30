#Ficheros incluidos

Programas:

1) transform_to_json.py, que toma el fichero xml y lo transforma a varios fichero en formato json cada uno correspondiente a una de las coleciones que queremos crear;
2) enter_data_in_Mongodb.py, que conecta con la base de datos MongoDB, crea una base de datos llamada "**" y escribe los fichero json como coleciones en esa base de datos;
3) queries.py, que  realiza las consultas de los 10 apartados de la parte I de la pr\'actica;
4) transform_csv.py, que transforma los ficheros json a csv adaptando a la estructura elegida
 para su paso a Neo4j.

Datos:

1) dblp_article.json: datos referentes a las publicaciones tipo articulos.
2) dblp_inproceedings.json: datos referentes a las publicaciones tipo "inproceedings".
3) dblp_incollection.json: datos referentes a las publicaciones tipo "incollection".
4) csv_autores.csv: lista de autores, fichero para introducir a Neo4j.
5) csv_pub.csv: lista de publicaciones, fichero para introducir a Neo4j.
6) csv_year.csv: lista de años de publicaciones, fichero para introducir a Neo4j.
7) csv art.csv: fichero que contiene el identificador (key) y el titulo de los artículos.



#Proceso

PARTE I

Con el programa transform_to_json.py tranformamos el fichero original de datos en formato XML, se generan
 los tres ficheros json: dblp_article.json, dblp_inproceedings.json, dblp_incollection.json.

Con el proprama enter_data_in_Mongodb.py, conectamos a MongoDB, creamos la base de datos y dos colecciones
 a partir de los fichero json.

Una vez se han creado las colecciones, usamos el programa queries.py para las 10 consultas.

PARTE II

Con el programa transform_csv.py, generamos los ficheros que seran los nodos y la conexión para Neo4j:
csv_autores.csv, csv_pub.csv, csv_year.csv y csv art.csv.

Seguimos los siguientes pasos para meter los datos creando los nodos, generando índices y creando las relaciones:

creación nodos:

USING PERIODIC COMMIT
LOAD CSV  WITH HEADERS FROM 'file:///csv_autores.csv' AS row
CREATE (au:Autores { id_name: row.Autor})

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///csv_years.csv' AS row
CREATE (ye:Years { year: toInteger(row.Year)})

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///csv_art.csv' AS row
CREATE (pu:Publicaciones { id_p: row.Key, title: row.Titulo})

creación índices:

CREATE INDEX ON :Autores(id_name)

CREATE INDEX ON :Years(year)

CREATE INDEX ON :Publicaciones(id_p)

creación de relaciones:

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv_pub.csv" AS row
MATCH (pu:Publicaciones { id_p: row.Key, title: row.Titulo})
MATCH (au:Autores { id_name: row.Autor})
MERGE (au)-[WR:WROTE]->(pu)

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv_pub.csv" AS row
MATCH (pu:Publicaciones { id_p: row.Key, title: row.Titulo})
MATCH (ye:Years { year: toInteger(row.Year)})
MERGE (pu)-[in:PUBIN]->(ye)


MATCH p=()-[r:WROTE]->()-[q:PUBIN]->() RETURN p LIMIT 50

Consultas:

Publicaciones de Autor
MATCH p=(au:Autores {id_name:"Norbert Blum"})-[r:WROTE]->() RETURN p

En numero
MATCH p=(au:Autores {id_name:"Norbert Blum"})-[r:WROTE]->() RETURN COUNT (p)

Autores en 2017
MATCH p=(ye:Years {year:1983})<-[r:PUBIN]-()<-[s:WROTE]-() RETURN p LIMIT 50
En numero
MATCH p=(ye:Years {year:1983})<-[r:PUBIN]-()<-[s:WROTE]-() RETURN COUNT (p)

Los Coautores de Norbert Blum
MATCH p=(au:Autores {id_name:"Norbert Blum"})-[r:WROTE]->()<-[s:WROTE]-() RETURN p




