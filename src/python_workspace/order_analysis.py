"""Analyze sample e-commerce orders and produce a business report."""

from __future__ import annotations

from collections import Counter
from typing import TypeAlias

Order: TypeAlias = tuple[str, str, float, str]


def create_dataset() -> tuple[list[str], list[Order], dict[str, list[str]]]:
    """Return customers, order tuples, and each customer's ordered products."""
    customers = [
        "Ava Patel",
        "Noah Kim",
        "Mia Garcia",
        "Liam Chen",
        "Sophia Brown",
        "Ethan Davis",
        "Isabella Wilson",
        "Lucas Martin",
        "Amara Johnson",
        "Oliver Thompson",
        "Zoe Anderson",
        "Leo Robinson",
    ]
    orders: list[Order] = [
        ("Ava Patel", "Laptop", 899.99, "Electronics"),
        ("Ava Patel", "Yoga Mat", 39.99, "Sports"),
        ("Ava Patel", "Desk Lamp", 44.50, "Home Essentials"),
        ("Noah Kim", "Headphones", 129.99, "Electronics"),
        ("Noah Kim", "T-Shirt", 24.99, "Clothing"),
        ("Noah Kim", "Python Basics", 39.00, "Books"),
        ("Mia Garcia", "T-Shirt", 24.99, "Clothing"),
        ("Mia Garcia", "Running Shoes", 79.95, "Sports"),
        ("Liam Chen", "Monitor", 249.99, "Electronics"),
        ("Liam Chen", "Keyboard", 74.99, "Electronics"),
        ("Liam Chen", "Coffee Maker", 89.00, "Home Essentials"),
        ("Sophia Brown", "Cookbook", 32.50, "Books"),
        ("Sophia Brown", "Desk Lamp", 44.50, "Home Essentials"),
        ("Ethan Davis", "Basketball", 34.95, "Sports"),
        ("Ethan Davis", "Water Bottle", 18.50, "Sports"),
        ("Isabella Wilson", "Laptop", 899.99, "Electronics"),
        ("Isabella Wilson", "Jeans", 59.99, "Clothing"),
        ("Lucas Martin", "Novel", 18.99, "Books"),
        ("Lucas Martin", "T-Shirt", 24.99, "Clothing"),
        ("Amara Johnson", "Coffee Maker", 89.00, "Home Essentials"),
        ("Amara Johnson", "Yoga Mat", 39.99, "Sports"),
        ("Oliver Thompson", "Headphones", 129.99, "Electronics"),
        ("Oliver Thompson", "Monitor", 249.99, "Electronics"),
        ("Oliver Thompson", "Novel", 18.99, "Books"),
        ("Zoe Anderson", "Jeans", 59.99, "Clothing"),
        ("Zoe Anderson", "Cookbook", 32.50, "Books"),
        ("Leo Robinson", "Water Bottle", 18.50, "Sports"),
    ]

    products_by_customer = {customer: [] for customer in customers}
    for customer, product, _, _ in orders:
        products_by_customer[customer].append(product)
    return customers, orders, products_by_customer


def classify_customer(spending: float) -> str:
    """Classify spending using the report's high/moderate/low thresholds."""
    if spending > 100:
        return "High-Value"
    if spending >= 50:
        return "Moderate"
    return "Low-Value"


def calculate_customer_spending(
    customers: list[str], orders: list[Order]
) -> dict[str, float]:
    """Calculate total order value for every customer, including zero orders."""
    spending = dict.fromkeys(customers, 0.0)
    for customer, _, price, _ in orders:
        spending[customer] += price
    return spending


def calculate_category_revenue(orders: list[Order]) -> dict[str, float]:
    """Return total revenue grouped by product category."""
    revenue: dict[str, float] = {}
    for _, _, price, category in orders:
        revenue[category] = revenue.get(category, 0.0) + price
    return revenue


def find_electronics_buyers(customers: list[str], orders: list[Order]) -> list[str]:
    """Return customers with at least one electronics order, in input order."""
    electronics_customers = {
        customer
        for customer, _, _, category in orders
        if category == "Electronics"
    }
    return [customer for customer in customers if customer in electronics_customers]


def find_top_customers(
    spending: dict[str, float], limit: int = 3
) -> list[tuple[str, float]]:
    """Return customers ranked by spending from highest to lowest."""
    return sorted(spending.items(), key=lambda item: (-item[1], item[0]))[:limit]


def generate_business_insights(
    customers: list[str],
    spending: dict[str, float],
    category_revenue: dict[str, float],
    customer_categories: dict[str, set[str]],
    product_counts: Counter[str],
) -> tuple[list[str], list[str]]:
    """Create concise observations and actionable business recommendations."""
    total_revenue = sum(category_revenue.values())
    highest_category = max(category_revenue, key=category_revenue.get)
    lowest_category = min(category_revenue, key=category_revenue.get)
    high_value_count = sum(value > 100 for value in spending.values())
    most_popular_count = max(product_counts.values())
    popular_products = sorted(
        product
        for product, count in product_counts.items()
        if count == most_popular_count
    )
    active_customer_count = sum(value > 0 for value in spending.values())
    electronics_and_clothing = {
        customer
        for customer, categories in customer_categories.items()
        if {"Electronics", "Clothing"}.issubset(categories)
    }
    multi_category_count = sum(
        len(categories) > 1 for categories in customer_categories.values()
    )

    observations = [
        f"{highest_category} is the leading category, generating "
        f"${category_revenue[highest_category]:,.2f} "
        f"({category_revenue[highest_category] / total_revenue:.2%} of revenue).",
        f"{lowest_category} has the lowest revenue at "
        f"${category_revenue[lowest_category]:,.2f}.",
        f"{high_value_count} of {len(customers)} customers are high-value buyers "
        "(spending above $100).",
        f"Most frequently purchased product(s): {', '.join(popular_products)} "
        f"({most_popular_count} orders).",
        f"{multi_category_count} customers purchased from multiple categories; "
        f"{len(electronics_and_clothing)} bought both electronics and clothing.",
        f"{active_customer_count} of {len(customers)} customers placed an order; "
        "cross-category bundles may increase repeat engagement.",
    ]
    recommendations = [
        f"Reward high-value buyers with early access or loyalty benefits; "
        f"there are {high_value_count} customers in this segment.",
        "Offer electronics-and-clothing bundles to the customers who already buy "
        "both categories, then measure conversion and basket size.",
        f"Test a targeted promotion for {lowest_category} to learn whether price, "
        "assortment, or visibility is limiting sales.",
        f"Review replenishment levels for {', '.join(popular_products)}, the "
        "most frequently ordered product(s), while tracking stock-outs.",
        "Use personalized cross-category recommendations to encourage single-"
        "category buyers to explore complementary products.",
        "Run a re-engagement campaign for customers with no orders and compare "
        "their response against a holdout group.",
    ]
    return observations, recommendations


def _customer_categories(orders: list[Order]) -> dict[str, set[str]]:
    """Map each customer to the distinct categories they purchased."""
    categories_by_customer: dict[str, set[str]] = {}
    for customer, _, _, category in orders:
        categories_by_customer.setdefault(customer, set()).add(category)
    return categories_by_customer


def display_report() -> None:
    """Print the complete customer order analysis report to the console."""
    customers, orders, _products_by_customer = create_dataset()
    product_categories = {product: category for _, product, _, category in orders}
    categories = set(product_categories.values())
    customer_spending = calculate_customer_spending(customers, orders)
    customer_classification = {
        customer: classify_customer(amount)
        for customer, amount in customer_spending.items()
    }
    category_revenue = calculate_category_revenue(orders)
    unique_products = {product for _, product, _, _ in orders}
    electronics_buyers = find_electronics_buyers(customers, orders)
    top_customers = find_top_customers(customer_spending)
    categories_by_customer = _customer_categories(orders)
    multi_category_buyers = sorted(
        customer
        for customer, customer_categories in categories_by_customer.items()
        if len(customer_categories) > 1
    )
    both_category_buyers = sorted(
        customer
        for customer, customer_categories in categories_by_customer.items()
        if {"Electronics", "Clothing"}.issubset(customer_categories)
    )
    product_counts = Counter(product for _, product, _, _ in orders)
    total_revenue = sum(category_revenue.values())
    observations, recommendations = generate_business_insights(
        customers,
        customer_spending,
        category_revenue,
        categories_by_customer,
        product_counts,
    )

    print("=" * 58)
    print("CUSTOMER ORDER ANALYSIS REPORT")
    print("=" * 58)
    print("\n1. Customer Spending Summary")
    print(f"{'Customer':<22} {'Spending':>12}  Classification")
    for customer in customers:
        print(
            f"{customer:<22} ${customer_spending[customer]:>10,.2f}  "
            f"{customer_classification[customer]}"
        )

    print("\n2. Customer Classification Summary")
    for classification in ("High-Value", "Moderate", "Low-Value"):
        members = [
            customer
            for customer, value in customer_classification.items()
            if value == classification
        ]
        print(f"{classification}: {len(members)} ({', '.join(members) or 'None'})")

    print("\n3. Revenue by Category")
    print("Product-category mapping:")
    for product, category in sorted(product_categories.items()):
        print(f"  {product}: {category}")
    print(f"Available categories ({len(categories)}): {', '.join(sorted(categories))}")
    for category in sorted(category_revenue):
        share = category_revenue[category] / total_revenue * 100
        print(
            f"  {category:<18} ${category_revenue[category]:>9,.2f} "
            f"({share:>5.2f}%)"
        )
    print(f"  {'Total':<18} ${total_revenue:>9,.2f}")

    print("\n4. Top Customers")
    for rank, (customer, amount) in enumerate(top_customers, start=1):
        print(f"  {rank}. {customer:<20} ${amount:,.2f}")

    print("\n5. Electronics Buyers")
    print(f"  {', '.join(electronics_buyers) or 'None'}")

    print("\n6. Multi-Category Buyers")
    print(f"  {', '.join(multi_category_buyers) or 'None'}")

    print("\n7. Common Electronics & Clothing Buyers")
    print(f"  {', '.join(both_category_buyers) or 'None'}")

    print("\n8. Unique Products")
    print(f"  Total: {len(unique_products)}")
    print(f"  Products: {', '.join(sorted(unique_products))}")
    print("  Product purchase counts:")
    for product, count in sorted(
        product_counts.items(), key=lambda item: (-item[1], item[0])
    ):
        print(f"    {product:<18} {count}")
    print("\n9. Key Business Insights")
    for observation in observations:
        print(f"  - {observation}")
    print("\n  Recommendations:")
    for number, recommendation in enumerate(recommendations, start=1):
        print(f"  {number}. {recommendation}")


if __name__ == "__main__":
    display_report()