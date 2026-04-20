import tkinter as tk
from tkinter import ttk, messagebox

BG = "#050505"
CARD = "#0d0d0d"
TEXT = "#ffffff"
MUTED = "#707070"
MINT = "#00FF9D"
ROSE = "#FF3D68"
GOLD = "#FFD700"
FONT_MONO = ("Courier", 10)
FONT_BOLD = ("Courier", 10, "bold")
FONT_TITLE = ("Courier", 11, "bold")
FONT_BIG = ("Courier", 28, "bold")
FONT_MED = ("Courier", 13, "bold")

expenses = []
income_val = [0]
budget_limit = [0]

root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("900x650")
root.configure(bg=BG)
root.resizable(True, True)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background="#0d0d0d", foreground=MUTED,
                padding=[20, 10], font=FONT_BOLD)
style.map("TNotebook.Tab", background=[("selected", BG)],
          foreground=[("selected", MINT)])
style.configure("Treeview", background=CARD, foreground=TEXT,
                fieldbackground=CARD, font=FONT_MONO, rowheight=28)
style.configure("Treeview.Heading", background=BG,
                foreground=MINT, font=FONT_BOLD)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

def lbl(parent, text, font=None, fg=TEXT, bg=BG, anchor="center"):
    return tk.Label(parent, text=text, font=font or FONT_MONO,
                    fg=fg, bg=bg, anchor=anchor)

def ent(parent, width=20, placeholder=""):
    e = tk.Entry(parent, width=width, font=FONT_MONO,
                 bg=CARD, fg=TEXT, insertbackground=MINT,
                 relief="flat", bd=8,
                 highlightthickness=1,
                 highlightcolor=MINT,
                 highlightbackground="#222222")
    if placeholder:
        e.insert(0, placeholder)
        e.config(fg=MUTED)
        def on_focus_in(event, _e=e, _p=placeholder):
            if _e.get() == _p:
                _e.delete(0, tk.END)
                _e.config(fg=TEXT)
        def on_focus_out(event, _e=e, _p=placeholder):
            if _e.get() == "":
                _e.insert(0, _p)
                _e.config(fg=MUTED)
        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
    return e

def btn(parent, text, cmd, fg=MINT):
    return tk.Button(parent, text=text, command=cmd,
                     font=FONT_BOLD, bg=BG, fg=fg,
                     relief="flat", padx=20, pady=8,
                     cursor="hand2",
                     highlightthickness=1,
                     highlightbackground=fg,
                     activebackground=fg,
                     activeforeground=BG)

# ══════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════
tab1 = tk.Frame(notebook, bg=BG)
notebook.add(tab1, text="DASHBOARD")

# TOP
top_wrap = tk.Frame(tab1, bg=CARD, pady=15)
top_wrap.pack(fill="x", padx=20, pady=(15, 5))
inner_top = tk.Frame(top_wrap, bg=CARD)
inner_top.pack(anchor="center")

lbl(inner_top, "MONTHLY BUDGET (₹)", fg=MUTED, font=FONT_TITLE, bg=CARD).grid(
    row=0, column=0, padx=25, pady=3)
budget_ent = ent(inner_top, width=18, placeholder="e.g. 5000")
budget_ent.grid(row=1, column=0, padx=25, pady=5)

def auto_update(event):
    try:
        bud = budget_ent.get().replace(",", "").strip()
        if bud in ("e.g. 5000", ""):
            return
        budget_limit[0] = float(bud)
        income_val[0] = float(bud)
        refresh_all()
    except:
        pass

budget_ent.bind("<KeyRelease>", auto_update)


# BIG NUMBERS ROW
numbers_row = tk.Frame(tab1, bg=BG)
numbers_row.pack(fill="x", padx=20, pady=(8, 2))
numbers_row.columnconfigure(0, weight=1, uniform="half")
numbers_row.columnconfigure(1, weight=1, uniform="half")

left_num = tk.Frame(numbers_row, bg=BG)
left_num.grid(row=0, column=0, sticky="ew")
lbl(left_num, "TOTAL SPENT", fg=MUTED, font=FONT_TITLE).pack()
spent_display = tk.Label(left_num, text="₹ 0.00", font=FONT_BIG, fg=ROSE, bg=BG)
spent_display.pack()

right_num = tk.Frame(numbers_row, bg=BG)
right_num.grid(row=0, column=1, sticky="ew")
lbl(right_num, "REMAINING BUDGET", fg=MUTED, font=FONT_TITLE).pack()
remaining_display = tk.Label(right_num, text="₹ 0.00", font=FONT_BIG, fg=MINT, bg=BG)
remaining_display.pack()
budget_status_lbl = tk.Label(right_num, text="SET BUDGET ABOVE",
                              font=FONT_TITLE, fg=MUTED, bg=BG)
budget_status_lbl.pack()

# BOTTOM ROW
bottom = tk.Frame(tab1, bg=BG)
bottom.pack(fill="both", expand=True, padx=20, pady=(4, 10))
bottom.columnconfigure(0, weight=1, uniform="half")
bottom.columnconfigure(1, weight=1, uniform="half")
bottom.rowconfigure(0, weight=1)

# LEFT — Add Expense
left_card = tk.Frame(bottom, bg=CARD)
left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

left_inner = tk.Frame(left_card, bg=CARD)
left_inner.place(relx=0.5, rely=0.05, anchor="n")

lbl(left_inner, "ADD EXPENSE", fg=MINT, font=FONT_MED, bg=CARD).pack(pady=(0, 12))

lbl(left_inner, "NAME", fg=MUTED, bg=CARD, anchor="w").pack(anchor="w")
exp_name = ent(left_inner, width=24, placeholder="e.g. Lunch")
exp_name.pack(anchor="w", pady=3)

lbl(left_inner, "AMOUNT (₹) — no commas", fg=MUTED, bg=CARD, anchor="w").pack(anchor="w")
exp_amount = ent(left_inner, width=24, placeholder="e.g. 1000")
exp_amount.pack(anchor="w", pady=3)

lbl(left_inner, "CATEGORY", fg=MUTED, bg=CARD, anchor="w").pack(anchor="w")
exp_cat = ttk.Combobox(left_inner,
                        values=["Food", "Transport", "Shopping",
                                "Bills", "Entertainment", "Other"],
                        width=21, font=FONT_MONO, state="readonly")
exp_cat.set("Food")
exp_cat.pack(anchor="w", pady=3)

# RIGHT — Monthly Summary
right_card = tk.Frame(bottom, bg=CARD)
right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

right_inner = tk.Frame(right_card, bg=CARD)
right_inner.pack(anchor="n", pady=15, padx=15, fill="both", expand=True)

lbl(right_inner, "MONTHLY SUMMARY", fg=MINT, font=FONT_MED, bg=CARD).pack(pady=(0, 10))
summary_box = tk.Text(right_inner, font=FONT_MONO,
                       bg=CARD, fg=TEXT, relief="flat",
                       padx=10, pady=10, state="disabled")
summary_box.pack(fill="both", expand=True)

# ── ALL LOGIC ──
def refresh_all():
    total = sum(e["amount"] for e in expenses)
    remaining = budget_limit[0] - total
    spent_display.config(text=f"₹ {total:,.2f}")
    remaining_display.config(text=f"₹ {remaining:,.2f}")

    if budget_limit[0] == 0:
        remaining_display.config(fg=MUTED)
        budget_status_lbl.config(text="SET BUDGET ABOVE", fg=MUTED)
    elif remaining < 0:
        remaining_display.config(fg=ROSE)
        budget_status_lbl.config(text="BUDGET EXCEEDED", fg=ROSE)
    elif remaining < budget_limit[0] * 0.2:
        remaining_display.config(fg=GOLD)
        budget_status_lbl.config(text="LOW BUDGET WARNING", fg=GOLD)
    else:
        remaining_display.config(fg=MINT)
        budget_status_lbl.config(text="SYSTEM STABLE", fg=MINT)

    cats = {}
    for e in expenses:
        cats[e["category"]] = cats.get(e["category"], 0) + e["amount"]
    savings = max(income_val[0] - total, 0)

    summary_box.config(state="normal")
    summary_box.delete(1.0, tk.END)
    summary_box.insert(tk.END, f"  MONTHLY BUDGET  ₹{budget_limit[0]:,.2f}\n")
    summary_box.insert(tk.END, f"  TOTAL SPENT     ₹{total:,.2f}\n")
    summary_box.insert(tk.END, f"  SAVINGS     ₹{savings:,.2f}\n")
    summary_box.insert(tk.END, "\n  " + "─" * 28 + "\n")
    summary_box.insert(tk.END, "  BY CATEGORY\n\n")
    for cat, amt in cats.items():
        summary_box.insert(tk.END, f"  {cat:<16} ₹{amt:,.2f}\n")
    if not cats:
        summary_box.insert(tk.END, "  No expenses added yet.\n")
    summary_box.config(state="disabled")

def add_expense():
    if budget_limit[0] == 0:
        messagebox.showwarning("Set Budget First", "Please set your income and budget limit before adding expenses.")
        return
    name = exp_name.get().strip()
    amount = exp_amount.get().strip()
    cat = exp_cat.get()
    if name in ("e.g. Lunch", "") or amount in ("e.g. 1000", ""):
        messagebox.showwarning("Missing", "Fill all fields.")
        return
    try:
        amt = float(amount.replace(",", ""))
    except:
        messagebox.showerror("Error", "Numbers only. No commas.")
        return
    expenses.append({"name": name, "amount": amt, "category": cat})
    exp_name.delete(0, tk.END)
    exp_name.insert(0, "e.g. Lunch")
    exp_name.config(fg=MUTED)
    exp_amount.delete(0, tk.END)
    exp_amount.insert(0, "e.g. 1000")
    exp_amount.config(fg=MUTED)
    refresh_all()

def delete_from_list():
    if not expenses:
        messagebox.showwarning("Empty", "No expenses to delete.")
        return
    popup = tk.Toplevel(root)
    popup.title("Delete Expense")
    popup.configure(bg=BG)
    popup.geometry("500x420")

    lbl(popup, "SELECT EXPENSE TO DELETE", fg=ROSE, font=FONT_MED).pack(pady=15)

    listbox = tk.Listbox(popup, font=FONT_MONO, bg=CARD, fg=TEXT,
                         selectbackground=ROSE, selectforeground=BG,
                         width=55, height=15, relief="flat", bd=5)
    listbox.pack(padx=20, pady=5)

    for i, e in enumerate(expenses):
        listbox.insert(tk.END, f"  {e['name']:<20} ₹{e['amount']:,.2f}   {e['category']}")

    def confirm_delete():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Select", "Select an expense first.")
            return
        index = selected[0]
        expenses.pop(index)
        refresh_all()
        popup.destroy()

    btn(popup, "CONFIRM DELETE", confirm_delete, fg=ROSE).pack(pady=10)
    
def view_expenses():
    popup = tk.Toplevel(root)
    popup.title("All Expenses")
    popup.configure(bg=BG)
    popup.geometry("500x420")
    popup.grab_set()

    lbl(popup, "ALL EXPENSES", fg=MINT, font=FONT_MED).pack(pady=15)

    tree = ttk.Treeview(popup, columns=("Name", "Amount", "Cat"),
                         show="headings", height=12)
    for col, w in [("Name", 180), ("Amount", 110), ("Cat", 130)]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")
    tree.pack(padx=20, pady=5)

    total = 0
    for e in expenses:
        tree.insert("", "end", values=(e["name"], f"₹{e['amount']:,.2f}", e["category"]))
        total += e["amount"]

    lbl(popup, f"TOTAL: ₹{total:,.2f}", fg=ROSE, font=FONT_BOLD).pack(pady=10)

btn_row = tk.Frame(left_inner, bg=CARD)
btn_row.pack(anchor="w", pady=12)
btn(btn_row, "ADD", add_expense).pack(side="left", padx=(0, 10))
btn(btn_row, "VIEW LIST", view_expenses).pack(side="left", padx=(0, 10))
btn(btn_row, "DELETE", delete_from_list, fg=ROSE).pack(side="left")

# ══════════════════════════════════════════
# TAB 2 — INVEST
# ══════════════════════════════════════════
tab2 = tk.Frame(notebook, bg=BG)
notebook.add(tab2, text="INVEST")

lbl(tab2, "INVESTMENT ADVISOR", fg=MUTED, font=FONT_TITLE).pack(pady=(30, 20))
inv_frame = tk.Frame(tab2, bg=BG)
inv_frame.pack()

lbl(inv_frame, "SAVINGS (₹)", fg=MUTED, bg=BG).grid(row=0, column=0, padx=20, pady=5)
lbl(inv_frame, "DURATION (YRS)", fg=MUTED, bg=BG).grid(row=0, column=1, padx=20, pady=5)
inv_savings = ent(inv_frame, placeholder="e.g. 10000")
inv_savings.grid(row=1, column=0, padx=20)
inv_years = ent(inv_frame, width=12, placeholder="e.g. 5")
inv_years.grid(row=1, column=1, padx=20)

def get_investment_advice():
    try:
        s = inv_savings.get().replace(",", "").strip()
        y = inv_years.get().strip()
        if s == "e.g. 10000": s = ""
        if y == "e.g. 5": y = ""
        savings = float(s)
        years = int(y)
    except:
        messagebox.showerror("Error", "Enter valid values. No commas.")
        return
    options = []
    if savings >= 100000:
        options.append(("FIXED DEPOSIT", "6.5%/yr", savings * (1.065 ** years)))
    if savings >= 500:
        options.append(("RECURRING DEPOSIT", "6.8%/yr", savings * (1.068 ** years)))
    if savings >= 500:
        options.append(("MUTUAL FUND SIP", "12%/yr", savings * (1.12 ** years)))
    if savings >= 10000:
        options.append(("GOLD INVESTMENT", "10%/yr", savings * (1.10 ** years)))
    if savings >= 25000:
        options.append(("STOCK MARKET", "15%/yr", savings * (1.15 ** years)))
    inv_result.config(state="normal")
    inv_result.delete(1.0, tk.END)
    inv_result.insert(tk.END, f"  SAVINGS: ₹{savings:,.2f}   DURATION: {years} YR(S)\n")
    inv_result.insert(tk.END, "  " + "─" * 55 + "\n\n")
    if options:
        inv_result.insert(tk.END, "  OPTION                  RATE         RETURNS\n\n")
        for name, rate, returns in options:
            inv_result.insert(tk.END, f"  {name:<22} {rate:<12} ₹{returns:,.2f}\n\n")
    else:
        inv_result.insert(tk.END, "  Minimum ₹500 required.")
    inv_result.insert(tk.END, "\n  * Estimates based on average market rates.")
    inv_result.config(state="disabled")

btn(tab2, "GET ADVICE", get_investment_advice).pack(pady=10)

inv_result = tk.Text(tab2, height=14, width=65, font=FONT_MONO,
                      bg=CARD, fg=TEXT, relief="flat",
                      padx=20, pady=15, state="disabled")
inv_result.pack(pady=(0, 15), padx=30)

# ══════════════════════════════════════════
# TAB 3 — SAVINGS GOAL
# ══════════════════════════════════════════
tab3 = tk.Frame(notebook, bg=BG)
notebook.add(tab3, text="SAVINGS GOAL")

lbl(tab3, "SAVINGS GOAL", fg=MUTED, font=FONT_TITLE).pack(pady=(20, 5))
goal_display = tk.Label(tab3, text="0%", font=FONT_BIG, fg=MINT, bg=BG)
goal_display.pack()
goal_status = lbl(tab3, "SET YOUR GOAL BELOW", fg=MUTED, font=FONT_BOLD)
goal_status.pack(pady=3)

gf = tk.Frame(tab3, bg=BG)
gf.pack(pady=10)

lbl(gf, "GOAL NAME", fg=MUTED, bg=BG).grid(row=0, column=0, padx=15, pady=5)
lbl(gf, "TARGET (₹)", fg=MUTED, bg=BG).grid(row=0, column=1, padx=15, pady=5)
lbl(gf, "SAVED (₹)", fg=MUTED, bg=BG).grid(row=0, column=2, padx=15, pady=5)

goal_name = ent(gf, width=18, placeholder="e.g. New Laptop")
goal_name.grid(row=1, column=0, padx=15)
goal_target = ent(gf, width=14, placeholder="e.g. 50000")
goal_target.grid(row=1, column=1, padx=15)
goal_saved_ent = ent(gf, width=14, placeholder="e.g. 12000")
goal_saved_ent.grid(row=1, column=2, padx=15)

canvas_bar = tk.Canvas(tab3, width=600, height=8,
                        bg="#1a1a1a", highlightthickness=0)
canvas_bar.pack(pady=15)
bar_fill = canvas_bar.create_rectangle(0, 0, 0, 8, fill=MINT, outline="")

def track_goal():
    try:
        name = goal_name.get().strip()
        t = goal_target.get().replace(",", "").strip()
        s = goal_saved_ent.get().replace(",", "").strip()
        if name == "e.g. New Laptop": name = ""
        if t == "e.g. 50000": t = ""
        if s == "e.g. 12000": s = ""
        target = float(t)
        saved = float(s)
    except:
        messagebox.showerror("Error", "Enter valid values. No commas.")
        return
    percent = min((saved / target) * 100, 100)
    remaining = max(target - saved, 0)
    goal_display.config(text=f"{percent:.1f}%", fg=MINT)
    goal_status.config(
        text=f"{name.upper()}  |  ₹{saved:,.2f} OF ₹{target:,.2f}  |  ₹{remaining:,.2f} LEFT",
        fg=MINT)
    bar_width = int((percent / 100) * 600)
    canvas_bar.itemconfig(bar_fill, fill=MINT)
    canvas_bar.coords(bar_fill, 0, 0, bar_width, 8)

btn(tab3, "TRACK", track_goal).pack(pady=10)

root.mainloop()