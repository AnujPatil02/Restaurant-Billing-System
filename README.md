# 🧾 The Social Bistro — Restaurant Billing System

A desktop restaurant billing application built with **Python + Tkinter**. Manages order entry, bill generation, tax/discount calculation and receipt storage.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- 🧑‍🤝‍🧑 Customer details capture — name, phone, table number
- 🍔 Categorized menu (Snacks, Beverages) with quantity entry per item
- 💰 Configurable discount % and tax %
- 💳 Payment mode selection (Cash / Card / UPI)
- 🧮 Automatic subtotal, discount, tax, and grand total calculation
- 🧾 Formatted bill preview in-app
- 💾 Bill auto-saved as a timestamped `.txt` receipt
- 📂 "View Bills" window to browse and reopen past receipts
- 🎨 Custom gradient-themed UI

## Requirements

- Python 3.x
- Tkinter (bundled with standard Python installation)

No external/third-party packages required.

## Installation & Run

```bash
git clone <AnujPatil02>
cd <Restaurant-Billing-System>
python restaurant_billing_system.py
```

On first run, a `receipts/` folder is created automatically in the project directory.

## How to Use

1. Enter customer name, phone, and table number.
2. Enter quantities for ordered items under Snacks/Beverages.
3. Set discount % and tax % as applicable.
4. Choose payment method.
5. Click **Calculate** to generate the bill and save the receipt.
6. Optionally print the receipt when prompted.
7. Use **View Bills** to browse past receipts, or **Reset** to clear the form for a new order.

## Project Structure

```
├── restaurant_billing_system.py    # Main application source code
├── receipts/                       # Auto-generated timestamped bill receipts (.txt)
├── project_screenshot.png
└── README.md
```

## Concepts Demonstrated

| Concept                    | Where it's used                                       |
|-----------------------------|--------------------------------------------------------|
| Object-Oriented Programming | `BillingSystem` class encapsulating UI and logic        |
| GUI programming             | Tkinter widgets — Frame, Entry, Label, Combobox, Text   |
| File handling                | Writing `.txt` receipts |
| Dictionaries & data modeling| Menu stored as nested dictionaries (category → items)  |
| Directory/file management     | Auto-creating `receipts/` via `os.makedirs`             |
| System interaction            | Cross-platform printing via `subprocess` / `os.startfile` |
| Date-time handling            | Timestamps for receipts and sales records via `datetime` |

## Sample Bill Output

```
========================================
THE SOCIAL BISTRO
========================================
Date: 2026-07-17 14:32:10
Customer: John Doe | Phone: 9876543210 | Table: 4
----------------------------------------

-- Snacks --
Burger x 2 = ₹120
Pizza x 1 = ₹150

-- Beverages --
Coffee x 2 = ₹100
----------------------------------------
Subtotal: ₹370.00
Discount: ₹18.50
Tax: ₹17.58
TOTAL: ₹369.08
Payment Mode: UPI
========================================
Thank you! Visit Again!
