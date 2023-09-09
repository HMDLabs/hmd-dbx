schemacrawler.sh --command=template --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=$1 --info-level=standard --templating-language=velocity --template "intermediate_json.vm" > ../../test/$1.json


#schemacrawler.sh --command=template --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=northwind --info-level=standard --templating-language=velocity --template "intermediate_json.vm" > ../../test/inter.json
#schemacrawler.sh --command=template --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=pagila --info-level=standard --templating-language=velocity --template "intermediate_json.vm" > ../../test/inter_2.json

#python3 entity_maker.py $1
