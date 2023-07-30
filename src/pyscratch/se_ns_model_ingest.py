import json

f = open('../../test/stuff.json')

raw_schema = json.load(f)

tables = dict()
columns = dict()
relations = dict()

class IDO:
    def __init__(self, content):
        self.ID = content['@uuid']
        self.content = content

    def small_print(self, indent=""):
        print(indent + self.ID + ' ' + self.content['name'])
        # print(self.content)

    def as_rect(self, indent=""):
        print('rectangle ' + self.ID.replace('-', '') + ' as "' + self.content['name'] + '"')

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

f.close()

def dump_strings():
    #let's dump some values
    for i in tables.values():
        i.small_print()
        for c_id in i.content['columns']:
            columns[c_id].small_print("  ")

# dump_strings()

print("@startuml")
for i in tables.values():
    i.as_rect()
    for c_id in i.content['columns']:
        columns[c_id].as_rect("  ")
        print(c_id.replace('-', '') + " ---> " + i.ID.replace('-', ''))
print("@enduml")