class FileSystemNode:
    def __init__(self, name, is_directory=False, size=0):
        self.name = name
        self.is_directory = is_directory
        self.size = size
        self.children = {}

    def add_child(self, child_node):
        self.children[child_node.name] = child_node

    def remove_child(self, name):
        if name in self.children:
            del self.children[name]


class FileSystem:
    def __init__(self):
        self.root = FileSystemNode("/", is_directory=True)

    def find_node(self, path):
        parts = path.strip("/").split("/")
        current_node = self.root
        for part in parts:
            if part in current_node.children:
                current_node = current_node.children[part]
            else:
                return None
        return current_node

    def create(self, path, name, is_directory=False, size=0):
        parent_node = self.find_node(path)
        if parent_node and parent_node.is_directory:
            new_node = FileSystemNode(name, is_directory, size)
            parent_node.add_child(new_node)
            return True
        return False

    def delete(self, path):
        parts = path.strip("/").split("/")
        node_name = parts.pop()
        parent_path = "/" + "/".join(parts)
        parent_node = self.find_node(parent_path)
        if parent_node and node_name in parent_node.children:
            parent_node.remove_child(node_name)
            return True
        return False

    def move(self, source_path, dest_path):
        parts = source_path.strip("/").split("/")
        node_name = parts.pop()
        source_parent_path = "/" + "/".join(parts)
        source_parent_node = self.find_node(source_parent_path)
        dest_node = self.find_node(dest_path)
        if source_parent_node and dest_node and node_name in source_parent_node.children and dest_node.is_directory:
            node_to_move = source_parent_node.children.pop(node_name)
            dest_node.add_child(node_to_move)
            return True
        return False

    def search(self, name, current_node=None, path=""):
        if current_node is None:
            current_node = self.root

        found_nodes = []
        if current_node.name == name:
            found_nodes.append(path + "/" + current_node.name)

        if current_node.is_directory:
            for child_name, child_node in current_node.children.items():
                found_nodes.extend(self.search(name, child_node, path + "/" + current_node.name))

        return found_nodes

    def display_tree(self, node=None, indent=""):
        if node is None:
            node = self.root
        print(indent + node.name)
        if node.is_directory:
            for child in node.children.values():
                self.display_tree(child, indent + "  ")

    def analyze(self, path):
        node = self.find_node(path)
        if node is None:
            return None
        return self._analyze_node(node)

    def _analyze_node(self, node):
        total_size = 0
        file_count = 0
        if node.is_directory:
            for child in node.children.values():
                child_size, child_count = self._analyze_node(child)
                total_size += child_size
                file_count += child_count
        else:
            total_size = node.size
            file_count = 1
        return total_size, file_count
