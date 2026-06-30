from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os
import csv
import subprocess
import platform

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("The Social Bistro - Billing System")
        self.root.geometry("1000x650")

        # Create receipts directory
        if not os.path.exists("receipts"):
            os.makedirs("receipts")

        # Menu data
        self.menu = {
            "Snacks": {"Burger": 60, "Sandwich": 60, "Fries": 70, "Pizza": 150, "Pasta": 120},
            "Beverages": {"Coke": 40, "Coffee": 50, "Tea": 30, "Mojito": 60, "Cold Coffee": 80}
        }

        # Variables
        self.quantities = {item: IntVar() for category in self.menu for item in self.menu[category]}
        self.customer_name = StringVar()
        self.customer_phone = StringVar()
        self.table_no = StringVar()
        self.discount = DoubleVar(value=0)
        self.tax_rate = DoubleVar(value=5)
        self.payment_method = StringVar(value="Cash")

        # Draw gradient background
        self.draw_gradient()

        # Build UI
        self.build_customer_frame()
        self.build_menu_frame()
        self.build_button_frame()
        self.build_bill_area()

    def draw_gradient(self):
        canvas = Canvas(self.root, width=970, height=1300, highlightthickness=0)
        canvas.place(x=0, y=0)
        for i in range(1300):
            r = int(255 - (255 - 230) * i / 1300)
            g = int(245 - (245 - 255) * i / 1300)
            b = int(230 - (230 - 200) * i / 1300)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, 970, i, fill=color)

    def build_customer_frame(self):
        frame = Frame(self.root, bg="#ffffff", bd=2, relief=RIDGE)
        frame.place(x=10, y=10, width=940, height=42)

        Label(frame, text="Customer Name:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
        Entry(frame, textvariable=self.customer_name, width=20).grid(row=0, column=1, padx=5)

        Label(frame, text="Phone:", font=("Arial", 12), bg="white").grid(row=0, column=2, padx=5)
        Entry(frame, textvariable=self.customer_phone, width=15).grid(row=0, column=3, padx=5)

        Label(frame, text="Table No:", font=("Arial", 12), bg="white").grid(row=0, column=4, padx=5)
        Entry(frame, textvariable=self.table_no, width=10).grid(row=0, column=5, padx=5)

    def build_menu_frame(self):
        frame = Frame(self.root, bg="#dfffe0", bd=2, relief=RIDGE)
        frame.place(x=10, y=90, width=480, height=180)

        col = 0
        for category, items in self.menu.items():
            cat_frame = Frame(frame, bg="#dfffe0")
            cat_frame.grid(row=0, column=col, padx=20)

            Label(cat_frame, text=category, font=("Arial", 16, "bold"), bg="#dfffe0", fg="#004d40").pack(anchor=W)
            for item, price in items.items():
                row_f = Frame(cat_frame, bg="#dfffe0")
                row_f.pack(anchor=W, pady=2)
                Label(row_f, text=f"{item} (₹{price})", font=("Arial", 12), bg="#dfffe0").pack(side=LEFT)
                Entry(row_f, textvariable=self.quantities[item], width=5).pack(side=LEFT)
            col += 1

    def build_button_frame(self):
        frame = Frame(self.root, bg="#f0fff0", bd=2, relief=RIDGE)
        frame.place(x=500, y=90, width=450, height=80)

        Label(frame, text="Discount %:", bg="#f0fff0").grid(row=0, column=0, padx=5)
        Entry(frame, textvariable=self.discount, width=5).grid(row=0, column=1, padx=5)

        Label(frame, text="Tax %:", bg="#f0fff0").grid(row=0, column=2, padx=5)
        Entry(frame, textvariable=self.tax_rate, width=5).grid(row=0, column=3, padx=5)

        Label(frame, text="Payment:", bg="#f0fff0").grid(row=0, column=4, padx=5)
        ttk.Combobox(frame, textvariable=self.payment_method, values=["Cash", "Card", "UPI"], width=8).grid(row=0, column=5, padx=5)

        Button(frame, text="Calculate", command=self.calculate_bill, bg="#008CBA", fg="white").grid(row=1, column=0, padx=5, pady=5)
        Button(frame, text="Reset", command=self.reset, bg="#f39c12", fg="white").grid(row=1, column=1, padx=5)
        Button(frame, text="Exit", command=self.root.destroy, bg="#c0392b", fg="white").grid(row=1, column=2, padx=5)
        Button(frame, text="View Bills", command=self.view_bills, bg="#27ae60", fg="white").grid(row=1, column=3, padx=5)

    def build_bill_area(self):
        Label(self.root, text="🧾 Bill Receipt", font=("Arial", 14, "bold"), bg="#dfffe0").place(x=10, y=300)
        self.bill_area = Text(self.root, height=30, width=117, font=("Courier", 10))
        self.bill_area.place(x=10, y=345)

    def calculate_bill(self):
        total = 0
        bill_text = f"{'='*40}\nTHE SOCIAL BISTRO\n{'='*40}\n"
        bill_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_text += f"Customer: {self.customer_name.get()} | Phone: {self.customer_phone.get()} | Table: {self.table_no.get()}\n"
        bill_text += f"{'-'*40}\n"

        for category in self.menu:
            bill_text += f"\n-- {category} --\n"
            for item, price in self.menu[category].items():
                qty = self.quantities[item].get()
                if qty > 0:
                    item_total = price * qty
                    total += item_total
                    bill_text += f"{item} x {qty} = ₹{item_total}\n"

        bill_text += f"{'-'*40}\nSubtotal: ₹{total:.2f}"
        discount_amt = total * (self.discount.get() / 100)
        total_after_discount = total - discount_amt
        tax_amt = total_after_discount * (self.tax_rate.get() / 100)
        grand_total = total_after_discount + tax_amt
        bill_text += f"\nDiscount: ₹{discount_amt:.2f}"
        bill_text += f"\nTax: ₹{tax_amt:.2f}"
        bill_text += f"\nTOTAL: ₹{grand_total:.2f}\n"
        bill_text += f"Payment Mode: {self.payment_method.get()}\n"
        bill_text += f"{'='*40}\nThank you! Visit Again!\n"

        self.bill_area.delete(1.0, END)
        self.bill_area.insert(END, bill_text)

        # Save to text file
        filename = f"receipts/Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as file:
            file.write(bill_text)

        # Save to CSV
        with open("sales.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             self.customer_name.get(),
                             self.customer_phone.get(),
                             self.table_no.get(),
                             total, discount_amt, tax_amt, grand_total,
                             self.payment_method.get()])

        # Ask to print
        if messagebox.askyesno("Print", "Do you want to print the receipt?"):
            self.print_bill(filename)

    def reset(self):
        for var in self.quantities.values():
            var.set(0)
        self.customer_name.set("")
        self.customer_phone.set("")
        self.table_no.set("")
        self.discount.set(0)
        self.tax_rate.set(5)
        self.payment_method.set("Cash")
        self.bill_area.delete(1.0, END)

    def view_bills(self):
        top = Toplevel(self.root)
        top.title("Past Bills")
        top.geometry("400x300")
        lb = Listbox(top, font=("Courier", 10))
        lb.pack(fill=BOTH, expand=True)
        for f in os.listdir("receipts"):
            lb.insert(END, f)

        def open_bill(event):
            file = lb.get(lb.curselection())
            with open(f"receipts/{file}", "r") as bill:
                content = bill.read()
            messagebox.showinfo("Bill Content", content)

        lb.bind("<Double-1>", open_bill)

    def print_bill(self, filename):
        if platform.system() == "Windows":
            os.startfile(filename, "print")
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["lp", filename])
        else:  # Linux
            subprocess.run(["lpr", filename])

if __name__ == "__main__":
    root = Tk()
    obj = BillingSystem(root)
    root.mainloop()
