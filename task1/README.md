Task 1 – Binary Tree with YAML Integration
Overview

This project implements a binary tree data structure as an installable Python package and provides utilities to:

Create and manipulate a binary tree

Add, delete, edit, and print nodes

Serialize a binary tree to a YAML file

Deserialize a YAML file into a binary tree

The project is part of the CFD-FOSSEE Screening Task (Task 1) and is designed to demonstrate:

Clean package structure

Modular design

YAML integration

Testability and ease of installation

Project Structure
task1_binary_tree/
├── tree/
│   ├── __init__.py
│   ├── node.py          # Node class definition
│   ├── operations.py   # Binary tree operations
│   └── yaml_io.py      # YAML read/write utilities
├── tests/
│   ├── test_script.py  # Test & demonstration script
│   └── test.yaml       # Sample YAML file
├── setup.py
├── requirements.txt
└── README.md


Each file has a single responsibility, and all functionality is accessed via clean imports.

Requirements

Python 3.8+

External dependency:

PyYAML

Install dependencies using:

pip install -r requirements.txt

Installation

From the project root directory:

pip install .


This installs the package so it can be imported from anywhere.

Usage
Importing the Package
from tree.node import Node
from tree.operations import (
    add_node_by_path,
    delete_node_by_path,
    edit_node_value,
    print_tree
)
from tree.yaml_io import (
    build_tree_from_yaml,
    write_tree_to_yaml
)

Creating and Manipulating a Tree
root = Node(10)

add_node_by_path(root, "L", 5)
add_node_by_path(root, "R", 15)
add_node_by_path(root, "LL", 3)
add_node_by_path(root, "LR", 7)

print_tree(root)

YAML → Binary Tree
root = build_tree_from_yaml("tests/test.yaml")
print_tree(root)

Binary Tree → YAML
write_tree_to_yaml(root, "output.yaml")

Running Tests / Demo

A simple test and demonstration script is provided.

From the project root:

python tests/test_script.py


This script:

Creates a binary tree manually

Adds nodes using path-based insertion

Prints the tree

Builds a tree from a YAML file

Prints the YAML-generated tree

No guessing or configuration is required.

YAML Format

Example test.yaml:

value: 10
left:
  value: 5
  left:
    value: 3
  right:
    value: 7
right:
  value: 15
  right:
    value: 18


Each node uses:

value

left (optional)

right (optional)

Design Decisions

Modular design: Node logic, tree operations, and YAML I/O are separated

Installable package: Can be installed via pip

Path-based traversal: Simple and explicit (L, R)

Readable output: Tree printing uses indentation for clarity

Evaluator-friendly: Clear structure, minimal dependencies, deterministic tests

Notes

This implementation focuses on correctness and clarity rather than balancing or optimization.

Bonus feature (general tree) is not implemented in this version.

Author

Omkar Bahirat
CFD-FOSSEE Screening Task Submission