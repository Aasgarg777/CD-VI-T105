class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add(self, child):
        self.children.append(child)


def build_ast(pos_tags):
    root = ASTNode("SENTENCE")
    i = 0
    used_indices = set()

    # Try to parse noun phrase first (subject)
    if i < len(pos_tags):
        if pos_tags[i][1] == "DET" and i + 1 < len(pos_tags) and pos_tags[i + 1][1] == "NOUN":
            det_node = ASTNode(pos_tags[i][0])
            noun_node = ASTNode(pos_tags[i + 1][0])
            np = ASTNode("NOUN_PHRASE")
            np.add(det_node)
            np.add(noun_node)
            root.add(np)
            used_indices.update([i, i + 1])
            i += 2
        elif pos_tags[i][1] == "NOUN":
            noun_node = ASTNode(pos_tags[i][0])
            np = ASTNode("NOUN_PHRASE")
            np.add(noun_node)
            root.add(np)
            used_indices.add(i)
            i += 1

    # Verb phrase (support AUX + VERB + PREP + NOUN)
    if i < len(pos_tags):
        vp = ASTNode("VERB_PHRASE")

        # AUX
        if pos_tags[i][1] == "AUX":
            aux_node = ASTNode(pos_tags[i][0])
            vp.add(aux_node)
            used_indices.add(i)
            i += 1

        # VERB
        if i < len(pos_tags) and pos_tags[i][1] == "VERB":
            verb_node = ASTNode(pos_tags[i][0])
            vp.add(verb_node)
            used_indices.add(i)
            i += 1

            # Optional PREP + NOUN phrase
            if i < len(pos_tags) and pos_tags[i][1] == "PREP":
                prep_node = ASTNode(pos_tags[i][0])
                i += 1
                if i < len(pos_tags) and pos_tags[i][1] == "NOUN":
                    noun_node = ASTNode(pos_tags[i][0])
                    prep_phrase = ASTNode("PREP_PHRASE")
                    prep_phrase.add(prep_node)
                    prep_phrase.add(noun_node)
                    vp.add(prep_phrase)
                    used_indices.update([i - 1, i])
                    i += 1

        if vp.children:
            root.add(vp)

    # Add any remaining unmatched tokens as fallback nodes
    for index, (word, tag) in enumerate(pos_tags):
        if index not in used_indices:
            root.add(ASTNode(f"{word} ({tag})"))

    return root
