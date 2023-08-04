import json

f = open('../../test/inter.json')
raw_schema = json.load(f)
f.close()

f = open('northwind_graph_config.json')
graph_config = json.load(f)
f.close()

f = open('typemap.json')
type_map_config = json.load(f)
f.close()

tables = dict()
columns = dict()
ns_relationships = dict()
schemas = dict()

def typemap(java_sql_type):
    return type_map_config[java_sql_type]["ns_type"]


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
        self.ignore_fks = dict()

    def get_ns_dict(self, ns_type="noun"):
        ret = {"name": self.name,
               "namespace": "lang_northwind",
               "metatype": ns_type,
               "attributes": dict()}
        for c in self.columns:
            if c.slug not in self.ignore_fks:
                ret["attributes"][c.name] = (c.get_attribute_dict())
        return ret

    def mark_fk_for_ignore(self, key_to_ignore):
        self.ignore_fks[key_to_ignore] = True



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
        return {"name": self.name,
                "type": typemap(self.column_java_sql_type),
                "java_sql_type": self.column_java_sql_type,
                "description": self.content["remarks"],
                "required": self.content["is_nullable"] }


schemas_to_namespace = {"public": "northwind"}

# note we're only reading the public schema now - this will need updated with a more robust inter format

for schema in raw_schema['schemas']:
    #tab_list = schema[schemas]
    for tt in schema["tables"]:
        t = Table(tt)
        tables[t.slug] = t
        for c in tt['columns']:
            new_col = Column(c)
            t.columns.append(new_col)
            columns[new_col.slug] = new_col

for k, v in tables.items():
    dict_to_write = dict()
    if v.name in graph_config["m2m_to_relationship"]:
        # if a table is m2m overridden
        # create relation from table with attributes
        # remove/hide FKs

        imported_key0 = v.content["imported_foreign_keys"][0]
        imported_key1 = v.content["imported_foreign_keys"][1]
        v.mark_fk_for_ignore(imported_key0["column_refs"][0]["foreign_key_column"])
        v.mark_fk_for_ignore(imported_key1["column_refs"][0]["foreign_key_column"])
        dict_to_write = v.get_ns_dict(ns_type="relationship")
        dict_to_write["ref_from"] = f'lang_northwind.{tables[(imported_key0["pk_table"])].name}'
        dict_to_write["ref_to"] = f'lang_northwind.{tables[(imported_key1["pk_table"])].name}'

        with open(f'../schemas/lang_northwind/{v.name}.hms', 'w') as f:
            json.dump(dict_to_write, f)
    else:
        # for a given table, we want to output:
        # a noun if it is not overridden,
        # for each fk TO noun, remove FK, create relationship.
        # repeat, write all.
        dict_to_write = v.get_ns_dict()
        outbound_fks = v.content["outbound_foreign_keys"]
        for fk in outbound_fks:
            fk_table = tables[fk["fk_table"]]
            #don't create FK relationships for m2m overriden tables
            if fk_table.name not in graph_config["m2m_to_relationship"]:
                new_rel_name = f'{v.name}_has_{fk_table.name}'
                new_relationship = {"name": new_rel_name,
                                    "namespace": "lang_northwind",
                                    "metatype": "relationship",
                                    "attributes": dict(),
                                    "ref_from": f'lang_northwind.{v.name}',
                                    "ref_to": f'lang_northwind.{fk_table.name}'
                                    }
                # save the new relationship
                ns_relationships[new_rel_name] = new_relationship
                with open(f'../schemas/lang_northwind/{new_rel_name}.hms', 'w') as f:
                    json.dump(new_relationship, f)

                #remove the column refs from the target tables
                for col_ref in fk["column_refs"]:
                    fk_col = col_ref["foreign_key_column"]
                    #print(f'Removing Column Ref {fk_col} from {fk_table.slug}')
                    tables[fk_table.slug].mark_fk_for_ignore(fk_col)
            else:
                print(f'ignoring target table: {fk_table.name}')

#write the tables now that they have the ignores set
for k, v in tables.items():
    #ignore the overriden
    if v.name not in graph_config["m2m_to_relationship"]:
        dict_to_write = v.get_ns_dict()
        with open(f'../schemas/lang_northwind/{v.name}.hms', 'w') as f:
            json.dump(dict_to_write, f)

print(f'New Relationships: {len(ns_relationships)}')
