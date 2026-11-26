import tkinter as tk
from tkinter import messagebox, ttk


pizza_prices = {
    "Pepperoni": 299,
    "Sausage": 329,
    "Hawaiian": 269,
    "Mushroom": 349,
}

size_prices = {
    "Small": 0,
    "Medium": 60,
    "Large": 120,
    "Extra Large": 180,
}

topping_prices = {
    "Extra Cheese": 35,
    "Onions": 25,
    "Black Olives": 40,
}

SKY_BLUE = "#73C8F0"
DEEP_BLUE = "#2878A8"
PALE_YELLOW = "#FFF3B0"
CARD = "#FFFCED"
TEXT = "#263746"
RECEIPT_BG = "#183B56"
RECEIPT_FG = "#FFF9DF"

window = tk.Tk()
window.title("Pizza Ordering System")
window.geometry("860x660")
window.minsize(780, 600)
window.configure(bg=SKY_BLUE)

pizza_var = tk.StringVar(value="Pepperoni")
size_var = tk.StringVar(value="Small")
quantity_var = tk.IntVar(value=1)
topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}

header = tk.Frame(window, bg=DEEP_BLUE)
header.pack(fill="x")

tk.Label(
    header,
    text="PIZZA ORDERING SYSTEM",
    font=("Arial", 19, "bold"),
    bg=DEEP_BLUE,
    fg="white",
).pack(pady=(12, 0))

tk.Label(
    header,
    text="Choose your pizza and place your order",
    font=("Arial", 10),
    bg=DEEP_BLUE,
    fg="#E5F6FF",
).pack(pady=(0, 12))

body = tk.Frame(window, bg=SKY_BLUE)
body.pack(fill="both", expand=True, padx=14, pady=14)
body.columnconfigure(0, weight=3)
body.columnconfigure(1, weight=2)
body.rowconfigure(0, weight=1)

form = tk.Frame(
    body,
    bg=CARD,
    padx=16,
    pady=12,
    highlightthickness=1,
    highlightbackground="#E6D88E",
)
form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
form.columnconfigure(0, weight=1)
form.columnconfigure(1, weight=1)


def section_label(text, row):
    tk.Label(
        form,
        text=text,
        font=("Arial", 11, "bold"),
        bg=CARD,
        fg=DEEP_BLUE,
    ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 4))


section_label("Pizza Flavor", 0)
pizza_dropdown = ttk.Combobox(
    form,
    textvariable=pizza_var,
    values=list(pizza_prices),
    state="readonly",
    font=("Arial", 10),
)
pizza_dropdown.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 4))

section_label("Pizza Size", 2)
size_frame = tk.Frame(form, bg=CARD)
size_frame.grid(row=3, column=0, columnspan=2, sticky="w")
for index, (size, price) in enumerate(size_prices.items()):
    tk.Radiobutton(
        size_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
        font=("Arial", 10),
        bg=CARD,
        fg=TEXT,
        activebackground=CARD,
        selectcolor=PALE_YELLOW,
    ).grid(row=index // 2, column=index % 2, sticky="w", padx=(0, 12))

section_label("Extra Toppings", 4)
for index, (topping, price) in enumerate(topping_prices.items()):
    tk.Checkbutton(
        form,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Arial", 10),
        bg=CARD,
        fg=TEXT,
        activebackground=CARD,
        selectcolor=PALE_YELLOW,
    ).grid(row=5 + index, column=0, columnspan=2, sticky="w")

section_label("Quantity", 8)
quantity_spinbox = tk.Spinbox(
    form,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Arial", 11),
    width=6,
)
quantity_spinbox.grid(row=9, column=0, sticky="w")

live_price_label = tk.Label(
    form,
    font=("Arial", 12, "bold"),
    bg=CARD,
    fg=DEEP_BLUE,
)
live_price_label.grid(
    row=10,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(12, 0),
)

summary = tk.Frame(
    body,
    bg=CARD,
    padx=12,
    pady=12,
    highlightthickness=1,
    highlightbackground="#E6D88E",
)
summary.grid(row=0, column=1, sticky="nsew")
summary.rowconfigure(1, weight=1)
summary.columnconfigure(0, weight=1)

tk.Label(
    summary,
    text="ORDER SUMMARY",
    font=("Arial", 12, "bold"),
    bg=CARD,
    fg=DEEP_BLUE,
).grid(row=0, column=0, sticky="w", pady=(0, 6))

receipt_text = tk.Text(
    summary,
    height=12,
    width=30,
    font=("Consolas", 10),
    bg=RECEIPT_BG,
    fg=RECEIPT_FG,
    insertbackground="white",
    relief="flat",
    padx=8,
    pady=8,
)
receipt_text.grid(row=1, column=0, sticky="nsew")


def price_per_pizza():
    toppings_total = sum(
        topping_prices[topping]
        for topping, variable in topping_vars.items()
        if variable.get()
    )
    return pizza_prices[pizza_var.get()] + size_prices[size_var.get()] + toppings_total


def refresh_live_price(*_):
    live_price_label.config(text=f"Price per pizza: ₱{price_per_pizza():,.2f}")


def calculate_total():
    try:
        quantity = int(quantity_var.get())
        if not 1 <= quantity <= 50:
            raise ValueError
    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a quantity between 1 and 50.",
        )
        return

    if not messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?",
    ):
        return

    pizza = pizza_var.get()
    size = size_var.get()
    selected_toppings = [
        topping for topping, variable in topping_vars.items() if variable.get()
    ]
    per_pizza = price_per_pizza()
    total = per_pizza * quantity

    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, "===== ORDER RECEIPT =====\n\n")
    receipt_text.insert(tk.END, f"Flavor: {pizza} (₱{pizza_prices[pizza]})\n")
    receipt_text.insert(tk.END, f"Size: {size} (+₱{size_prices[size]})\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END,
                f"+ {topping}: ₱{topping_prices[topping]}\n",
            )
    else:
        receipt_text.insert(tk.END, "No extra toppings\n")

    receipt_text.insert(tk.END, f"\nPrice per pizza: ₱{per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity: {quantity}\n")
    receipt_text.insert(tk.END, "-" * 26 + "\n")
    receipt_text.insert(tk.END, f"TOTAL: ₱{total:,.2f}\n")
    receipt_text.insert(tk.END, "\nThank you for ordering!\n")


def reset_order():
    pizza_var.set("Pepperoni")
    size_var.set("Small")
    quantity_var.set(1)
    for variable in topping_vars.values():
        variable.set(False)
    receipt_text.delete("1.0", tk.END)


button_frame = tk.Frame(summary, bg=CARD)
button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
button_frame.columnconfigure(0, weight=2)
button_frame.columnconfigure(1, weight=1)

tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 10, "bold"),
    bg=DEEP_BLUE,
    fg="white",
    activebackground="#1D5F88",
    activeforeground="white",
    relief="flat",
    command=calculate_total,
).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=6)

tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 10, "bold"),
    bg="#E7C94B",
    fg=TEXT,
    activebackground="#DDBD2F",
    relief="flat",
    command=reset_order,
).grid(row=0, column=1, sticky="ew", padx=(4, 0), ipady=6)

pizza_var.trace_add("write", refresh_live_price)
size_var.trace_add("write", refresh_live_price)
for variable in topping_vars.values():
    variable.trace_add("write", refresh_live_price)
refresh_live_price()

window.mainloop()
