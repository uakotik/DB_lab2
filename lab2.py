import random

def hash_name(name):
    name = enumerate(name.lower())
    max_len = max([len(i) for i in names])
    hash = 0
    for i, char in name:
        if i >= max_len:
            break
        hash += ord(char) ** (max_len - i)

    return hash

def gen_number():
    return "380" + "".join([str(random.randint(0, 9)) for _ in range(7)])


class Node:
    def __init__(self):
        self.keys = []
        self.parent = None


class InternalNode(Node):
    def __init__(self):
        super().__init__()
        self.children = []

class Leaf(Node):
    def __init__(self):
        super().__init__()
        self.records = []
        self.next = None


class BPlusTree:
    def __init__(self, order=4):
        self.root = Leaf()
        self.order = order

    def insert(self, key, value, number):
        """
        Вставляє пару ключ-значення в дерево.
        Спускається до відповідного листового вузла.
        Якщо листовий вузол переповнюється розбиває його.
        """
        node = self.root

        # Спускаємся до листового вузла
        while isinstance(node, InternalNode):
            i = 0
            # Шукаємо підходяще нам дитя
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        # Знаходить позицію для вставки ключа в листовий вузол
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
            
        # Якщо ключ вже існує в листовому вузлі, додає запис
        if i < len(node.keys) and key == node.keys[i]:
            node.records[i].append((value, number))
        else:
            node.keys.insert(i, key)
            node.records.insert(i, [(value, number)])

        # При переповнені листового вузлу виконуємо спліт
        if len(node.keys) > self.order:
            self.split_leaf(node)

    def split_leaf(self, node):
        """
        Розбиває листовий вузол та змінює батьківські посилання
        """
        new_leaf = Leaf()
        centr = len(node.keys) // 2

         # Переміщує другу половину ключів і записів в новий лист
        new_leaf.keys = node.keys[centr:]
        new_leaf.records = node.records[centr:]
        node.keys = node.keys[:centr]
        node.records = node.records[:centr]

        if node.parent:
            parent = node.parent
            insert_index = parent.children.index(node) + 1
            parent.keys.insert(insert_index - 1, new_leaf.keys[0])
            parent.children.insert(insert_index, new_leaf)
            new_leaf.parent = parent

            # Розбиття батьківського вузла при переповненні
            if len(parent.keys) > self.order:
                self.split_internal(parent)
        else:
            # Створює корінь при відсутності батьківського вузла
            new_root = InternalNode()
            new_root.keys = [new_leaf.keys[0]]
            new_root.children = [node, new_leaf]
            node.parent = new_leaf.parent = new_root
            self.root = new_root


    def split_internal(self, node):
        """
        Розділяє внутрішній вузол
        """
        new_internal = InternalNode()
        centr = len(node.keys) // 2
        centr_key=node.keys[centr]

        # Переміщує другу половину ключів і записів в новий лист
        new_internal.keys = node.keys[centr + 1:]
        new_internal.children = node.children[centr + 1:]
        node.keys = node.keys[:centr]
        node.children = node.children[:centr + 1]
        
        # Оновлює посилання на батьківський вузол для дочірніх вузлів нового внутрішнього вузла
        for child in new_internal.children:
            child.parent = new_internal
        if node.parent:
            parent = node.parent
            insert_index = parent.children.index(node) + 1
            parent.keys.insert(insert_index - 1, centr_key)
            parent.children.insert(insert_index, new_internal)
            new_internal.parent = parent

            # Розбиття батьківського вузла при переповненні
            if len(parent.keys) > self.order:
                self.split_internal(parent)
        else:
            # Створює корінь при відсутності батьківського вузла
            new_root = InternalNode()
            new_root.keys = [centr_key]
            new_root.children = [node, new_internal]
            node.parent = new_internal.parent = new_root
            self.root = new_root

            
    def search(self, key):
        node = self.root
        
        # Спускаємся до листового вузла
        while isinstance(node, InternalNode):
            i = 0
            # Шукаємо підходяще нам дитя
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
            
        
        # Шукаємо ключ
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.records[i]
    
        return None
    

    def delete(self, key):
        node = self.root
        
        # Спускаємся до листового вузла
        while isinstance(node, InternalNode):
            i = 0
            # Шукаємо підходяще нам дитя
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
            
        # Видяляємо значення 
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and key == node.keys[i]:
            del node.keys[i]
            del node.records[i]
            return True  
        
        return False  


    def print_tree(self, node=None, indent=""):
        if node is None:
            node = self.root
        if isinstance(node, Leaf):
            print(indent + "Leaf: " + str(node.keys) + " " + str(node.records))
        else:
            print(indent + "Node: " + str(node.keys))
            for child in node.children:
                self.print_tree(child, indent + "  ")

# Ініціалізація
names = [ 'Aiden','Bella','Carter','Diana','Ethan','Fiona','Gavin','Hannah','Isabella','Jack','Kaitlyn','Liam',
          'Mia','Nathan','Olivia','Parker','Quinn','Rachel','Sophia','Zoyberg']
tree = BPlusTree()

# Вставляєм значення
for name in names:
    tree.insert(hash_name(name), name, gen_number())

print('B+TREE:')
tree.print_tree()

# Пошук імені
record = tree.search(hash_name('Rachel'))

if record is not None:
    for i in record:
        print(f'\nНомер телефону {i[0]} : {i[1]}')
else:
    print(f'\nНомер не знайдено')

#Видалення елементу
name_to_delete = 'Zoyberg'
if tree.delete(hash_name(name_to_delete)):
    print(f'Name with key {name_to_delete} deleted successfully.')
else:
    print(f'Name with key {name_to_delete} not found.')

# Повторний вивід структури дерева для перевірки видалення
print('\nB+TREE after deletion:')
tree.print_tree()