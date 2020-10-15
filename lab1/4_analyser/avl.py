class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.__root = None

# region Private

# region Rotations

    def __ll(self, a):
        """
                a             b
               / \           / \
              b   ar   ->   c   a
             / \           / \  / \
            c   br        cl cr br ar
           / \
          cl  cr
        """
        b = a.left
        br = b.right

        # Rotation
        b.right = a
        a.left = br

        # Affected nodes
        a.height = 1 + max(self.__get_height(a.left),
                           self.__get_height(a.right))
        b.height = 1 + max(self.__get_height(b.left),
                           self.__get_height(b.right))

        return b

    def __lr(self, a):
        """
                a              c
               / \           /   \
              b   ar   ->   b     a
             / \           / \   / \
            bl  c         bl cl cr ar
               / \
              cl cr
        """
        b = a.left
        c = b.right
        cl = c.left
        cr = c.right

        # Rotation
        c.right = a
        c.left = b
        b.right = cl
        a.left = cr

        # Affected nodes
        a.height = 1 + max(self.__get_height(a.left),
                           self.__get_height(a.right))
        b.height = 1 + max(self.__get_height(b.left),
                           self.__get_height(b.right))
        c.height = 1 + max(self.__get_height(c.left),
                           self.__get_height(c.right))

        return c

    def __rl(self, a):
        """
                a             c
               / \          /   \
              al  b   ->   a     b
                 / \      / \   / \
                c  br    al cl cr br
               / \
              cl cr
        """
        b = a.right
        c = b.left
        cl = c.left
        cr = c.right

        # Rotation
        c.right = b
        c.left = a
        b.left = cr
        a.right = cl

        # Affected nodes
        a.height = 1 + max(self.__get_height(a.left),
                           self.__get_height(a.right))
        b.height = 1 + max(self.__get_height(b.left),
                           self.__get_height(b.right))
        c.height = 1 + max(self.__get_height(c.left),
                           self.__get_height(c.right))

        return c

    def __rr(self, a):
        """
                a              b
               / \           /   \
             al   b   ->    a     c
                 / \       / \   / \  
                bl  c     al bl cl cr 
                   / \
                  cl cr
        """
        b = a.right
        bl = b.left

        # Rotation
        b.left = a
        a.right = bl

        # Affected nodes
        a.height = 1 + max(self.__get_height(a.left),
                           self.__get_height(a.right))
        b.height = 1 + max(self.__get_height(b.left),
                           self.__get_height(b.right))

        return b

# endregion

# region Traversal

    def __preorder_rec(self, node, only_values):
        if not node:
            return []

        nodes = []
        if only_values:
            nodes.append(node.value)
        else:
            nodes.append(node)

        nodes.extend(self.__preorder_rec(node.left, only_values))
        nodes.extend(self.__preorder_rec(node.right, only_values))
        return nodes

    def __inorder_rec(self, node, only_values):
        if not node:
            return []

        nodes = []
        nodes.extend(self.__inorder_rec(node.left, only_values))
        if only_values:
            nodes.append(node.value)
        else:
            nodes.append(node)

        nodes.extend(self.__inorder_rec(node.right, only_values))
        return nodes

    def __postorder_rec(self, node, only_values):
        if not node:
            return []

        nodes = []
        nodes.extend(self.__postorder_rec(node.left, only_values))
        nodes.extend(self.__postorder_rec(node.right, only_values))
        if only_values:
            nodes.append(node.value)
        else:
            nodes.append(node)

        return nodes

# endregion

    def __get_height(self, node):
        if not node:
            return 0

        return node.height

    def __get_balance(self, node):
        if not node:
            return 0

        return self.__get_height(node.left) - self.__get_height(node.right)

    def __balanced_insert(self, node, value):
        if not node:
            return TreeNode(value)

        if value < node.value:
            node.left = self.__balanced_insert(node.left, value)
        else:
            node.right = self.__balanced_insert(node.right, value)

        node.height = 1 + max(self.__get_height(node.left),
                              self.__get_height(node.right))
        balance = self.__get_balance(node)

        # Left rotation necessary
        if 1 < balance:
            balance_left = self.__get_balance(node.left)
            # Left-left rotation necessary
            if 0 < balance_left:
                return self.__ll(node)
            # Left-right rotation necessary
            elif 0 > balance_left:
                return self.__lr(node)
        # Right rotation necessary
        elif -1 > balance:
            balance_right = self.__get_balance(node.right)
            # Right-left rotation necessary
            if 0 < balance_right:
                return self.__rl(node)
            # Right-right rotation necessary
            elif 0 > balance_right:
                return self.__rr(node)

        return node


# endregion

    def get_root(self):
        return self.__root

    def insert(self, value):
        self.__root = self.__balanced_insert(self.__root, value)

    def preorder(self, only_values=True):
        nodes = []
        nodes.extend(self.__preorder_rec(self.__root, only_values))
        return nodes

    def inorder(self, only_values=True):
        nodes = []
        nodes.extend(self.__inorder_rec(self.__root, only_values))
        return nodes

    def postorder(self, only_values=True):
        nodes = []
        nodes.extend(self.__postorder_rec(self.__root, only_values))
        return nodes


if __name__ == "__main__":
    tree = AVLTree()
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)
    tree.insert(40)
    tree.insert(0)

    print(tree.preorder())
    print(tree.inorder())
    print(tree.postorder())
