# Smart Cart - Mowa's Simple Guide 🏠

Mowa, think of this project like building a **House (Illu)**. Everything has its own room and purpose.

## 1. The Big Picture (House Plan)

Here is your project structure explained simply:

```
smart_cart/
├── app/                 # 🏠 MAIN HOUSE (Where people live/work)
├── scripts/             # 🛠️ TOOL SHED (For repairs & setup)
├── tests/               # 🩺 DOCTOR (Checkups to see if house is healthy)
├── alembic/             # 🚧 RENOVATIONS (Tracking changes to the building)
├── REQUIREMENTS.txt     # 🛒 SHOPPING LIST (Python libraries we need)
└── cleanup.bat          # 🧹 BROOM (Cleaning tool we just used)
```

---

## 2. Inside the House (`app/`) 🏠

This is where the actual work happens.

*   **`main.py` (The Front Gate)**
    *   **What it is:** The entry point.
    *   **What it does:** When someone visits your site (API), they come here first. It opens the doors.

*   **`api/` (The Waiters)** 🤵
    *   **What it is:** Does not cook food, just takes orders.
    *   **What it does:** Takes data from the user ("I want a discount") and passes it to the kitchen (`services`).

*   **`services/` (The Kitchen)** 👨‍🍳
    *   **What it is:** Where the cooking happens!
    *   **What it does:** This is the **Brain**. It calculates discounts, checks rules (Step-by-step vs Bulk), and decides the price.
    *   **Key File:** `cart_service.py` is the Head Chef.

*   **`models/` (The Storage Containers)** 📦
    *   **What it is:** How we store things in the fridge (Database).
    *   **What it does:** Defines what a "Discount" or "Order" looks like (e.g., ID, Price, Name).

*   **`schemas/` (The Menu Card)** 📜
    *   **What it is:** The list of what serves are available.
    *   **What it does:** Ensures customers order correctly. If they send bad data, the Schema rejects it before it hits the kitchen.

*   **`core/` (The Foundation)** 🏗️
    *   **What it is:** The base pillars.
    *   **What it does:** Connects to the Database (Postgres) and holds passwords.

---

## 3. The Tool Shed (`scripts/`) 🛠️

You don't live here, you just go here to fix things.

*   `mowa_setup.py`: **The Construction Crew.** Builds the house (Database) for the first time.
*   `simple_reset.py`: **The Demolition Team.** Destroys everything and rebuilds fresh. Use carefully!
*   `check_discounts.py`: **The Inventory Check.** Just looks at what discounts we have.

---

## 4. The Doctor (`tests/`) 🩺

*   `verify_final.py`: **Full Body Checkup.** It runs scenarios (buying 1 item, buying 2 items) to make sure the Project Logic is healthy.

---

## How Data Moves (The Flow)

1.  **User** knocks on the door (`main.py`).
2.  **Waiter** (`api/`) takes the Order.
3.  **Kitchen** (`services/`) cooks the logic (Calculates Discount).
    *   *Kitchen might check the Fridge (`models`/Database) for ingredients.*
4.  **Waiter** (`api/`) serves the result back to the **User**.

---

**Summary for you Mowa:**
*   Want to change **Logic**? Go to `services/`.
*   Want to add a new **API URL**? Go to `api/`.
*   Want to fix the **Database**? Use `scripts/`.

Simple & Neat! ✨
