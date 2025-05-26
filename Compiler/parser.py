class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add(self, child):
        self.children.append(child)

    # Optional but recommended: visualize using graphviz
    def visualize(self, filename="ast_tree"):
        try:
            from graphviz import Digraph
        except ImportError:
            print("Install graphviz using `pip install graphviz` to use visualization.")
            return

        dot = Digraph(comment="Abstract Syntax Tree")

        def add_nodes_edges(node, parent_id=None, node_id=0):
            current_id = str(id(node)) + str(node_id)
            dot.node(current_id, node.value)
            if parent_id:
                dot.edge(parent_id, current_id)
            for i, child in enumerate(node.children):
                add_nodes_edges(child, current_id, i)

        add_nodes_edges(self)
        dot.render(filename, format='png', cleanup=True)
        print(f"AST visualization saved as '{filename}.png'")

def build_ast(pos_tags):
    root = ASTNode("SENTENCE")
    i = 0
    used_indices = set()

    def is_used(idx):
        return idx in used_indices

    def parse_noun_phrase(start):
        children = []
        idx = start

        # Determiner (optional)
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "Determiner":
            children.append(ASTNode(pos_tags[idx][0]))
            idx += 1

        # Adjective(s)
        while idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "Adjective":
            children.append(ASTNode(pos_tags[idx][0]))
            idx += 1

        # Noun or Pronoun
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] in ("Noun", "Pronoun"):
            children.append(ASTNode(pos_tags[idx][0]))
            idx += 1
            np = ASTNode("NOUN_PHRASE")
            for c in children:
                np.add(c)
            return np, idx
        else:
            if start < len(pos_tags) and not is_used(start) and pos_tags[start][1] == "Pronoun":
                np = ASTNode("NOUN_PHRASE")
                np.add(ASTNode(pos_tags[start][0]))
                return np, start + 1

        return None, start

    def parse_verb_phrase(start):
        vp = ASTNode("VERB_PHRASE")
        idx = start

        # Auxiliary verb
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "Auxiliary Verb":
            vp.add(ASTNode(pos_tags[idx][0]))
            idx += 1

        # Main verb required
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "Verb":
            vp.add(ASTNode(pos_tags[idx][0]))
            idx += 1
        else:
            return None, start

        # Prepositional phrase (optional)
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "Preposition":
            prep_node = ASTNode(pos_tags[idx][0])
            idx += 1
            np, new_idx = parse_noun_phrase(idx)
            if np:
                prep_phrase = ASTNode("PREP_PHRASE")
                prep_phrase.add(prep_node)
                prep_phrase.add(np)
                vp.add(prep_phrase)
                idx = new_idx
            else:
                vp.add(prep_node)

        return vp, idx

    # Start building
    np, new_i = parse_noun_phrase(i)
    if np:
        root.add(np)
        used_indices.update(range(i, new_i))
        i = new_i

    vp, new_i = parse_verb_phrase(i)
    if vp:
        root.add(vp)
        used_indices.update(range(i, new_i))
        i = new_i

    for idx, (word, tag) in enumerate(pos_tags):
        if idx not in used_indices:
            root.add(ASTNode(f"{word} ({tag})"))

    return root
