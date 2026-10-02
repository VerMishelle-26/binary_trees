from collections import deque


# === К1: Класс BinaryTree ===
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    """Бинарное дерево поиска (BST)."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Вставка значения."""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value)

    def search(self, value):
        """Поиск значения. True, если найдено."""
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)


# === К2: Обход в ширину (BFS) ===
def bfs(root):
    """Breadth-First Search — по уровням."""
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


# === К3: Обходы в глубину (DFS) ===
def preorder(root):
    """Прямой обход: корень → левое → правое."""
    if root is None:
        return []
    return [root.value] + preorder(root.left) + preorder(root.right)


def inorder(root):
    """Симметричный обход: левое → корень → правое."""
    if root is None:
        return []
    return inorder(root.left) + [root.value] + inorder(root.right)


def postorder(root):
    """Обратный обход: левое → правое → корень."""
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.value]


# === К4: Класс AVLTree с балансировкой ===
class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(BinaryTree):
    """AVL-дерево — самобалансирующееся бинарное дерево."""

    def __init__(self):
        super().__init__()
        self.root = None

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def left_rotate(self, z):
        """Левый поворот."""
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        self._update_height(z)
        self._update_height(y)
        return y

    def right_rotate(self, z):
        """Правый поворот."""
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        self._update_height(z)
        self._update_height(y)
        return y

    def rebalance(self, node, value):
        """Балансировка узла после вставки."""
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left-Left
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)
        # Right-Right
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)
        # Left-Right
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right-Left
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def insert(self, value):
        """Вставка с балансировкой."""
        self.root = self._insert_avl(self.root, value)

    def _insert_avl(self, node, value):
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert_avl(node.left, value)
        elif value > node.value:
            node.right = self._insert_avl(node.right, value)
        else:
            return node
        return self.rebalance(node, value)


# === Проверка ===
if __name__ == "__main__":
    print("=== К1: BinaryTree ===")
    bt = BinaryTree()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bt.insert(v)
    print("Вставлено: 50, 30, 70, 20, 40, 60, 80")
    print(f"Поиск 40: {bt.search(40)}")
    print(f"Поиск 100: {bt.search(100)}")

    print("\n=== К2: BFS (обход в ширину) ===")
    print(f"BFS: {bfs(bt.root)}")

    print("\n=== К3: DFS (обходы в глубину) ===")
    print(f"Preorder:  {preorder(bt.root)}")
    print(f"Inorder:   {inorder(bt.root)}")
    print(f"Postorder: {postorder(bt.root)}")

    print("\n=== К4: AVLTree ===")
    avl = AVLTree()
    for v in [10, 20, 30, 40, 50, 25]:
        avl.insert(v)
        print(f"Вставлено {v}, корень: {avl.root.value}, высота: {avl.root.height}")
    print(f"BFS AVL: {bfs(avl.root)}")
    print(f"Inorder AVL (отсортировано): {inorder(avl.root)}")