import sys, os
sys.path.append(os.path.abspath(".."))
print(os.path.abspath(".."))
print(os.path.dirname(os.path.realpath(__file__)) + "/../")
print(os.path.dirname(os.getcwd()))