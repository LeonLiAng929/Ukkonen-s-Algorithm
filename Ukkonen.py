class Node:
    def __init__(self, start=-1, end=-1, suffix_start=-1, suffix_link=None):
        # self.parent = parent
        self.children = []
        self.start = start
        self.end = end
        # holds the start index of a suffix if this node is a leaf node
        self.suffix_start = suffix_start
        self.suffix_link = suffix_link

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


class GlobalEnd:
    def __init__(self):
        self.global_end = -1

    def increment(self):
        self.global_end += 1

    def __int__(self):
        return self.global_end

    def __repr__(self):
        return str(self.global_end)


class SuffixTree:
    def __init__(self, word):
        self.word = word
        self.rootNode = Node()
        self.leaf = [None] * len(word)
        self.last_created_node = None  # will be used to assist suffix link assignment
        self.end = GlobalEnd()
        self.active_length = 0
        self.active_node = None
        self.active_edge = -1
        self.remaining = 0  # denotes how many suffixes that need to be insert at the end of each phase

    def edge_length(self, node):
        return int(node.end) - node.start + 1

    def build_implicit_tree(self):
        word = self.word
        word_len = len(word)
        i = 0
        self.active_node = self.rootNode
        while i < word_len:
            # extension rule 1
            self.end.increment()  # rapid leaf extension
            self.remaining += 1
            self.last_created_node = None
            while self.remaining > 0:
                if self.active_length == 0:
                    self.active_edge = i
                result = self.traverse(i)
                if result[0] == 2:
                    # extension rule 2, case one
                    if result[1] is None:
                        new_leaf = Node(i, self.end, i, self.rootNode)
                        self.active_node.children.append(new_leaf)
                        if self.last_created_node is not None:
                            self.last_created_node.add_suffix_link(self.active_node)
                            self.last_created_node = None
                    else:
                        # in somewhere middle of the path
                        original_node = result[1]
                        original_start = original_node.start
                        parent_node = self.active_node
                        offset = self.active_length + original_node.start
                        if original_node == parent_node:
                            # this means there is already an internal node, no need to create a new one
                            new_leaf = Node(i, self.end, i - offset, self.rootNode)
                            # internal_node = original_node
                            original_node.children.append(new_leaf)
                        else:
                            internal_node = Node(original_start, offset - 1, -1, self.rootNode)
                            new_leaf = Node(i, self.end, i - offset, self.rootNode)
                            original_node.start = offset
                            # change the parent node of the original node to the internal node
                            parent_node.children[parent_node.children.index(original_node)] = internal_node
                            internal_node.children.append(original_node)
                            internal_node.children.append(new_leaf)

                        if self.last_created_node is not None:
                            self.last_created_node.add_suffix_link(internal_node)
                        self.last_created_node = internal_node
                elif result[0] == 3:
                    # extension rule 3
                    break
                elif result[0] == 1:
                    # skip the current active node and start all over again.
                    continue
                self.remaining -= 1
                if self.active_node != self.rootNode:
                    self.active_node = self.active_node.suffix_link
                else:
                    if self.active_length > 0:
                        self.active_length -= 1
                        self.active_edge = i - self.remaining + 1
            i += 1

    def build_tree(self):
        self.word += '$'
        self.build_implicit_tree()

    def traverse(self, i):
        """

        :param i: current phase
        :return: (1,None): this is when traversing down a node, the edge length of that node is less than the length
        of the path we are traversing, so we skip this node and start all over from the next node.
        (2, None): this happens when there is no edge starting with a char, so we create a leaf node.
        (2, child_node): this happens when we stuck in the middle of an edge of a node, and word[i] != the char at
        where we stuck, so we create an internal node and a new leaf from there.
        """
        current_node = self.active_node
        child_node = None
        children = current_node.children
        for child in children:
            if self.word[child.start] == self.word[self.active_edge]:
                child_node = child
                break
        if child_node is None:
            # at the end of a node, it has no outgoing edge(child node), so apply rule two
            # this is the case one for rule 2
            return (2, None)
        else:
            child_node_len = self.edge_length(child_node)
            # skip to the next node if the edge_length is less than the path_length
            if child_node_len <= self.active_length:
                self.active_length -= child_node_len
                self.active_edge += child_node_len
                self.active_node = child_node
                return (1, None) # 1 represents skip
            if self.word[i] == self.word[self.active_length + child_node.start]:
                # char already exists, rule 3 will be applied
                self.active_length += 1
                if self.last_created_node is not None:
                    if self.active_node != self.rootNode:
                        self.last_created_node.add_suffix_link(self.active_node)
                        self.last_created_node = None
                return (3, None) # second place is of no use, just set it to be None
            else:
                # in somewhere middle of the path, rule two will be applied, this is the case two of
                # rule two
                return (2, child_node)

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



s = SuffixTree("oooo$")
s.build_implicit_tree()
print(s.rootNode)


