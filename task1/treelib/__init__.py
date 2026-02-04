"""treelib: Binary/General Tree library with YAML integration

Provides a `Node` class that supports arbitrary children while keeping
`left`/`right` convenience properties for binary-style usage, plus
helper functions and YAML import/export.
"""
from typing import List, Optional
import yaml


class Node:
    def __init__(self, value=None, children: Optional[List['Node']]=None):
        self.value = value
        self.children: List[Optional[Node]] = children if children is not None else []

    # Binary compatibility: left/right map to children[0]/children[1]
    @property
    def left(self) -> Optional['Node']:
        return self.children[0] if len(self.children) > 0 else None

    @left.setter
    def left(self, node: Optional['Node']):
        if len(self.children) == 0:
            self.children.append(node)
        else:
            self.children[0] = node

    @property
    def right(self) -> Optional['Node']:
        return self.children[1] if len(self.children) > 1 else None

    @right.setter
    def right(self, node: Optional['Node']):
        while len(self.children) < 2:
            self.children.append(None)
        self.children[1] = node


def create_tree(root_value=None) -> Node:
    return Node(root_value)


def _traverse_to_parent_by_path(root: Node, path: str):
    """Return (parent_node, idx) where target is parent's child at idx.
    If path empty, parent is None and idx is None.
    Supports binary paths using 'L'/'R' and general numeric index paths using comma separators.
    """
    if not path:
        return None, None
    node = root
    # binary style
    if all(c in 'LR' for c in path):
        for c in path[:-1]:
            idx = 0 if c == 'L' else 1
            while len(node.children) <= idx:
                node.children.append(None)
            if node.children[idx] is None:
                node.children[idx] = Node()
            node = node.children[idx]
        final_idx = 0 if path[-1] == 'L' else 1
        return node, final_idx
    # numeric indices style: "0,2,1"
    parts = [p.strip() for p in path.split(',') if p.strip() != '']
    for p in parts[:-1]:
        idx = int(p)
        while len(node.children) <= idx:
            node.children.append(None)
        if node.children[idx] is None:
            node.children[idx] = Node()
        node = node.children[idx]
    final_idx = int(parts[-1])
    return node, final_idx


def add_node_by_path(root: Node, path: str, value) -> Node:
    """Add a node at `path` and set its value. Creates intermediate nodes as needed.
    Binary-style path example: "LLR" (L/R letters). General-style path example: "0,2,1".
    """
    if not path:
        root.value = value
        return root
    parent, idx = _traverse_to_parent_by_path(root, path)
    while len(parent.children) <= idx:
        parent.children.append(None)
    if parent.children[idx] is None:
        parent.children[idx] = Node(value)
    else:
        parent.children[idx].value = value
    return root


def delete_node_by_path(root: Node, path: str) -> Optional[Node]:
    """Delete the node at `path`. If path is empty, deletes entire tree (returns None).
    """
    if not path:
        return None
    parent, idx = _traverse_to_parent_by_path(root, path)
    if parent is None:
        return root
    if 0 <= idx < len(parent.children):
        # remove element for general trees; keep position for binary by setting None
        # If binary-style path (L/R) we'll keep None to preserve indices.
        if all(c in 'LR' for c in path):
            parent.children[idx] = None
        else:
            parent.children.pop(idx)
    return root


def edit_node_value(root: Node, path: str, new_value) -> Node:
    if not path:
        root.value = new_value
        return root
    parent, idx = _traverse_to_parent_by_path(root, path)
    while len(parent.children) <= idx:
        parent.children.append(None)
    if parent.children[idx] is None:
        parent.children[idx] = Node(new_value)
    else:
        parent.children[idx].value = new_value
    return root


def print_tree(root: Node, indent: int = 0, label: str = 'Root') -> None:
    if root is None:
        print('None')
        return
    prefix = ' ' * (4 * indent)
    print(f"{prefix}{label}:{root.value}")
    # If it's binary-like (<=2 children), label with L/R
    if not root.children:
        return
    if len(root.children) <= 2 and all((c is None) or isinstance(c, Node) for c in root.children):
        labels = ['L', 'R']
        for i in range(len(root.children)):
            child = root.children[i]
            lab = labels[i]
            if child is None:
                print(' ' * (4 * (indent + 1)) + f"{lab}---None")
            else:
                print_tree(child, indent + 1, label=f"{lab}---")
    else:
        for i, child in enumerate(root.children):
            lab = f"C{i}---"
            if child is None:
                print(' ' * (4 * (indent + 1)) + f"{lab}None")
            else:
                print_tree(child, indent + 1, label=lab)


def build_tree_from_yaml(yaml_file: str) -> Optional[Node]:
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return None

    def build(d) -> Optional[Node]:
        if d is None:
            return None
        val = d.get('value') if isinstance(d, dict) else d
        node = Node(val)
        # binary style
        if isinstance(d, dict) and ('left' in d or 'right' in d):
            left = build(d.get('left')) if d.get('left') is not None else None
            right = build(d.get('right')) if d.get('right') is not None else None
            node.children = []
            node.children.append(left)
            node.children.append(right)
        # generic children
        elif isinstance(d, dict) and 'children' in d:
            node.children = []
            for c in d.get('children') or []:
                node.children.append(build(c))
        return node

    return build(data)


def write_tree_to_yaml(root: Node, yaml_file: str) -> None:
    def serialize(node: Optional[Node]):
        if node is None:
            return None
        d = {'value': node.value}
        if node.children:
            # if it's binary-like (length <=2), use left/right keys
            if len(node.children) <= 2:
                left = serialize(node.children[0]) if len(node.children) > 0 else None
                right = serialize(node.children[1]) if len(node.children) > 1 else None
                if left is not None:
                    d['left'] = left
                if right is not None:
                    d['right'] = right
            else:
                d['children'] = [serialize(c) for c in node.children]
        return d

    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(serialize(root), f, sort_keys=False)


__all__ = [
    'Node', 'create_tree', 'add_node_by_path', 'delete_node_by_path', 'edit_node_value',
    'print_tree', 'build_tree_from_yaml', 'write_tree_to_yaml'
]
