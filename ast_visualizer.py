import tkinter as tk

COLORS = {
    "NOUN_PHRASE": "#a1c9f1",
    "VERB": "#f7a072",
    "ROOT": "#d3f8e2",
    "TEXT": "black"
}

LEGEND = {
    "ROOT": "Root (SENTENCE)",
    "NOUN_PHRASE": "Noun Phrase",
    "VERB": "Verb"
}

def draw_tree(canvas, node, x, y, level=0):
    """
    Recursively draws the AST nodes and edges on the canvas.
    """
    canvas.create_text(x, y, text=node.value, font=("Arial", 12), fill="blue")
    child_count = len(node.children)
    spacing = 100

    for i, child in enumerate(node.children):
        x_child = x + (i - child_count / 2) * spacing + spacing / 2
        y_child = y + 60
        canvas.create_line(x, y + 10, x_child, y_child - 10, fill="black")
        draw_tree(canvas, child, x_child, y_child, level + 1)

def draw_ast(canvas, tree, width, height):
    """
    Draws the AST with rectangles and lines, including a legend.
    """
    canvas.delete("all")
    node_width = 80
    node_height = 30
    spacing_x = 150
    spacing_y = 100

    def draw_node(text, x, y, color):
        canvas.create_rectangle(x, y, x + node_width, y + node_height, fill=color, outline="black")
        canvas.create_text(x + node_width / 2, y + node_height / 2, text=text, fill=COLORS['TEXT'])

    def draw_line(x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

    x_root = width / 2 - node_width / 2
    y_root = 20
    draw_node("SENTENCE", x_root, y_root, COLORS['ROOT'])
    y1 = y_root + node_height

    x_start = width / 2 - spacing_x
    for i, part in enumerate(tree.get("SENTENCE", [])):
        if isinstance(part, dict):
            label, words = list(part.items())[0]
            color = COLORS['NOUN_PHRASE'] if label.startswith("NOUN_PHRASE") else COLORS['VERB']
            x = x_start + i * spacing_x

            draw_node(label, x, y1, color)
            draw_line(x_root + node_width / 2, y_root + node_height, x + node_width / 2, y1)

            y2 = y1 + spacing_y
            if isinstance(words, list):
                for j, word in enumerate(words):
                    x_leaf = x + j * (node_width + 10) - (len(words) - 1) * (node_width + 10) / 2
                    draw_node(word, x_leaf, y2, "white")
                    draw_line(x + node_width / 2, y1 + node_height, x_leaf + node_width / 2, y2)
            else:
                draw_node(words, x, y2, "white")
                draw_line(x + node_width / 2, y1 + node_height, x + node_width / 2, y2)

    # Draw legend
    y_legend = height - 100
    x_legend = 10
    for key, label in LEGEND.items():
        canvas.create_rectangle(x_legend, y_legend, x_legend + 20, y_legend + 20, fill=COLORS[key], outline="black")
        canvas.create_text(x_legend + 130, y_legend + 10, text=f"= {label}", anchor=tk.W)
        y_legend += 30