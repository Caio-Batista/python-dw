import ast
from copy import copy
from util.type_entity_enum import EntityTypeEnum
from util.type_relation_enum import RelationTypeEnum
from util.type_ast_entity_enum import AstEntityTypeEnum
from design.relation.relation import Relation
from design.class_node import ClassNode
from design.function_node import FunctionNode 
from design.field_node import FieldNode
from design.parameter_node import ParameterNode


class PythonDW:
    """Python Design Wizard API"""
    
    
    def __init__(self):
        self.ast_tree = []
        self.entities = {}
        self.ast_elements_dict = AstEntityTypeEnum.ast_entity_dict
		 
    def parse(self, file_path):
        read_file = open(file_path,'r')
        self.ast_tree = ast.parse(read_file.read())
        
        for node in ast.walk(self.ast_tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        
    def get_entity_by_name(self,name):
        entity = self.entities.get(name)
        if entity is None:
            entity = ""
        return entity 
        
    def get_entity_by_type(self,type_entity):
        entities_return_fields = []
        entities_return_functions = []
        entities = self.entities
        for k,v in entities.items():
            if (type(v) == type([])) and isinstance(v[0], FieldNode):
                entities_return_fields += v  
            elif isinstance(v,type_entity):
                entities_return_functions.append(v)      
        if type_entity == FieldNode:
            return entities_return_fields 
        elif type_entity == FunctionNode:
            return entities_return_functions         
            
    
    def delete_entity_by_name(self, name):
        del self.entities[name]

    def delete_all_entities(self):
        self.entities = {}               
    
    def is_leaf_from_branch(self, branch_node, leaf):
        response = False
        while (not isinstance(leaf.ast_node, self.ast_elements_dict['module'])):
            if leaf.ast_node.parent != branch_node.ast_node:
                leaf.ast_node = leaf.ast_node.parent
            else:
                response = True
                break
        return response            

    """ Returning nodes functions """ 


    def get_all_elements_file(self, key):
        list_elements = []
        for node in ast.walk(self.ast_tree): 
            if isinstance(node, self.ast_elements_dict[key]):
                list_elements.append(node)
        return list_elements
    
    def get_everything(self):
        list_elements = []
        for node in ast.walk(self.ast_tree):
            list_elements.append(node)
        return list_elements    
    
    def get_all_fields_without_class_func(self):
        return self.get_all_elements_file('augassign') + \
         self.get_all_elements_file('assign') + \
         self.get_all_elements_file('call') + \
         self.get_all_elements_file('for') + \
         self.get_all_elements_file('load') + \
         self.get_all_elements_file('store') + \
         self.get_all_elements_file('index') + \
         self.get_all_elements_file('subscript') + \
         self.get_all_elements_file('if')
          					

    def get_all_classes(self):
        return self.get_all_elements_file('class')
		
    def get_all_functions(self):
        return self.get_all_elements_file('function')

    def get_all_imports(self):
        all_imports = []
        imports = self.get_all_elements_file('import')
        for node in imports:
            for single_import in node.names:
                if single_import not in all_imports:
                    all_imports.append(single_import)
        return all_imports
 
   
    def get_class_by_name(self,name):
        class_found = []
        classes = self.get_all_classes()
        for clas in classes:
            if clas.name == name:
                class_found = clas
        return class_found        
    
    def get_function_by_name(self,name):
        function_found = []
        functions = self.get_all_functions()
        for func in functions:
            if func.name == name:
                function_found = func
        return function_found 
    
    def get_import_by_name(self,name):
        import_found = []
        imports = self.get_all_imports()
        for imp in imports:
            if imp.name == name:
                import_found = imp
        return import_found        
    				 
    def create_function_entity_by_name(self, name):
        function_node = self.get_function_by_name(name)
        self.create_function_entity(function_node)

    def create_class_entity_by_name(self, name):
        class_node = self.get_class_by_name(name)
        self.create_class_entity(class_node)


 
    """ CREATION ENTITY FUNCTIONS """
    
    #TODO(Caio) Needs update
    def create_class_entity(self, node):
        class_entity = ClassNode("temporary_name", ast_node=node)
        class_entity.set_name_to_ast_name()
        name = class_entity.get_name()
        self.entities[name] = class_entity
        
    def create_function_entity(self, node):
        function_entity = FunctionNode\
         ("temporary_name", ast_node=node)
        function_entity.set_name_to_ast_name()
        name = function_entity.get_name() 
        
        # Only creates if is not in entity dict 
        if self.get_entity_by_name("def_" + name) == "":
            self.entities["def_" + name] = function_entity
            calls = function_entity.get_function_calls_str\
             (just_caller=True)
            for call in calls:
                if self.get_entity_by_name("def_" + call) != "":
                    self.get_entity_by_name("def_" + call).add_callee\
                     (function_entity)
                elif self.get_function_by_name(call) != []:
                    node_function_callee = \
                     self.get_function_by_name(call) 
                    classe = function_entity.__class__ 
                    function_callee = classe\
                     ("temporary_name2", ast_node=node_function_callee)
                    function_callee.set_name_to_ast_name()
                    callee_name = function_callee.get_name() 
                    function_callee.add_callee(function_entity)
                    self.entities["def_" + callee_name] = function_callee
    
    def create_field_entity(self,node): 
        parent = node.parent
        grand_parent = {}
        field_node = {}

        if not isinstance(parent, ast.Module):
            grand_parent = parent.parent            
            
        if isinstance(node, self.ast_elements_dict['for']):
            field_node = FieldNode("for", ast_node=node, is_loop=True)
            if self.entities.get("for") is None:
                field_node.set_name("for1")                
                self.entities["for"] = [field_node]
            else:
                field_node.set_name('for'+ str(len(self.entities["for"]) + 1))
                self.entities["for"].append(field_node)  

        if isinstance(node, self.ast_elements_dict['if']):
            field_node = FieldNode("if", ast_node=node, is_loop=False)
            if self.entities.get("if") is None:
                field_node.set_name("if1")                
                self.entities["if"] = [field_node]
            else:
                field_node.set_name('if'+ str(len(self.entities["if"]) + 1))
                self.entities["if"].append(field_node)  
                  
        if isinstance(node, self.ast_elements_dict['assign']) or \
         isinstance(node, self.ast_elements_dict['augassign']): 
            node = node.value
            
        if isinstance(node, self.ast_elements_dict['call']):

            if isinstance(node.func, self.ast_elements_dict['attribute']):
                field_node = FieldNode(node.func.attr, ast_node=node, is_call=True, is_attribute=True)
                if isinstance(node.func.value, self.ast_elements_dict['call']):
                    field_node_value = FieldNode("Temporary_name", ast_node=node.func.value, is_call=True, is_attribute=False)
                    field_node_value.set_name_to_ast_name()
                    relation = Relation(field_node, RelationTypeEnum.ISCALLED, field_node_value)
                    field_node.add_relation(relation)
                
            elif isinstance(node.func, self.ast_elements_dict['call']):
                if isinstance(node.func.func, self.ast_elements_dict['call']):
                    field_node = FieldNode(node.func.func.id, ast_node=node, is_call=True, is_attribute=False)
                else:
                    field_node = FieldNode("call", ast_node=node, is_call=True, is_attribute=False)
                    field_node.set_name_to_ast_name()    
            else:
                field_node = FieldNode("call", ast_node=node, is_call=True, is_attribute=False)    
                field_node.set_name_to_ast_name()

            if self.entities.get(field_node.get_name()) is None:
                self.entities[field_node.get_name()] = [field_node]
            else:
                self.entities[field_node.get_name()].append(field_node)
        else:
            if isinstance(node, self.ast_elements_dict['index']):
                field_node = FieldNode("index", ast_node=node, is_index=True)
            elif isinstance(node, self.ast_elements_dict['subscript']):
                field_node = FieldNode("subscript", ast_node=node, is_subscript=True)
            elif isinstance(node, self.ast_elements_dict['tuple']):      
                field_node = FieldNode("tuple", ast_node=node, is_subscript=True)
            elif isinstance(node, self.ast_elements_dict['assign']) or \
              isinstance(node, self.ast_elements_dict['call']):
                create_field_entity(node.value)  
            
            if field_node != {}:
                if self.entities.get("assign_field") is None:
                    self.entities["assign_field"] = [field_node]
                else:
                    self.entities["assign_field"].append(field_node)                  
                              

            


    """ Returning strings functions """


    def get_all_classes_str(self):
        classes = [e.name for e in self.get_all_classes()]
        return classes 

    def get_all_functions_str(self):
        functions = [e.name for e in self.get_all_functions()]
        return functions
	
    def get_all_imports_str(self):
        imports = [e.name for e in self.get_all_imports()]
        return imports

    def get_functions_inside_class_str(self, name):
        functions = \
         [e.name for e in self.get_functions_inside_class(name)]
        return functions
 
