import sys
sys.path.insert(0, "./")

import os
import importlib
from inspect import getmembers, isfunction, getsourcelines

def get_tests(mod):
    # Get list of functions defined in mod with names that start with 'test'
    pred = lambda x: isfunction(x) and x.__module__ == mod.__name__ and x.__name__.startswith("test_")
    tests = list(getmembers(mod, pred))
    # Sort functions by order of declaration
    tests.sort(key=lambda x: getsourcelines(x[1])[1])
    return tests

# Get all .py files with names starting with 'tests_'
fns = os.listdir("tests")
fns = filter(lambda fn: fn.startswith("tests_") and fn.endswith(".py"), fns)
for fn in fns:
    mod = importlib.import_module(os.path.splitext(fn)[0])
    tests = get_tests(mod)
    print(f"Running test module {mod.__name__.lstrip('tests_')}")
    for test_name, test_fn in tests:
        print(f" > Running test '{test_name}'... ", end="")
        test_fn()
        print("Success")

print("All tests successful")
