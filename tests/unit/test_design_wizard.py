import unittest, ast
from api.design_wizard import PythonDW
from design.function_node import FunctionNode


class TestDesignWizard(unittest.TestCase):
    
    def setUp(self):
        self.dw = PythonDW()
        self.dw.parse("tests/data/simple_module.py")
    
    
    def test_default_values(self):
        dw = PythonDW()
        self.assertEqual(dw.ast_tree, [])
        self.assertEqual(dw.ast_elements_dict,\
         {"class":ast.ClassDef, \
         "function":ast.FunctionDef, \
         "import":ast.Import })

    def test_values_after_parse_file_get_all_functions(self):
        self.assertEqual(self.dw.get_all_classes_str(), ['Test','Test2'])
        self.assertEqual(self.dw.get_all_functions_str(), ['func1','func2', 'inside_func'])
        self.assertEqual(self.dw.get_all_imports_str(), ['Math','unittest'])

    def test_values_of_inner_functions(self):		
        self.assertEqual(self.dw.get_functions_inside_class_str("Test2"), ['inside_func'])

    def test_body_not_empty_function(self):	
        self.assertNotEqual(self.dw.get_body_function("inside_func"), [])

    def test_get_fields_from_function(self):
        self.assertEqual(self.dw.get_fields_function_str("func1"), ['oi'])       			

    def test_get_element_by_name(self):
        self.assertEqual(self.dw.get_class_by_name("Test").name, 'Test')
        self.assertNotEqual(self.dw.get_class_by_name("Test"), [])
        
        self.assertEqual(self.dw.get_function_by_name("func1").name, 'func1')         
        self.assertNotEqual(self.dw.get_function_by_name("func1"), [])
        
        self.assertEqual(self.dw.get_import_by_name("Math").name, 'Math')
        self.assertNotEqual(self.dw.get_import_by_name("Math"), [])

    def test_get_entity_attribute_by_name(self):
        empty_node = FunctionNode("Empty")
        self.dw.entities.append(empty_node)
        self.assertEqual(self.dw.get_entity_attr_by_name("Empty"), empty_node)


    def test_create_function_node(self):
        self.dw.create_function_entity_by_name("func1")
        self.assertNotEqual(self.dw.entities, [])
        func_entity = self.dw.get_entity_attr_by_name("func1")
        self.assertEqual(func_entity.get_name(), 'func1')
        


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDesignWizard)
    unittest.TextTestRunner(verbosity=2).run(suite)


