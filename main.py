import fileinput


class Node:
    def __init__(self, s_, t_):
        self.str = s_
        self.children = dict()
        self.is_terminal = t_

    def extract(self, i, t):
        if i != len(self.str):
            new = Node(self.str[i:], self.is_terminal)
            new.children = self.children
            self.str = self.str[:i]
            self.children = {new.str[0]: new}
        self.is_terminal = t

    def suggest(self, word_, sug, i_, mistake, acc):
        if mistake:
            if i_ < len(word_):
                next_n = self.children.get(word_[i_])
                if next_n:
                    if next_n.str == word_[i_:i_ + len(next_n.str)]:
                        if next_n.str == word_[i_:] and next_n.is_terminal:
                            sug.add(acc + next_n.str)
                        next_n.suggest(word_, sug, i_ + len(next_n.str), True, acc + next_n.str)
            return
        for node in self.children.values():
            l_ = len(node.str)
            l_new = len(acc + node.str)
            for it, char in enumerate(node.str):
                if len(word_) <= it + i_ or char != word_[it + i_]:
                    l_ = it
                    break
            if len(node.str) == l_:
                if l_new in [len(word_), len(word_) - 1] and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(word_, sug, i_ + l_, False, acc + node.str)
                continue
            l_ = len(node.str)
            if node.str[l_:] == word_[i_ + l_ + 1:l_new + 1]:
                if l_new == (len(word_) - 1) and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(word_, sug, i_ + l_ + 1, True, acc + node.str)

            if node.str[l_ + 1:] == word_[i_ + l_:l_new - 1]:
                if l_new == (len(word_) + 1) and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(word_, sug, i_ + l_ - 1, True, acc + node.str)

            if node.str[l_ + 1:] == word_[i_ + l_ + 1:l_new]:
                if l_new == len(word_) and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(word_, sug, i_ + l_, True, acc + node.str)

            if i_ + l_ + 1 < len(word_) and (word_[i_ + l_] in node.children) and word_[i_ + l_ + 1] == node.str[i_]:
                adjusted = word_[:i_ + l_] + word_[i_ + l_ + 1] + word_[i_ + l_] + word_[i_ + l_ + 1 + 1:]
                if l_new == len(word_) and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(adjusted, sug, i_ + l_, True, acc + node.str)
                continue

            if l_ < l_ - 1 and i_ + l_ < len(word_) - 1 and node.str[l_] == word_[i_ + l_ + 1] and \
                    node.str[l_ + 1] == word_[i_ + l_] and node.str[l_ + 2:] == word_[i_ + l_ + 1 + 1:l_new]:
                if l_new == len(word_) and node.is_terminal:
                    sug.add(acc + node.str)
                node.suggest(word_, sug, i_ + l_, True, acc + node.str)


class Trie:
    def __init__(self):
        self.root = Node(s_='', t_=False)

    def add_word(self, word_):
        if word_:
            node_ = self.root.children.get(word_[0])
            if node_ is None:
                self.root.children[word_[0]] = Node(word_, True)
                return
            str_i = 0
            for i_ in range(len(word_)):
                if not word_[i_] == node_.str[str_i]:
                    node_.extract(str_i, False)
                    node_.children[word[i_]] = Node(word[i_:], True)
                    return
                str_i += 1
                if str_i == len(node_.str):
                    next_node, str_i = node_.children.get(word_[i_]), 0
                    if next_node is None:
                        node_.children[word_[i_:]] = Node(word_, True)
                        return
                    node_ = next_node
            if str_i < len(node_.str):
                node_.extract(str_i, True)
                return
            node_.is_terminal = True

    def find(self, word_):
        if word:
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
        suggests = set()
        self.root.suggest(word_, suggests, 0, False, '')
        return sorted(suggests)


if __name__ == '__main__':
    t = Trie()
    length = int(input())
    for i in range(length):
        word = input()
        while word is None:
            word = input()
        t.add_word(word)
    for line in fileinput.input():
        s = line.strip().lower()
        if s != '':
            if t.find(s):
                print(f'{s} - ok')
                continue
            k = t.suggest(s)
            if k:
                print(f'{s} -> {", ".join(k)}')
                continue
            print(f'{s} -?')
