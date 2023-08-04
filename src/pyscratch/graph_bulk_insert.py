from hmd_entity_storage.engines.gremlin_engine import GremlinEngine


graph_engine = GremlinEngine("localhost", protocol="ws", with_strategies=False)

inst = Noun()

graph_engine.put_noun(inst)

rel = Relationship()
graph_engine.put_relationship(rel)
