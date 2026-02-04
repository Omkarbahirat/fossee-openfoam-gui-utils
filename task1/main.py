from treelib import *

if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    print_tree(root)

    root = Node(10)
    print("Initial tree:")
    print_tree(root)

    # Add nodes
    print("\nAdding nodes:")
    add_node_by_path(root, "L", 5)
    add_node_by_path(root, "R", 15)
    add_node_by_path(root, "LL", 3)
    add_node_by_path(root, "LR", 7)
    add_node_by_path(root, "RL", 12)
    add_node_by_path(root, "RR", 18)
    print("\nTree after additions:")
    print_tree(root)

    yaml_file = "test.yaml"
    print(f"\nBuilding tree from '{yaml_file}':")
    yaml_tree_root = build_tree_from_yaml(yaml_file)
    if yaml_tree_root:
        print("\nTree built from YAML:")
        print_tree(yaml_tree_root)
