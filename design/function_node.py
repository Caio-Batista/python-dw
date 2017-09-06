from design import entity
from util.type_entity_enum import * 

class FunctionNode(entity.Entity):

    def __init__(self, name, ast_node, parameters=[], fields=[], returns=[], function_calls=[]):
        entity.Entity.__init__(self,name=name,ast_node=ast_node)
        self.type_entity = EntityTypeEnum.FUNCTION
        self.parameters = parameters 
        self.fields = fields
        self.returns = returns
        self.function_calls = function_calls
    
    def get_name(self):
        if self.ast_node == {}:
            return self.name
        return self.ast_node.name 	

    def add_relation(self,relation):
        relation_type = relation.get_type_relation()
        value_dict = self.relations.get(relation_type)
        if value_dict is None:
            self.relations[relation_type] = [relation]
        else:
            self.relations[relation_type].append(relation)
            
    def get_relations_by_type(self, type_relation):
        return self.relations[type_relation]
                
