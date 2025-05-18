import tkinter as tk
from tkinter import ttk
from lexer import lexical_analysis
from parser import build_ast

class ASTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple NLP AST Visualizer")

        # Input Frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.label = tk.Label(self.frame, text="Enter a sentence:")
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.frame, width=50)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.button = tk.Button(self.frame, text="Parse & Visualize", command=self.parse_and_draw)
        self.button.pack(side=tk.LEFT)

        # Canvas for AST
        self.canvas = tk.Canvas(root, width=1000, height=500, bg="white")
        self.canvas.pack(pady=10)

        # Token Table
        self.tree = ttk.Treeview(root, columns=("Word", "POS"), show="headings", height=8)
        self.tree.heading("Word", text="Word")
        self.tree.heading("POS", text="Part of Speech")
        self.tree.column("Word", width=200, anchor=tk.CENTER)
        self.tree.column("POS", width=200, anchor=tk.CENTER)
        self.tree.pack(pady=10, anchor="center", padx=20, fill=tk.BOTH, expand=True)

        # POS tag label (optional UX improvement)
        self.pos_label = tk.Label(root, text="", fg="gray")
        self.pos_label.pack()

    def parse_and_draw(self):
        sentence = self.entry.get().strip()
        if not sentence:
            return

        pos_tags = lexical_analysis(sentence)
        ast_root = build_ast(pos_tags)

        print("POS Tags:", pos_tags)

        # Update token table
        for row in self.tree.get_children():
            self.tree.delete(row)
        for word, tag in pos_tags:
            self.tree.insert("", tk.END, values=(word, tag))

        # Clear and prepare canvas
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        root_x = canvas_width // 2

        if ast_root:
            self.draw_ast_recursive(ast_root, root_x, 50)
        else:
            self.canvas.create_text(canvas_width // 2, 200,
                                    text="Could not build AST for this sentence.",
                                    fill="red", font=("Arial", 16, "bold"))

    def draw_ast_recursive(self, node, x, y, level=0):
        radius = 20
        node_width = self.get_subtree_width(node)

        # Draw current node
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue")
        self.canvas.create_text(x, y, text=node.value, font=("Arial", 12, "bold"))

        if not node.children:
            return

        spacing = 60  # Increased spacing between child nodes
        total_width = sum(self.get_subtree_width(child) for child in node.children) + spacing * (len(node.children) - 1)
        start_x = x - total_width / 2
        current_x = start_x
        child_y = y + 100  # Increased vertical distance between levels

        for child in node.children:
            child_width = self.get_subtree_width(child)
            child_center_x = current_x + child_width / 2

            # Draw line to child
            self.canvas.create_line(x, y + radius, child_center_x, child_y - radius)

            # Recurse
            self.draw_ast_recursive(child, child_center_x, child_y, level + 1)
            current_x += child_width + spacing

    def get_subtree_width(self, node):
        if not node.children:
            return 60  # Wider width for individual leaf nodes
        spacing = 60  # Match horizontal spacing
        return sum(self.get_subtree_width(child) for child in node.children) + spacing * (len(node.children) - 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ASTApp(root)
    root.mainloop()