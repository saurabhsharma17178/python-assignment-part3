# Python Assignment Part 3
# Product Explorer & Error-Resilient Logger
# Author: Saurabh Sharma

print("\n========== PART 3 PROGRAM START ==========")

# =====================================================
# Task 1 — File Read & Write Basics
# =====================================================

print("\n===== Task 1: File Read & Write =====")

# Lines to write into file
notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

# Write lines to file
with open("python_notes.txt", "w", encoding="utf-8") as file:
    for line in notes:
        file.write(line + "\n")

print("File written successfully.")

# Append extra lines
with open("python_notes.txt", "a", encoding="utf-8") as file:
    file.write("Topic 6: Functions help reuse code.\n")
    file.write("Topic 7: APIs allow applications to communicate.\n")

print("Lines appended successfully.")

# Read file and print numbered lines
print("\nReading file:")
with open("python_notes.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.strip()}")

print("Total number of lines:", len(lines))

# Keyword search
keyword = input("\nEnter keyword to search: ").lower()
print("Matching lines:")
found = False

for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found.")


# =====================================================
# Task 2 — API Integration
# =====================================================

import requests

print("\n===== Task 2: API Integration =====")

base_url = "https://dummyjson.com/products"

# Fetch products
try:
    response = requests.get(base_url + "?limit=20", timeout=5)
    data = response.json()
    products = data["products"]

    print("\nID | Title | Category | Price | Rating")
    print("-" * 50)

    for product in products:
        print(f"{product['id']} | {product['title']} | {product['category']} | {product['price']} | {product['rating']}")

except Exception as e:
    print("Error fetching products:", e)

# Filter rating >= 4.5 and sort by price
print("\nFiltered Products (Rating >= 4.5)")
filtered = [p for p in products if p["rating"] >= 4.5]
filtered.sort(key=lambda x: x["price"], reverse=True)

for p in filtered:
    print(p["title"], "-", p["price"], "-", p["rating"])

# Fetch laptops category
print("\nLaptop Products:")
try:
    laptop_response = requests.get(base_url + "/category/laptops", timeout=5)
    laptops = laptop_response.json()["products"]

    for laptop in laptops:
        print(laptop["title"], "-", laptop["price"])
except Exception as e:
    print("Error fetching laptops:", e)

# POST request simulation
print("\nPOST Request Simulation:")
new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

try:
    post_response = requests.post(base_url + "/add", json=new_product, timeout=5)
    print(post_response.json())
except Exception as e:
    print("POST request failed:", e)


# =====================================================
# Task 3 — Exception Handling
# =====================================================

print("\n===== Task 3: Exception Handling =====")

# Guarded calculator
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nCalculator Tests:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# Guarded file reader
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{filename}' not found."
    finally:
        print("File operation attempt complete.")

print("\nReading python_notes.txt:")
print(read_file_safe("python_notes.txt"))

print("\nReading ghost_file.txt:")
print(read_file_safe("ghost_file.txt"))


# Input validation loop with API lookup
print("\nProduct Lookup System")

while True:
    user_input = input("Enter product ID (1-100) or 'quit': ")

    if user_input.lower() == "quit":
        print("Exiting lookup.")
        break

    if not user_input.isdigit():
        print("Invalid input. Enter number.")
        continue

    product_id = int(user_input)

    if product_id < 1 or product_id > 100:
        print("ID must be between 1 and 100.")
        continue

    try:
        response = requests.get(f"https://dummyjson.com/products/{product_id}", timeout=5)

        if response.status_code == 404:
            print("Product not found.")
        else:
            product = response.json()
            print("Product:", product["title"], "| Price:", product["price"])

    except Exception as e:
        print("Error:", e)


# =====================================================
# Task 4 — Logging to File
# =====================================================

print("\n===== Task 4: Logging to File =====")

from datetime import datetime

# Function to log errors
def log_error(message):
    with open("error_log.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {message}\n")

# Trigger connection error
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError:
    msg = "ERROR in fetch_products: ConnectionError — No connection could be made"
    print(msg)
    log_error(msg)

# Trigger HTTP 404 error
try:
    response = requests.get("https://dummyjson.com/products/9999", timeout=5)
    if response.status_code == 404:
        msg = "ERROR in lookup_product: HTTPError — 404 Not Found for product ID 9999"
        print(msg)
        log_error(msg)
except Exception as e:
    log_error(str(e))

# Print error log contents
print("\nError Log Contents:")
try:
    with open("error_log.txt", "r", encoding="utf-8") as file:
        print(file.read())
except FileNotFoundError:
    print("No error log file found.")

print("\n========== PROGRAM END ==========")
