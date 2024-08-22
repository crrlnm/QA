from playwright.sync_api import Playwright

def test_scenario_two(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://magento.softwaretestingboard.com/")

    # Step 1: Using navigation menu, find women pants section.
    women_selector = 'a#ui-id-4'
    page.hover(women_selector)
    bottoms_selector = 'a#ui-id-10'
    page.hover(bottoms_selector)
    pants_selector = 'a#ui-id-15'
    page.click(pants_selector)

    # Step 2: Filter section to show the cheapest products available (sort by ascending price).
    sorter_action = page.wait_for_selector('.sorter-action')
    sort_direction = sorter_action.get_attribute('data-value')

    if sort_direction == "asc":
        sorter_action.click()     

    page.wait_for_selector("select#sorter")
    page.select_option("select#sorter", "price")
    products = page.locator('.product-items .product-item')

    # Step 3: Select the cheapest pants and add them to the cart.
    first_product = products.nth(0)
    first_product.locator('[attribute-code="size"] .swatch-option').first.click()
    first_product.locator('[attribute-code="color"] .swatch-option').first.click()
    add_to_cart_button = first_product.get_by_role("button", name="Add to Cart")
    add_to_cart_button.click()

    # Step 4: Add 2 more products to the cart. Check that cart icon is updated with each product.
    second_product = products.nth(1)
    second_product.locator('[attribute-code="size"] .swatch-option').first.click()
    second_product.locator('[attribute-code="color"] .swatch-option').first.click()
    add_to_cart_button = second_product.get_by_role("button", name="Add to Cart")
    add_to_cart_button.click()

    page.wait_for_selector('.qty .counter-number')
    cart_quantity = page.inner_text('.qty .counter-number')
    assert cart_quantity == '2', (
        f"Expected cart quantity to be '2', but got {cart_quantity}"
    )

    third_product = products.nth(2)
    third_product.locator('[attribute-code="size"] .swatch-option').first.click()
    third_product.locator('[attribute-code="color"] .swatch-option').first.click()
    add_to_cart_button = third_product.get_by_role("button", name="Add to Cart")
    add_to_cart_button.click()

    # Wait until the loading mask disappears, indicating the cart update is complete.
    page.wait_for_selector('.loading-mask', state='hidden')
    page.wait_for_selector('.qty .counter-number')
    cart_quantity = page.inner_text('.qty .counter-number')
    assert cart_quantity == '3', (
        f"Expected cart quantity to be '3', but got {cart_quantity}"
    )

    # Step 5: Open the cart and remove a product.
    page.locator('.showcart').click()
    page.get_by_role("link", name="View and Edit Cart").click()
    page.get_by_role("link", name="Remove item").nth(1).click()

    # Wait for the cart to update before checking the quantity again.
    page.wait_for_selector('.loading-mask', state='visible')
    page.wait_for_selector('.loading-mask', state='hidden')
    page.wait_for_selector('.qty .counter-number')
    cart_quantity = page.inner_text('.qty .counter-number')
    assert cart_quantity == '2', (
        f"Expected cart quantity to be '2', but got {cart_quantity}"
    )

    # Step 6: Add product to the cart from suggested products.
    crossell_products = page.locator('.products-crosssell .product-item')
    crossell_products.first.get_by_role("button", name="Add to Cart")

    # Step 7: Proceed to checkout.
    page.get_by_role("button", name="Proceed to Checkout").click()

    # Step 8: Fill in the required fields to complete the order.
    page.get_by_role("textbox", name="Email Address * Email Address*").fill("test@gmail.com")
    page.get_by_label("First Name").fill("K")
    page.get_by_label("Last Name").fill("M")
    page.get_by_label("Street Address: Line 1").fill("Street 123")
    page.get_by_label("City").fill("Forest")
    page.locator("select[name=\"region_id\"]").select_option("2")
    page.get_by_label("Zip/Postal Code").fill("12345")
    page.get_by_label("Phone Number").fill("00000000")
    page.get_by_label("Table Rate").check()

    # Proceed to the next step and place the order
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Place Order").click()

    # Close the context and browser to end the session.
    context.close()
    browser.close()