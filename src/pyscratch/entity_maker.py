import json
import json_fix

f = open('../../test/inter.json')
raw_schema = json.load(f)
f.close()

f = open('northwind_graph_config.json')
graph_config = json.load(f)
f.close()


tables = dict()
columns = dict()
relations = dict()


class NamedObject:
    def __init__(self, content):
        self.content = content
        self.slug = content['slug']
        self.name = content['name']

    def __json__(self):
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        return self.__dict__

    def small_print(self, indent=""):
        print(indent + self.ID + ' ' + self.content['name'])
        # print(self.content)

    def as_rect(self, indent=""):
        print('rectangle ' + self.graph_id() + ' as "' + self.content['name'] + '"')

    def as_entity(self, indent=""):
        print('entity ' + self.graph_id() + ' as "' + self.content['name'] + '"')


class Table(NamedObject):
    def __init__(self, content):
        NamedObject.__init__(self, content)
        self.columns = list()

    def get_noun_dict(self):
        ret = {"name": self.name,
               "namespace": "lang_northwind",
               "metatype": "noun",
               "attributes": dict()}
        for c in self.columns:
            ret["attributes"][c.name] = (c.get_attribute_dict())
        return ret

class Column(NamedObject):
    def __init__(self, content):
        NamedObject.__init__(self, content)
        self.column_java_sql_type = content['column_java_sql_type']
        self.required = False

    def get_attribute_dict(self):
        '''
        The column as an attribute for an hmd entity (noun or relationship)
        :return:
        '''
        return {"name": self.name, "type": self.column_java_sql_type, "description" : "<todo>"}

#note we're only reading the public schema now - this will need updated with a more robust inter format
tab_list = raw_schema['public']
for tt in tab_list:
    t = Table(tt)
    tables[t.slug] = t
    for c in tt['columns']:
        new_col = Column(c)
        t.columns.append(new_col)
        columns[new_col.slug] = new_col



for k, v in tables.items():
    with open(f'../schemas/lang_northwinds/{v.name}.hmdentity', 'w') as f:
        json.dump(v.get_noun_dict(), f)

