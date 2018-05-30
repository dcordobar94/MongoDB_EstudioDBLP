import pymongo
import json


def connection(bd, collection):
    # mongod debe estar corriendo
    # > cd "C:\Program Files\MongoDB\Server\3.6\bin"
    # > mongod.exe
    # Creamos una conexión (por defecto sin parámetro al localhost: puerto 27017)
    conex = pymongo.MongoClient()

    # Usamos una BD existente o creamos una nueva

    db = getattr(conex, bd)
    # es equivalente a #db = conex.bd

    col = getattr(db, collection)
    print("Conectado a la coleccion", collection, "de la base de datos ", bd)
    return col


def read_json(file):
    with open(file, 'r', encoding="ISO-8859-1") as f:
        file = f.read()
    f.close()
    file = json.loads(file)
    return file


def add_autor(col, autor, publicacion, tipo_articulo):
    tipo_articulo = "numero_"+tipo_articulo+"s"
    col.update(autor, {'$push': {'publicaciones': publicacion}, '$inc': {tipo_articulo: 1}}, upsert=True)


def enter_to_mongodb(autores, articulos, file, tipo):
        print("Introduciendo archivo del tipo", tipo, "en Mongodb...")
        for article in file:  # file.values debe dar article, inproceedings etc...
            try:
                publications = {"_id": article['@key'], "year": article['year']}
                authors = article['author']
                #Actualizacion de la coleccion autores
                if type(authors) == str:
                    autor = {'_id': authors}
                    add_autor(autores, autor, publications, tipo)

                elif type(authors) == list:
                    for author in authors:
                        autor = {'_id': author}
                        add_autor(autores, autor, publications, tipo)

                # Actualizacion de la coleccion articulos
                title = {'titulo': article['title']}
                publications.update(title)

                if type(authors) == str:
                    publications.update({'autores': [authors]})
                else:
                    publications.update({'autores': authors})

                publications.update({'type': tipo})
                articulos.save(publications)

            except KeyError:
                pass
        print("Base de datos actualizada.")


if __name__ == '__main__':
    aut = connection('dblp', 'autores')
    articulos = connection('dblp', 'articulos')
    print('Se va a proceder a la creacion de las colecciones, podria dar algun problema en caso de existir.')
    response = str(input('¿Desea continuar?[Yes\ No]'))
    if response.lower() == 'yes':
        r = read_json('dblp_article.json')
        enter_to_mongodb(aut, articulos, r['article'], 'revista')
        i = read_json('dblp_inproceedings.json')
        enter_to_mongodb(aut, articulos, i['inproceedings'], 'conferencia')
        c = read_json('dblp_incollection.json')
        enter_to_mongodb(aut, articulos, c["incollection"], 'recopilacione')

