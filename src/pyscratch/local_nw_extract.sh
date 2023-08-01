#schemacrawler.sh --command=serialize --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=northwind --info-level=standard --output-format=json > ../../test/stuff.json
schemacrawler.sh --command=template --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=northwind --info-level=standard --templating-language=velocity --template "intermediate_json.vm" > inter.json

#schemacrawler.sh --command=schema --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=northwind --info-level=standard --output-format=html

#schemacrawler.sh -h

#schemacrawler.sh --command=script --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=northwind --info-level=standard --script=sc_plantuml.py > sc_puml.puml


#schemacrawler.sh --command=schema --host=localhost --port=5432 --user=postgres --password=admin --server=postgresql --database=northwind --info-level=standard -F html > report.html