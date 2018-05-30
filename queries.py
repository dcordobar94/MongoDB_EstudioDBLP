from enter_data_in_Mongodb import connection

if __name__ == '__main__':
    aut = connection('dblp', 'autores')
    articulos = connection('dblp', 'articulos')

    print("\n Numero de autores en la base de datos: ", aut.find().count())
    print("Numero de articulos en la base de datos: ", articulos.find().count())

    autor = "Nathan Goodman"
    print("\n El autor escogido como ejemplo para las consultas es", autor)

    print("\n 1. Listado de todas las publicaciones de", autor)
    for i in aut.aggregate([{"$match": {"_id": {"$eq": autor}}}, \
                            {"$unwind": "$publicaciones"}, \
                            {"$lookup": { \
                                    "from": "articulos", \
                                    "localField": "publicaciones._id", \
                                    "foreignField": "_id", \
                                    "as": "Articulos" \
                                    }}, \
                            {"$match": {"Articulos": {"$ne": []}}}, \
                            {"$project": {"Titulo": "$Articulos.titulo"}}
                            ]):
        print(i)

    for i in aut.aggregate([{"$match": {"_id": autor}}, \
                            {"$project": {"TotalArticulos": {"$size": "$publicaciones"}}}]):
        print("\n 2. Numero de publicaciones de", autor, ": ", i)

    for i in articulos.aggregate([{"$match": {"$and": [{"type": "revista"}, {"year": 2017}]}}, \
                                  {"$count": "year"}]):
        print("\n 3. Numero de publicaciones en revistas para 2017: ", i['year'])

    num = aut.find({"publicaciones.5": {"$exists": False}}).count()
    # num = aut.aggregate([{"$project": {"TotalArticulos": {"$size": "$publicaciones"}}}, \
    #    {"$match": {"TotalArticulos": {"$lt": 5}}}]).count()
    print("\n 4. Numero de autores ocasionares: ", num)

    print("\n 5. Numero de articulos de revista (article) y numero de articulos en congresos (inproceedings) de los" \
          " diez autores con más publicaciones totales.")
    for i in aut.aggregate([{"$project": {"TotalArticulos": {"$size": "$publicaciones"}, \
                                          "NumeroRevistas": "$numero_revistas", \
                                          "NumeroConferencias": "$numero_conferencias" \
                                          }}, \
                            {"$sort": {"TotalArticulos": -1}}, \
                            {"$limit": 10}]):
        print(i)

    print("\n 6. Numero medio de autores de todas las publicaciones")
    for i in articulos.aggregate([{"$project": {"num_autores": {"$size": "$autores"}}}, \
                                  {"$group": {
                                      "_id": "Null", \
                                          "NumeroMedioAutores": {"$avg": "$num_autores"}} \
                                          }]):
        print(i['NumeroMedioAutores'])

    print("\n 7. Listado de coautores por articulo del autor", autor, ":")
    for i in aut.aggregate([{"$match": {"_id": {"$eq": autor}}}, \
                            {"$unwind": "$publicaciones"}, \
                            {"$lookup": { \
                                    "from": "articulos", \
                                    "localField": "publicaciones._id", \
                                    "foreignField": "_id", \
                                    "as": "Coautores" \
                                    }}, \
                            {"$match": {"Coautores": {"$ne": ""}}}, \
                            {"$project": { \
                                    "Titulo": "$Coautores.titulo", \
                                    "Coautores": "$Coautores.autores"}} \
                            ]):
        print(i)
    print("\n 8. Edad de los 5 autores con periodo de publicacion mas largo")
    for i in aut.aggregate([{"$unwind": "$publicaciones"}, \
                            {"$group": {"_id": "$_id", \
                                        "max": {"$max": '$publicaciones.year'},
                                        "min": {"$min": "$publicaciones.year"}}}, \
                            {"$project": {"diferencia": {"$subtract": ["$max", "$min"]}}}, \
                            {"$sort": {"diferencia": -1}}, \
                            {"$limit": 5}], \
                           allowDiskUse=True):
        print(i)

    print("\n 9. Numero de autores con periodo de publicacion mas corto")

    for i in aut.aggregate([{"$unwind": "$publicaciones"}, \
                            {"$group": {"_id": "$_id", \
                                        "max": {"$max": '$publicaciones.year'},
                                        "min": {"$min": "$publicaciones.year"}}}, \
                            {"$project": {"diferencia": {"$subtract": ["$max", "$min"]}}}, \
                            {"$match": {"diferencia": {"$gte": 5}}}, \
                            {"$count": "diferencia"}],
                           allowDiskUse=True):
        print(i['diferencia'])

    co_re = articulos.find({"type": "revista"}).count()
    co_co = articulos.find({"type": {"$ne": "revista"}}).count()
    propo = co_re / (co_re + co_co)
    print("\n 10. Porcentaje de publicaciones en revistas con respecto al total de publicaciones:", propo * 100, "%")
