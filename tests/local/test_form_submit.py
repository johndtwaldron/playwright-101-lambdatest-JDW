from playwright.sync_api import sync_playwright

''' Test Scenario 3:
1. Open the https://www.lambdatest.com/selenium-playground page and
click “Input Form Submit”.
2. Click “Submit” without filling in any information in the form.
3. Assert “Please fill in the fields” error message.
4. Fill in Name, Email, and other fields.
5. From the Country drop-down, select “United States” using the text
property.
6. Fill in all fields and click “Submit”.
7. Once submitted, validate the success message “Thanks for contacting
us, we will get back to you shortly.” on the screen. 
'''

def test_input_form_submission():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")

        # Click Input Form Submit and wait for navigation
        with page.expect_navigation():
            page.click("text=Input Form Submit")

        # Ensure the form is loaded
        page.wait_for_selector("form#seleniumform")

        # Submit the form empty first
        page.click("form#seleniumform button[type='submit']")
        page.wait_for_timeout(1500)

        # Validate empty form triggers validation
        is_valid = page.eval_on_selector("form#seleniumform input[name='name']", "el => el.checkValidity()")
        assert not is_valid, "Expected 'name' input to be invalid after empty submit"

        form = page.locator("form#seleniumform")

        # Fill out the visible fields
        form.locator("input[name='name']").fill("John Doe")
        form.locator("input[name='email']").fill("john@example.com")
        form.locator("input[name='password']").fill("securePassword123")
        form.locator("input[name='company']").fill("Acme Inc")
        form.locator("input[name='website']").fill("https://example.com")
        form.locator("select[name='country']").select_option(label="United States")
        form.locator("input[name='city']").fill("New York")
        form.locator("input[name='address_line1']").fill("123 Main St")
        form.locator("input[name='address_line2']").fill("Apt 4B")
        form.locator("#inputState").fill("NY")
        form.locator("#inputZip").fill("10001")


        # Try closing the pop-up banner if it exists
        popup_close = page.locator("div#exit_popup button:has-text('×')")
        if popup_close.is_visible():
            popup_close.click()
            page.wait_for_timeout(500)

        # Submit the filled form
        form.locator("button[type='submit']").click()

        # Validate success message
        page.wait_for_selector(".success-msg", timeout=10000)
        msg = page.locator(".success-msg").inner_text()
        print("🎉 Success Message:", msg)
        assert "Thanks for contacting us, we will get back to you shortly." in msg
        page.wait_for_timeout(4000)  # wait 4 seconds before ending
        browser.close()