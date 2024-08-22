from playwright.sync_api import Playwright

def test_scenario_one(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://magento.softwaretestingboard.com/")

    # Step 1: Using navigation menu, find mens Hoodies & Sweatshirts section.
    men_selector = 'a#ui-id-5'
    page.hover(men_selector)
    tops_selector = 'a#ui-id-17'
    page.hover(tops_selector)
    hoodies_and_sweatshirts_selector = 'a#ui-id-20'
    page.click(hoodies_and_sweatshirts_selector)

    # Step 2: Check/Assert that the displayed number of jackets matches the selected number of jackets displayed per page.
    displayed_hoodies = page.locator('.products-grid .product-item').count()
    hoodies_per_page = 12
    assert displayed_hoodies == hoodies_per_page, (
        f"Displayed hoodies ({displayed_hoodies}) do not match the expected number per page ({hoodies_per_page})."
    )

    # Step 3: Select “Frankie Sweatshirt” and open its details.
    page.get_by_role("link", name="Frankie Sweatshirt").first.click()

    # Step 4: Select size, color, and quantity
    page.get_by_label("M", exact=True).click()
    page.get_by_label("Yellow").click()
    page.get_by_label("Qty").fill("2")

    # Step 5: Add product to cart and check that cart icon is updated with product quantity.
    page.get_by_role("button", name="Add to Cart").click()

    # Wait for the cart icon to update with the correct quantity
    page.wait_for_selector('.qty .counter-number')

    # Get the cart quantity and assert it is updated correctly
    cart_quantity = page.inner_text('.qty .counter-number')
    assert cart_quantity == '2', (
        f"Expected cart quantity to be '2', but got {cart_quantity}"
    )

    # Step 6: Open cart and check if product match the one You added to the cart.
    page.locator('.showcart').click()
    product_name = page.locator('.minicart-items-wrapper .product-item-name a').inner_text().strip()
    assert product_name == 'Frankie Sweatshirt', (
        f"Expected product name to be Frankie Sweatshirt, but got {product_name}"
    )

    # Step 7: Proceed to checkout and complete the order
    page.get_by_role("button", name="Proceed to Checkout").click()

    # Fill in the required fields to complete the order.
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
