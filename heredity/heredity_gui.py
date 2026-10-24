import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from heredity import (
    load_data, powerset, joint_probability, update, normalize
)


def compute(people):
    probabilities = {
        person: {
            "gene": {2: 0, 1: 0, 0: 0},
            "trait": {True: 0, False: 0}
        }
        for person in people
    }

    names = set(people)
    for have_trait in powerset(names):
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)
    return probabilities


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("احتمال وراثت ژن و صفت")
        self.geometry("760x420")
        self.minsize(640, 320)

        base = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base, "data")
        self.initial_dir = data_dir if os.path.isdir(data_dir) else base

        font = ("Tahoma", 10)
        style = ttk.Style(self)
        style.configure("Treeview", font=font, rowheight=26)
        style.configure("Treeview.Heading", font=("Tahoma", 10, "bold"))
        style.configure("TButton", font=font)
        style.configure("TLabel", font=font)

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="انتخاب فایل...", command=self.choose_file).pack(side="right")
        self.path_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.path_var, state="readonly", justify="left")
        entry.pack(side="right", fill="x", expand=True, padx=8)

        actions = ttk.Frame(self, padding=(10, 0))
        actions.pack(fill="x")
        ttk.Button(actions, text="محاسبه", command=self.run).pack(side="right")

        columns = ("trait_no", "trait_yes", "gene2", "gene1", "gene0", "name")
        headings = {
            "trait_no": "صفت ندارد",
            "trait_yes": "صفت دارد",
            "gene2": "۲ کپی ژن",
            "gene1": "۱ کپی ژن",
            "gene0": "بدون ژن",
            "name": "نام",
        }

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=headings[col], anchor="center")
            width = 120 if col == "name" else 90
            self.tree.column(col, width=width, anchor="center")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="left", fill="y")
        self.tree.pack(side="right", fill="both", expand=True)

        self.status = tk.StringVar(value="یک فایل CSV انتخاب کنید.")
        ttk.Label(self, textvariable=self.status, anchor="e", padding=(10, 0, 10, 8)).pack(fill="x")

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="انتخاب فایل خانواده",
            initialdir=self.initial_dir,
            filetypes=[("CSV", "*.csv"), ("همه فایل‌ها", "*.*")],
        )
        if path:
            self.path_var.set(path)
            self.status.set("آماده‌ی محاسبه.")

    def run(self):
        path = self.path_var.get()
        if not path:
            messagebox.showwarning("توجه", "ابتدا یک فایل انتخاب کنید.")
            return
        try:
            people = load_data(path)
            result = compute(people)
        except Exception as e:
            messagebox.showerror("خطا", f"محاسبه انجام نشد:\n{e}")
            return

        self.tree.delete(*self.tree.get_children())
        for person in people:
            g = result[person]["gene"]
            t = result[person]["trait"]
            self.tree.insert("", "end", values=(
                f"{t[False]:.4f}", f"{t[True]:.4f}",
                f"{g[2]:.4f}", f"{g[1]:.4f}", f"{g[0]:.4f}",
                person,
            ))
        self.status.set(f"تعداد افراد: {len(people)}")


if __name__ == "__main__":
    App().mainloop()
