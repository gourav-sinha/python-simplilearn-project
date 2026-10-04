# Analyzing Customer Orders Using Python

A beginner-friendly e-commerce order analysis program built with Python lists,
tuples, dictionaries, sets, comprehensions, loops, and sorting. It prints a
customer, product, and category report from a repeatable sample dataset.

## Prerequisites

- Python 3.12 or newer

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run the report

```powershell
python -m python_workspace
analyze-customer-orders
```

The original greeting helper remains available as an optional CLI mode:

```powershell
python -m python_workspace "Ava"
```

## What the analysis does

The sample contains 12 customers and 27 orders across Electronics, Clothing,
Home Essentials, Books, and Sports. Each order is a tuple of customer, product,
price, and category, stored in a list. `create_dataset()` also builds the
customer-to-products dictionary. From those single-source orders, the program
derives the product-category mapping, per-customer spending and classification,
category revenue and contribution, electronics buyers, multi-category buyers,
the electronics-and-clothing intersection, and most frequently ordered products.

Classification boundaries are explicit: spending above $100 is High-Value,
$50 through $100 inclusive is Moderate, and below $50 is Low-Value. All sample
customers have at least one order; the spending calculator also retains a
customer with no orders at $0.00.

## Data structures

- **List of strings:** customer names, kept in report order.
- **List of tuples:** the canonical order rows `(customer, product, price, category)`.
- **Dictionary of lists:** each customer mapped to their ordered product names.
- **Dictionaries:** product categories, customer spending/classifications, and
	category revenue.
- **Sets:** distinct categories/products and category membership/intersections,
	preventing duplicate buyers in set-based analysis.
- **Counter:** product order frequency, including repeat purchases.

## Algorithm and complexity

The program initializes each customer's total, then makes one pass over the
orders to aggregate spending and another pass to aggregate category revenue.
Set membership makes unique and overlap queries efficient. The report sorts
customers, products, and categories only where a stable readable presentation is
useful.

Let $O$ be the number of orders, $C$ the number of customers, $P$ the number of
distinct products, and $K$ the number of categories. Building the lookup and
aggregates takes $O(O + C)$ time. Customer/category membership analysis takes
$O(O)$ expected time. Sorting the report is $O(C \log C + P \log P + K \log K)$;
top-customer selection currently sorts all customers, $O(C \log C)$. Overall
space usage is $O(O + C + P + K)$, with the original order list retained.

## Sample output

The full report is printed by the command above. Its key totals include:

```text
CUSTOMER ORDER ANALYSIS REPORT

Available categories (5): Books, Clothing, Electronics, Home Essentials, Sports
Electronics        $2,634.93 (75.92%)
Clothing             $194.95 ( 5.62%)
Home Essentials      $267.00 ( 7.69%)
Books                $141.98 ( 4.09%)
Sports               $231.88 ( 6.68%)
Total              $3,470.74

Top Customers
	1. Ava Patel            $984.48
	2. Isabella Wilson      $959.98
	3. Liam Chen            $413.98
```

The report also lists all customer totals and classifications, product mappings
and counts, buyers by category overlap, category contribution percentages, six
automatically generated observations, and six marketing/inventory recommendations.

## Business insights

For the included sample, Electronics is the largest revenue category and Books
the smallest. Five customers purchased electronics; Ava Patel, Noah Kim, Liam
Chen, Isabella Wilson, and Oliver Thompson purchased from that category. Ava
Noah Kim and Isabella Wilson purchased both Electronics and Clothing.
Most popular products are derived from order frequency rather than maintained as
a separate hardcoded list. The generated recommendations focus on loyalty,
cross-category bundles, low-category promotion testing, popular-item stock
planning, personalized recommendations, and re-engagement of inactive buyers.

## Future enhancements

- Load orders from CSV, a database, or an e-commerce API and validate incoming rows.
- Use `Decimal` or integer cents for exact currency arithmetic in production.
- Add date-aware revenue trends, cohort/retention analysis, and refund handling.
- Export reports to CSV/Excel or visualize category and customer trends.
- Add configurable classification thresholds and automated scheduled reporting.

## Run tests

```powershell
python -m pytest -q
```
