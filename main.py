import fileinput


class Node:
    def __init__(self, s_, t_):
        self.str = s_
        self.children = {}
        self.is_terminal = t_

    def split(self, i):
        if i != len(self.str):
            new = Node(self.str[i:], self.is_terminal)
            new.children = self.children
            self.str = self.str[:i]
            self.children = {new.str[0]: new}

    def mistake(self, word_, sug, acc):
        if len(word_) > 0:
            next_n = self.children.get(word_[0])
            if next_n:
                if next_n.str == word_[:len(next_n.str)]:
                    if next_n.str == word_ and next_n.is_terminal:
                        sug.add(acc + next_n.str)
                    next_n.mistake(word_[len(next_n.str):], sug, acc + next_n.str)

    def suggest(self, word_, sug, acc):
        for node in self.children.values():
            l_ = len(node.str)
            l_new = len(node.str)
            for i_, ch in enumerate(node.str):
                if len(word_) <= i_ or ch != word_[i_]:
                    l_ = i_
                    break
            if len(node.str) == l_:
                if l_new in [len(word_), len(word_) - 1] and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(word_[l_new:], sug, acc + node.str)
                continue

            if node.str[l_:] == word_[l_ + 1:l_new + 1]:
                if l_new == (len(word_) - 1) and node.is_terminal:
                    sug.add(acc + node.str)
                node.mistake(word_[l_new + 1:], sug, acc + node.str)

            if node.str[l_ + 1:] == word_[l_:l_new - 1]:
                if l_new == (len(word_) + 1) and node.is_terminal:
                    sug.add(acc + node.str)
                node.mistake(word_[l_new - 1:], sug, acc + node.str)

            if node.str[l_ + 1:] == word_[l_ + 1:l_new]:
                if l_new == len(word_) and node.is_terminal:
                    sug.add(acc + node.str)
                node.mistake(word_[l_new:], sug, acc + node.str)

            if l_ + 1 < len(word_) and word_[l_ + 1] == node.str[l_]:
                if word_[l_] in node.children:
                    adjusted = word_[:l_] + word_[l_ + 1] + word_[l_] + word_[l_ + 1 + 1:]
                    if l_new == len(word_) and node.is_terminal:
                        sug.add(acc + node.str)
                    node.mistake(adjusted[l_new:], sug, acc + node.str)
                elif l_ < len(node.str) - 1 and node.str[l_ + 1] == word_[l_] and node.str[l_ + 2:] == word_[
                                                                                                       l_ + 1 + 1:l_new]:
                    if l_new == len(word_) and node.is_terminal:
                        sug.add(acc + node.str)
                    node.mistake(word_[l_new:], sug, acc + node.str)


class Trie:
    def __init__(self):
        self.root = Node(s_='', t_=False)

    def add_word(self, word_):
        # вставка выполняется за O(1) в случае пустого дерева и
        # за O(n) в худшем случае при полном совпадении слова с уже существующим словом.
        # В среднем выполняется за O(log(n))
        if word_:
            node_ = self.root.children.get(word_[0])
            if node_ is None:
                self.root.children[word_[0]] = Node(word_, True)
                return
            str_i = 0
            for i_ in range(len(word_)):
                if str_i < len(node_.str):
                    if not word_[i_] == node_.str[str_i]:
                        node_.split(str_i)
                        node_.is_terminal = False
                        node_.children[word[i_]] = Node(word[i_:], True)
                str_i += 1
                if str_i == len(node_.str) and i_ + 1 < len(word_):
                    next_node, str_i = node_.children.get(word_[i_ + 1]), 0
                    if next_node is None:
                        node_.children[word_[i_ + 1]] = Node(word_[i_ + 1:], True)
                        return
                    node_ = next_node
            if str_i < len(node_.str):
                node_.split(str_i)
                node_.is_terminal = True
                return

    def find(self, word_):
        # поиск выполняется в среднем за O(log(k) * n),
        # где k - количество вершин в дереве, n - количество символов в слове
        if word_ and self.root.children is not None:
            node_ = self.root.children.get(word_[0])
            if node_ is not None:
                str_i = -1
                for i_ in range(len(word_)):
                    str_i += 1
                    if str_i == len(node_.str):
                        node_, str_i = node_.children.get(word_[i_]), 0
                        if node_ is None:
                            return False
                    elif word_[i_] != node_.str[str_i]:
                        return False
                if node_.is_terminal and node_.str in word_:
                    return True
        return False

    def suggest(self, word_):
        # алгоритм советования работает за O(m * n^2) в худшем случае
        # где m - количество вершин дерева, в n - количество символов в слове
        suggests = set()
        self.root.suggest(word_, suggests, '')
        return sorted(suggests)


if __name__ == '__main__':
    t = Trie()
    length = int(input())
    for i in range(length):
        word = input()
        while word is None:
            word = input()
        t.add_word(word.lower())
    for line in fileinput.input():
        s = line[:-1]
        if s != '':
            if t.find(s.lower()):
                print(f'{s} - ok')
                continue
            k = t.suggest(s.lower())
            if k:
                print(f'{s} -> {", ".join(k)}')
                continue
            print(f'{s} -?')
