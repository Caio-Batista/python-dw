import unittest, ast
from util.type_entity_enum import EntityTypeEnum
from util.type_relation_enum import RelationTypeEnum
from api.design_wizard import PythonDW
from design.function_node import FunctionNode


class TestDesignWizard(unittest.TestCase):
    
    def setUp(self):
        self.dw = PythonDW()
        self.dw.parse("tests/data/simple_module.py")
    
    
    def test_default_values(self):
        dw = PythonDW()
        self.assertEqual(dw.ast_tree, [])
        self.assertEqual(dw.entities, {})
        self.assertEqual(dw.ast_elements_dict,\
         {"class":ast.ClassDef, \
         "function":ast.FunctionDef, \
         "import":ast.Import, \
         "call":ast.Call, \
         "expr":ast.Expr })

    def test_values_after_parse_file_get_all_functions(self):
        self.assertEqual(self.dw.get_all_classes_str(), \
         ['Test','Test2'])
        self.assertEqual(self.dw.get_all_functions_str(), \
         ['func1','func2', 'inside_func'])
        self.assertEqual(self.dw.get_all_imports_str(), \
         ['Math','unittest'])

    def test_values_of_inner_functions(self):		
        self.assertEqual\
         (self.dw.get_functions_inside_class_str("Test2"), \
         ['inside_func'])

    def test_body_not_empty_function(self):	
        self.assertNotEqual\
         (self.dw.get_body_function("inside_func"), [])

    def test_get_fields_from_function(self):
        self.dw.create_function_entity_by_name("func2")
        function = self.dw.get_entity_by_name("func2")
        parameters = function.get_parameters_function_str()
        self.assertEqual(parameters, [])  
        
        self.dw.create_function_entity_by_name("func1")
        function = self.dw.get_entity_by_name("func1")
        parameters = function.get_parameters_function_str()
        self.assertEqual(parameters, ['r_param'])        			

    def test_get_element_by_name(self):
        self.assertEqual(self.dw.get_class_by_name("Test").name, 'Test')
        self.assertNotEqual(self.dw.get_class_by_name("Test"), [])
        
        self.assertEqual\
         (self.dw.get_function_by_name("func1").name, 'func1')         
        self.assertNotEqual(self.dw.get_function_by_name("func1"), [])
        
        self.assertEqual\
         (self.dw.get_import_by_name("Math").name, 'Math')
        self.assertNotEqual(self.dw.get_import_by_name("Math"), [])

    def test_get_entity_attribute_by_name(self):
        empty_node = FunctionNode("Empty",{})
        self.dw.entities["Empty"] = empty_node
        self.assertEqual\
         (self.dw.get_entity_by_name("Empty"), empty_node)


    def test_create_function_node_and_check_relation(self):
        
        ONLY_ELEMENT_LIST = 0
        
        self.dw.create_function_entity_by_name("func1")
        self.assertNotEqual(self.dw.entities, [])
        func_entity = self.dw.get_entity_by_name("func1")
        self.assertEqual(func_entity.get_name(), 'func1')
        
        self.assertNotEqual(func_entity.relations, {})
        
        relation = func_entity.get_relations_by_type\
         (RelationTypeEnum.HASFIELD)
        self.assertNotEqual(relation,[])
        self.assertEqual(type(relation), type([]))
        self.assertEqual\
         (relation[ONLY_ELEMENT_LIST].get_str_relation(), \
         'func1 HASFIELD r_param')
        
        
    def test_get_calls_inside_functions_body(self):
        self.dw.create_function_entity_by_name("func1")
        self.assertNotEqual(self.dw.entities, [])
        func_entity = self.dw.get_entity_by_name("func1")
        self.assertEqual(func_entity.get_function_calls_str(), \
         [ ('caller', ['func2']), ('callee', []) ] )
        self.assertEqual(func_entity.get_function_calls_str\
         (just_caller=True), ['func2'])        
        self.assertEqual(func_entity.get_function_calls_str\
         (just_callee=True), [])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase\
     (TestDesignWizard)
    unittest.TextTestRunner(verbosity=2).run(suite)


