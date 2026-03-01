# data_structures/trie.py
from typing import List, Optional

class TrieNode:
    __slots__ = ('children', 'is_end')
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect_words(self, node: TrieNode, prefix: str, result: List[str]) -> None:
        if node.is_end:
            result.append(prefix)
        for ch, child in node.children.items():
            self._collect_words(child, prefix + ch, result)

    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """
        إرجاع قائمة بالكلمات التي تبدأ بالبادئة المعطاة (حد أقصى limit).
        """
        node = self._find_node(prefix)
        if not node:
            return []
        results = []
        self._collect_words(node, prefix, results)
        return results[:limit]
