import json


def read_json(file):
    with open(file, 'r') as f:
        file = f.read()
    f.close()
    file = json.loads(file)
    return file


def save_csv(f, tag):
    count = 0
    for i in f[tag]:
        count += 1
        try:
            author = i['author']
            if type(author) == str:
                csv_pub.write('"' + i['@key'] + '","' + i['title'].replace('"', "'") + '","' + str(
                    i['year']) + '","' + author.replace('"', "'") + '"\n')

                if author not in autores:
                    csv_autores.write('"' + author.replace('"', "'") + '"\n')
                    autores.add(author)
            else:
                for aut in author:
                    csv_pub.write('"' + i['@key'] + '","' + i['title'].replace('"', "'") + '","' + str(
                        i['year']) + '","' + aut.replace('"', "'") + '"\n')

                    if aut not in autores:
                        csv_autores.write('"' + aut.replace('"', "'") + '"\n')
                        autores.add(aut)

            if i['year'] not in year:
                csv_year.write('"' + str(i['year']) + '"')
                csv_year.write('\n')
                year.add(i['year'])

            if i['@key'] not in art:
                csv_art.write('"' + i['@key'] + '","' + i["title"].replace('"', "'") + '"\n')
                art.add(i['@key'])
        except:
            pass

        if count > 10000:
            print('.')
            count = 0


if __name__ == '__main__':
    csv_autores = open('csv_autores.csv', 'a')
    csv_year = open('csv_year.csv', 'a')
    csv_pub = open('csv_pub.csv', 'a')
    csv_art = open('csv_art.csv', 'a')
    csv_pub.write('"Key","Titulo","Year","Autor"\n')
    csv_year.write('"Year"\n')
    csv_autores.write('"Autor"\n')
    csv_art.write('"Key","Titulo"\n')
    f = read_json('dblp_article.json')
    autores = set()
    year = set()
    art = set()
    print('Procesando json article...')
    save_csv(f, 'article')
    g = read_json('dblp_inproceedings.json')
    print('Procesando json inproceedings...')
    save_csv(g, 'inproceedings')
    print('Ficheros csv creados')
