from lxml import etree
import json


def tranform_to_json(xml, tag, f):
    #count = 0
    print('Transformado del fichero', xml, 'las etiquetas', tag, 'a json...')
    events = ("start", "end")
    e = '{"'
    e += tag
    e += '": [ \n'
    with open(f, 'w', encoding='UTF-8') as file:
        file.write(e)
    dtd = etree.DTD(file='dblp.dtd')
    for event, element in etree.iterparse(xml, load_dtd=dtd, encoding="ISO-8859-1", events=events, tag=tag):
        # count += 1
        e = {}
        if event == "start":
            e["@key"] = element.attrib['key']
            try:
                for child in element:
                    try:
                        e[child.tag] = int(child.text)
                    except ValueError:
                        if child.tag in e:
                            if type(e[child.tag]) == str:
                                e[child.tag] = [e[child.tag], child.text]
                            else:
                                e[child.tag].append(child.text)
                        else:
                            e[child.tag] = child.text
                with open(f, 'a', encoding='UTF-8') as file:
                    file.write(',')
                    file.write(json.dumps(e))
            except:
                pass

        #if count > 1000:
        #   break

    e = ']} \n'
    with open(f, 'a', encoding='UTF-8') as file:
        file.write(e)
    print('Transformado y guardado en ', f)


if __name__ == '__main__':
    tranform_to_json('dblp.xml', 'article', 'dblp_article.json')
    tranform_to_json('dblp.xml', 'inproceedings', 'dblp_inproceedings.json')
    tranform_to_json('dtlp.xml', 'incollection', 'dblp_incollection.json')
