

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from logic import Symbol, And, Or, Not, Implication, Biconditional, model_check
import puzzle as puzzle_module




def load_builtin_puzzles():
    """Pulls the puzzles already defined inside puzzle.py."""
    names = ["Puzzle 0", "Puzzle 1", "Puzzle 2", "Puzzle 3"]
    knowledges = [
        puzzle_module.knowledge0,
        puzzle_module.knowledge1,
        puzzle_module.knowledge2,
        puzzle_module.knowledge3,
    ]
    symbols = [
        puzzle_module.AKnight, puzzle_module.AKnave,
        puzzle_module.BKnight, puzzle_module.BKnave,
        puzzle_module.CKnight, puzzle_module.CKnave,
    ]
    return list(zip(names, knowledges)), symbols


def solve_puzzle(knowledge, symbols):
    """Returns list of symbols that the knowledge base entails as True."""
    results = []
    for symbol in symbols:
        if model_check(knowledge, symbol):
            results.append(str(symbol))
    return results



class KnightsKnavesGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Knights & Knaves - Logic Puzzle Solver")
        self.geometry("760x560")

        
        builtin_puzzles, self.builtin_symbols = load_builtin_puzzles()
        self.puzzles = list(builtin_puzzles)  
        self.puzzle_symbols = {name: self.builtin_symbols for name, _ in builtin_puzzles}

        
        self.characters = {}          
        self.base_constraints = []    
        self.custom_statements = []   
        self.eval_namespace = {
            "Symbol": Symbol, "And": And, "Or": Or, "Not": Not,
            "Implication": Implication, "Biconditional": Biconditional,
        }

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.puzzles_tab = ttk.Frame(notebook)
        self.add_tab = ttk.Frame(notebook)
        notebook.add(self.puzzles_tab, text="Puzzles")
        notebook.add(self.add_tab, text="Add Puzzle")

        self._build_puzzles_tab()
        self._build_add_tab()

    
    def _build_puzzles_tab(self):
        frame = self.puzzles_tab

        left = ttk.Frame(frame)
        left.pack(side="left", fill="y", padx=(0, 8))

        ttk.Label(left, text="Puzzles:").pack(anchor="w")
        self.puzzle_listbox = tk.Listbox(left, width=28, height=20, exportselection=False)
        self.puzzle_listbox.pack(fill="y", expand=True)
        self._refresh_puzzle_list()

        ttk.Button(left, text="Solve Selected", command=self._solve_selected).pack(fill="x", pady=(8, 0))

        right = ttk.Frame(frame)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Result:").pack(anchor="w")
        self.result_box = scrolledtext.ScrolledText(right, wrap="word")
        self.result_box.pack(fill="both", expand=True)

    def _refresh_puzzle_list(self):
        self.puzzle_listbox.delete(0, tk.END)
        for name, _ in self.puzzles:
            self.puzzle_listbox.insert(tk.END, name)

    def _solve_selected(self):
        selection = self.puzzle_listbox.curselection()
        if not selection:
            messagebox.showinfo("Select a puzzle", "Please select a puzzle from the list first.")
            return
        name, knowledge = self.puzzles[selection[0]]
        symbols = self.puzzle_symbols.get(name, self.builtin_symbols)

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, f"{name}\n{'-' * len(name)}\n")
        try:
            results = solve_puzzle(knowledge, symbols)
        except Exception as exc:
            self.result_box.insert(tk.END, f"Error while solving: {exc}\n")
            return

        if results:
            for r in results:
                self.result_box.insert(tk.END, f"  \u2713 {r}\n")
        else:
            self.result_box.insert(tk.END, "  No conclusions could be drawn.\n")

    
    def _build_add_tab(self):
        frame = self.add_tab


        step1 = ttk.LabelFrame(frame, text="1. Add a character")
        step1.pack(fill="x", padx=4, pady=4)

        self.char_entry = ttk.Entry(step1, width=20)
        self.char_entry.pack(side="left", padx=4, pady=4)
        ttk.Button(step1, text="Add Character", command=self._add_character).pack(side="left", padx=4)

        self.char_list_label = ttk.Label(step1, text="Characters: (none)")
        self.char_list_label.pack(side="left", padx=8)

        
        step2 = ttk.LabelFrame(
            frame,
            text=("2. Add a statement — use character names + Knight/Knave, e.g.\n"
                  "   Biconditional(AKnight, And(AKnave, BKnave))")
        )
        step2.pack(fill="x", padx=4, pady=4)

        self.statement_entry = ttk.Entry(step2, width=70)
        self.statement_entry.pack(side="left", padx=4, pady=4, fill="x", expand=True)
        ttk.Button(step2, text="Add Statement", command=self._add_statement).pack(side="left", padx=4)

        self.statements_box = scrolledtext.ScrolledText(frame, height=6, wrap="word")
        self.statements_box.pack(fill="x", padx=4, pady=(0, 4))
        self.statements_box.configure(state="disabled")

        
        step3 = ttk.LabelFrame(frame, text="3. Save puzzle")
        step3.pack(fill="x", padx=4, pady=4)

        ttk.Label(step3, text="Puzzle name:").pack(side="left", padx=4)
        self.puzzle_name_entry = ttk.Entry(step3, width=25)
        self.puzzle_name_entry.pack(side="left", padx=4)
        ttk.Button(step3, text="Save Puzzle", command=self._save_puzzle).pack(side="left", padx=4)
        ttk.Button(step3, text="Reset Builder", command=self._reset_builder).pack(side="left", padx=4)

        ttk.Label(
            frame,
            text=("Saved puzzles appear in the \"Puzzles\" tab and can be solved "
                  "the same way as the built-in ones."),
            foreground="gray"
        ).pack(anchor="w", padx=4, pady=(4, 0))

    def _add_character(self):
        name = self.char_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Enter a character name (e.g. A, B, Bob...).")
            return
        if name in self.characters:
            messagebox.showwarning("Duplicate", f"Character '{name}' already exists.")
            return

        knight = Symbol(f"{name} is a Knight")
        knave = Symbol(f"{name} is a Knave")
        self.characters[name] = {"knight": knight, "knave": knave}


        self.eval_namespace[f"{name}Knight"] = knight
        self.eval_namespace[f"{name}Knave"] = knave

        self.base_constraints.append(Or(knight, knave))
        self.base_constraints.append(Not(And(knight, knave)))

        self.char_entry.delete(0, tk.END)
        self.char_list_label.config(text="Characters: " + ", ".join(self.characters.keys()))

    def _add_statement(self):
        expr = self.statement_entry.get().strip()
        if not expr:
            return
        if not self.characters:
            messagebox.showwarning("No characters", "Add at least one character first.")
            return
        try:
            sentence = eval(expr, {"__builtins__": {}}, self.eval_namespace)
        except Exception as exc:
            messagebox.showerror("Invalid statement", f"Could not parse statement:\n{exc}")
            return

        self.custom_statements.append(sentence)
        self.statements_box.configure(state="normal")
        self.statements_box.insert(tk.END, f"{expr}\n")
        self.statements_box.configure(state="disabled")
        self.statement_entry.delete(0, tk.END)

    def _save_puzzle(self):
        name = self.puzzle_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Give your puzzle a name before saving.")
            return
        if not self.characters:
            messagebox.showwarning("No characters", "Add at least one character first.")
            return
        if any(existing == name for existing, _ in self.puzzles):
            messagebox.showwarning("Duplicate name", f"A puzzle named '{name}' already exists.")
            return

        all_conjuncts = list(self.base_constraints) + list(self.custom_statements)
        knowledge = And(*all_conjuncts)
        symbols = [s for pair in self.characters.values() for s in (pair["knight"], pair["knave"])]

        self.puzzles.append((name, knowledge))
        self.puzzle_symbols[name] = symbols
        self._refresh_puzzle_list()

        messagebox.showinfo("Saved", f"Puzzle '{name}' saved. Go to the 'Puzzles' tab to solve it.")
        self._reset_builder()

    def _reset_builder(self):
        self.characters = {}
        self.base_constraints = []
        self.custom_statements = []
        self.eval_namespace = {
            "Symbol": Symbol, "And": And, "Or": Or, "Not": Not,
            "Implication": Implication, "Biconditional": Biconditional,
        }
        self.char_list_label.config(text="Characters: (none)")
        self.statements_box.configure(state="normal")
        self.statements_box.delete("1.0", tk.END)
        self.statements_box.configure(state="disabled")
        self.puzzle_name_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = KnightsKnavesGUI()
    app.mainloop()
