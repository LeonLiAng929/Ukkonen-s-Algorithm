class Node:
    def __init__(self, start=-1, end=-1, suffix_start=-1):
        self.children = []
        self.start = start
        self.end = end
        #self.mother_node = None
        # holds the start index of a suffix if this node is a leaf node
        self.suffix_start = suffix_start

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
    def __init__(self):
        self.rootNode = Node()

    def add_word(self, word):
        root = self.rootNode
        children = self.rootNode.children
        word_len = len(word)
        i = 0
        if len(children) == 0:
            new_node = Node(i, i, i)
            children.append(new_node)
        while i < word_len:
            new_char = word[i]
            node = Node(i, i, i)
            j = 0
            while j < i:
                if len(children) == j:
                    pass

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



