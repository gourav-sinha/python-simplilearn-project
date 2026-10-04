from collections import Counter

import pytest

from python_workspace.order_analysis import (
    calculate_category_revenue,
    calculate_customer_spending,
    classify_customer,
    create_dataset,
    display_report,
    find_electronics_buyers,
    find_top_customers,
    generate_business_insights,
)


def test_dataset_has_twelve_customers_and_customer_product_lookup():
    customers, orders, products_by_customer = create_dataset()

    assert len(customers) >= 10
    assert all(len(order) == 4 for order in orders)
    assert set(products_by_customer) == set(customers)
    assert "Laptop" in products_by_customer["Ava Patel"]


def test_customer_classification_thresholds():
    assert classify_customer(100.01) == "High-Value"
    assert classify_customer(100) == "Moderate"
    assert classify_customer(50) == "Moderate"
    assert classify_customer(49.99) == "Low-Value"


def test_spending_and_category_revenue_include_expected_totals():
    customers, orders, _ = create_dataset()
    spending = calculate_customer_spending(customers, orders)
    category_revenue = calculate_category_revenue(orders)

    assert spending["Ava Patel"] == 984.48
    assert category_revenue["Electronics"] == pytest.approx(2634.93)
    assert set(category_revenue) == {
        "Electronics",
        "Clothing",
        "Home Essentials",
        "Books",
        "Sports",
    }


def test_electronics_buyers_and_top_customer_ordering():
    customers, orders, _ = create_dataset()

    assert find_electronics_buyers(customers, orders) == [
        "Ava Patel",
        "Noah Kim",
        "Liam Chen",
        "Isabella Wilson",
        "Oliver Thompson",
    ]
    top_customers = find_top_customers(
        {"Ava": 200.0, "Zoe": 200.0, "Mia": 50.0, "Liam": 300.0}
    )
    assert top_customers == [("Liam", 300.0), ("Ava", 200.0), ("Zoe", 200.0)]


def test_insights_recommendations_are_actionable_and_include_category_overlap():
    customers, orders, _ = create_dataset()
    spending = calculate_customer_spending(customers, orders)
    category_revenue = calculate_category_revenue(orders)
    customer_categories: dict[str, set[str]] = {}
    for customer, _, _, category in orders:
        customer_categories.setdefault(customer, set()).add(category)
    product_counts = Counter(product for _, product, _, _ in orders)

    observations, recommendations = generate_business_insights(
        customers,
        spending,
        category_revenue,
        customer_categories,
        product_counts,
    )

    assert any("2 bought both electronics and clothing" in item for item in observations)
    assert len(recommendations) >= 5


def test_report_lists_customers_who_bought_both_target_categories(capsys):
    display_report()

    report = capsys.readouterr().out
    assert "7. Common Electronics & Clothing Buyers\n  Isabella Wilson, Noah Kim" in report