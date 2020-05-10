class Node:
    def __init__(self, start=-1, end=-1, suffix_start=-1, parent=None):
        self.parent = parent
        self.children = []
        self.start = start
        self.end = end
        # holds the start index of a suffix if this node is a leaf node
        self.suffix_start = suffix_start
        self.suffix_link = None

    def edge_length(self):
        end = self.end
        start = self.start
        return end - start + 1

    def add_suffix_link(self, node):
        self.suffix_link = node

    def __str__(self):
        output = ""
        # output += '\n'
        for child in self.children:
            output += "-{}".format(child.start)
            output += ",{}-".format(child.end)
        for child in self.children:
            output += '\n'
            output += child.__str__()
        return output


class SuffixTree:
    def __init__(self, word):
        self.word = word
        self.rootNode = Node()
        self.leaf_count = 0
        self.leaf = [None] * len(word)
        self.last_created_node = None
        self.end = -1
        self.active_length = 0
        self.active_node = None
        self.active_edge = -1

    def edge_length(self, node):
        return node.end - node.start + 1

    def implicit_tree(self):
        root = self.rootNode
        word = self.word
        word_len = len(word)
        i = 0
        while i < word_len:
            j = 0
            while j <= i:
                result = self.traverse(i, j, root)
                if result[2] == 1:
                    result[0].end += 1
                    j += 1
                elif result[2] == 2:
                    if result[1] == 0:
                        new_leaf = Node(j, i, j, result[0])
                        result[0].children.append(new_leaf)
                    else:
                        # in somewhere middle of the path
                        offset = result[1]
                        original_node = result[0]
                        original_start = original_node.start
                        parent_node = original_node.parent
                        # change the parent node of the original node to the internal node
                        internal_node = Node(original_start, offset - 1, -1, parent_node)
                        new_leaf = Node(j + offset - 1, i, j, internal_node)  # a little bug here, the start index is wrong, need to come up with a new solution
                        original_node.start = offset
                        parent_node.children[parent_node.children.index(original_node)] = internal_node
                        original_node.parent = internal_node
                        internal_node.children.append(original_node)
                        internal_node.children.append(new_leaf)
                    j += 1
                elif result[2] == 3:
                    break
            i += 1

    def traverse(self, i, j, node):
        current_node = node
        word = self.word
        children = node.children
        index = j
        offset = 0
        child_node = None
        for child in children:
            if word[child.start] == word[j]:
                child_node = child
                break
        if child_node is None:
            # the node is not created yet, rule two will be applied
            return (current_node, 0, 2)
        else:
            node_start = child_node.start
            node_end = child_node.end
            edge_len = self.edge_length(child_node)
            if i - j <= edge_len:
                # when the edge length >= the length of path we need to traverse, we do not skip, else we skip to the
                # place we want to operate directly.
                while index <= i and node_start <= node_end and word[index] == word[node_start]:
                    node_start += 1
                    index += 1
                    offset += 1     # denotes the index where an internal node should be created
                if node_start == node_end + 1:
                    # rule one will be applied
                    return (child_node, offset, 1)
                elif index <= i:
                    # rule two will be applied
                    return (child_node, offset, 2)
                elif node_start <= node_end and index == i + 1:
                    #rule 3 will be applied
                    return (child_node, -1, 3)
            else:
                return self.traverse(i, j + edge_len, child_node)

    # def extension_rule_applier(self, i, j):
    #     root = self.rootNode
    #     children = self.rootNode.children
    #     word = self.word
    #     node = None
    #     for child in children:
    #         if word[child.start] == word[j]:
    #             node = child
    #     if node is None:
    #         new_leaf = Node(j, i, j)
    #         root.children.append(new_leaf)
    #         if self.leaf[j] is not None:
    #             print("something wrong with leaf!")
    #         self.leaf[j] = new_leaf
    #     else:
    #         index = j
    #         edge_start = node.start
    #         already_exist = True
    #         while index <= i - 1:
    #
    #             edge_start += 1
    #             index += 1

    def extension_rule_1(self, i, leaf):
        leaf.end = i

    def extension_rule_2(self, i, j, parent_node):
        already_exist = False
        for child in parent_node.children:
            if child.start == j and child.end == i - 1:
                already_exist = True
                parent_node = child
        if already_exist:
            leaf_node = Node(j, i, j)
            parent_node.children.append(leaf_node)
        else:
            internal_node = Node(j, i - 1)
            internal_node.children.append(parent_node.children[j])
            parent_node.children[j] = internal_node
            """the above step is wrong as the parent node is not always the root. Fix this later """
            leaf_node = Node(j, i, j)
            internal_node.children.append(leaf_node)

    def find_node(self, i, j, word, node):
        for child in node.children:
            if word[child.start] == word[j]:
                pass
            else:
                return False
        return False


    def search(self, query_word):
        root = self.rootNode
        for char in query_word:
            char_not_found = True
            for child in root.children:
                if char == child.value:
                    root = child
                    char_not_found = False
            if char_not_found:
                return "Not found"
        search_result = ""
        for child in root.children:
            if child.end:
                search_result += child.value + " "
        return search_result

    def __repr__(self):
        return str(self.rootNode)
"""
    def trace_end(self, node: Node):
        max_occ = node.count_end()
        max_occ_word = node
        for child in node.children:
            if not child.end:
                child_trace_result = self.trace_end(child)
                if child_trace_result[0] > max_occ:
                    max_occ = child_trace_result[0]
                    max_occ_word = child_trace_result[1]
        return (max_occ, max_occ_word)

    def most_common_word(self, query_prefix):
        root = self.rootNode
        for char in query_prefix:
            char_not_found = True
            for child in root.children:
                if char == child.value:
                    root = child
                    char_not_found = False
            if char_not_found:
                return "Not found"
        result_word = self.trace_end(root)[1]
        result =[]
        while result_word.mother_node is not None:
            result.append(result_word.value)
            result_word = result_word.mother_node
        result.reverse()
        result = "".join(result)
        return result"""



li = {}
word = "abc"

print(li.get(word[0]))
s = SuffixTree("abad")
s.implicit_tree()
print(s.rootNode)

node = Node()
nodee = Node()
liq = []
liq.append(node)
liq.append(nodee)
print(liq.index(nodee))