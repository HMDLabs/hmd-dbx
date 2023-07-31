import json

f = open('../../test/stuff.json')
raw_schema = json.load(f)
f.close()

tables = dict()
columns = dict()
relations = dict()

class IDO:
    def __init__(self, content):
        self.ID = content['@uuid']
        self.content = content

    def graph_id(self):
        return self.ID.replace('-', '')

    def small_print(self, indent=""):
        print(indent + self.ID + ' ' + self.content['name'])
        # print(self.content)

    def as_rect(self, indent=""):
        print('rectangle ' + self.graph_id() + ' as "' + self.content['name'] + '"')

    def as_entity(self, indent=""):
        print('entity ' + self.graph_id() + ' as "' + self.content['name'] + '"')

class Table(IDO):
    def __init__(self, content):
        IDO.__init__(self, content)

class Column(IDO):
    def __init__(self, content):
        IDO.__init__(self, content)


def add_table(table_dict):
    t = Table(table_dict)
    tables[t.ID] = t


def parse_table(table_dict):
    # add_table(table_dict)
    if len(table_dict['dependent-tables']) > 0:
        for x in table_dict['dependent-tables']:
            if isinstance(x, dict):
                parse_base(x)


def parse_fks(table_dict):
    # add_table(table_dict)
    if len(table_dict['foreign-keys']) > 0:
        for x in table_dict['foreign-keys']:
            if isinstance(x, dict):
                table_ref = x['primary-key-table']
                if isinstance(table_ref, dict):
                    parse_base(x['primary-key-table'])


def parse_base(table_dict):
    add_table(table_dict)
    parse_table(table_dict)
    parse_fks(table_dict)


for i in raw_schema['all-table-columns']:
    c = Column(i)
    columns[c.ID] = c

for i in raw_schema['catalog']['tables']:
    if isinstance(i, dict):
        parse_base(i)



def dump_strings():
    #let's dump some values
    for i in tables.values():
        i.small_print()
        for c_id in i.content['columns']:
            columns[c_id].small_print("  ")

# dump_strings()

print("@startuml")
for i in tables.values():
    i.as_entity()
    print("together {")
    for c_id in i.content['columns']:
        columns[c_id].as_rect("  ")
        print(c_id.replace('-', '') + " <-- " + i.graph_id())
    print("}")

# dump the fks
for i in tables.values():
    for fk_entry in i.content['foreign-keys']:
        if isinstance(fk_entry, dict):
            #print(fk_entry['column-references'][0]['foreign-key-column'].replace('-', ''))
            print(fk_entry['column-references'][0]['foreign-key-column'].replace('-', '') + ' "*" <... "1" ' + fk_entry['column-references'][0]['primary-key-column'].replace('-', ''))
        #else:
            #print(fk_entry)


print("@enduml")