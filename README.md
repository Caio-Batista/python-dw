# Python Design Wizard

## Requiriments

### Python version over version 2.x
This version of Python Design Wizard uses (mainly) the [AST](https://docs.python.org/2/library/ast.html) api from the Python 2.x lib. It also runs with the [3.x version](https://docs.python.org/3.5/library/ast.html) of the api, but it was not the focus of this project so it may have some issues in some cases e.g.: Print, dict and calls entities.  

## Introduction 

### What is it?
The Python Design Wizard is a tool, and also an api, that uses the AST (Abstract syntax tree) of Python to find anti-patterns or *violations* in Python programs without having to run them in anyway. An example of AST in python:

![alt text](http://garethrees.org/2011/07/17/grammar/binop.png)

### Why should I use it?
First of all, this tool is way easier to use than the raw AST, that has some very useful options, but need abstraction to be used in different ways. The Python DW uses two forms of abstractions that are Relation and Entity. These two allow the user to search for patterns, check the tree for calls of specific functions and also to restrict the use of them too.  
Python DW can also be used to search slow algorithms based on their syntax. It comes along with an interactive module to execute your own *Design tests*, called [dw-check](https://github.com/Caio-Batista/python-dw#what-is-the-dw-check).

### How to use the API?
This tool is used like any api else. It creates the abstractions with side functions in the main module that can be found in [here](https://github.com/Caio-Batista/python-dw/blob/master/api/design_wizard.py). All the functions have their own documentations but are self explanned by their names and the section of the code that are found.

Next is an example how to use the tool:

```python
from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/file.py")
```
After this you can use the functions to create whatever restrictions or rule search that you want.

### What is the dw-check?
The **dw-check** is an interactive module that helps the user to filter functions and run tests of syntax using the api of Python DW, for all Python files in a certain directory. With a detailed command line interface, the user can create their own scripts with tests without having to create a class test or implement searching algorithms using the api. Those two things are already implemented with this module.

To get in to how to use the **dw-check**, see the [section bellow](https://github.com/Caio-Batista/python-dw#how-to-use-the-dw-check) or just run the following command:

```shell
$ ./dw-check help
```

### How to use the dw-check?
To make it easier to understand, this section will be divided in two parts (for each purpose), function restriction and script testing. 

#### Function restriction
This part of the **dw-check** uses the api to search for a costumizable group of functions through a directory for each Python file present in it. To use it is really simple, the only setup needed is a **json** file containing the functions to be found. Like bellow:

```shell
$ ./dw-check -f my/dir/functions.json -d my/dir/python_files/
```
**-f** stands for "functions" and **-d** stands for "directory".

In order for the **dw-check** to work properly the json file must be in this format, for the N funtions that the user wants to filter: 

```json
{"functions_not_allowed":["function1", "function2"]}
```
The result will be displayed as it follows:

```shell
$ ./dw-check -f my/dir/functions.json -d my/dir/python_files/

Directory: my/dir/python_files

. .  file1.py
function1 . file2.py
. function2 file3.py
function1 function2 file4.py

$

```


---
**NOTE**

It works with almost all markdown flavours (the below blank line matters).

---

### Is it tested?
Python DW has 100% of coverage in function testing, this tests can be found in the [test directory](https://github.com/Caio-Batista/python-dw/tree/master/tests). This tool is also self-tested, what means that the code tests itself with the abstract syntax tree. 
The test suite can be improved anytime by the user who can add new kinds of tests like *Design Tests*.

To execute the tests already developed just run the command:

```shell
$ ./run_tests.sh
```
The result of the command is a well detaled test suite run of each module of the tool. 

## Examples and sample data
The Python DW comes with an example of what you can do with this api. It's an interactive demo to search for calls of certain functions inside python modules in a certain directory. To use this demo just follow the next quick guide:

First of all open the [file](https://github.com/Caio-Batista/python-dw/blob/master/demo/restrict.json) and configure with functions that you want to detect, like this:

```json
{"functions_not_allowed":["sort", "min", "max", "map", "sum"]}
```

Then execute on your shell:
```shell
$ python2 -m demo.demo_interact
```

or for python 3: 

```shell
$ python3 -m demo.demo_interact
```

The demo will ask for a python directory:

```shell
$ python2 -m demo.demo_interact


======Type the name of directory to use Python DW=============


Directory: [path/to/dir]
```

Done, the demo will print file by file each and single one of the functions found acording to the json config file.

## Some important definitions

### Design Tests

### Violations

