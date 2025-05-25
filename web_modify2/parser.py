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

    # Helper to check if index is already used
    def is_used(idx):
        return idx in used_indices

    # Parse noun phrase: (DET)? + (ADJ)* + NOUN | PRON
    def parse_noun_phrase(start):
        children = []
        idx = start

        # Determiner (optional)
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "DET":
            children.append(ASTNode(pos_tags[idx][0]))
            idx += 1

        # Adjectives (zero or more)
        while idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "ADJ":
            children.append(ASTNode(pos_tags[idx][0]))
            idx += 1

        # Noun or Pronoun
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] in ("NOUN", "PRON"):
            children.append(ASTNode(pos_tags[idx][0]))
            idx += 1
            np = ASTNode("NOUN_PHRASE")
            for c in children:
                np.add(c)
            return np, idx
        else:
            # Try Pronoun alone if no DET/ADJ/NOUN
            if start < len(pos_tags) and not is_used(start) and pos_tags[start][1] == "PRON":
                np = ASTNode("NOUN_PHRASE")
                np.add(ASTNode(pos_tags[start][0]))
                return np, start + 1

        return None, start

    # Parse verb phrase: (AUX)? + VERB + (PREP + noun_phrase)?
    def parse_verb_phrase(start):
        vp = ASTNode("VERB_PHRASE")
        idx = start

        # AUX optional
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "AUX":
            vp.add(ASTNode(pos_tags[idx][0]))
            idx += 1

        # VERB mandatory
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "VERB":
            vp.add(ASTNode(pos_tags[idx][0]))
            idx += 1
        else:
            return None, start  # no verb phrase if no verb here

        # Optional PREP + noun phrase
        if idx < len(pos_tags) and not is_used(idx) and pos_tags[idx][1] == "PREP":
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
                # Just add prep node alone
                vp.add(prep_node)

        return vp, idx

    # Parse full sentence: noun phrase + verb phrase + remaining
    # 1) Noun Phrase (subject)
    np, new_i = parse_noun_phrase(i)
    if np:
        root.add(np)
        used_indices.update(range(i, new_i))
        i = new_i

    # 2) Verb Phrase (predicate)
    vp, new_i = parse_verb_phrase(i)
    if vp:
        root.add(vp)
        used_indices.update(range(i, new_i))
        i = new_i

    # 3) Catch any leftover tokens as fallback nodes (with tag)
    for idx, (word, tag) in enumerate(pos_tags):
        if idx not in used_indices:
            root.add(ASTNode(f"{word} ({tag})"))

    return root
