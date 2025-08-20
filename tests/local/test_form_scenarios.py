from playwright.sync_api import sync_playwright

def run_slider_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")
        page.click("text=Drag & Drop Sliders")
        slider = page.locator("input[type='range']").nth(2)
        output = page.locator("#rangeSuccess")
        box = slider.bounding_box()
        click_x = box["x"] + (box["width"] * 0.93)
        click_y = box["y"] + box["height"] / 2
        page.mouse.click(click_x, click_y)
        page.wait_for_timeout(500)
        final = output.inner_text()
        print("🎯 Slider Value:", final)
        assert final == "95"
        page.wait_for_timeout(4000)  # wait 4 seconds before ending
        browser.close()

def run_simple_form_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground/simple-form-demo")

        page.fill("input#user-message", "Hello LambdaTest!")
        page.click("button#showInput")

        output = page.locator("#message").text_content()
        print(f"OUTPUT: {output}")
        assert output.strip() == "Hello LambdaTest!"
        page.wait_for_timeout(4000)  # wait 4 seconds before ending
        browser.close()

def run_input_form_submit_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")
        with page.expect_navigation():
            page.click("text=Input Form Submit")
        page.wait_for_selector("form#seleniumform")
        page.click("form#seleniumform button[type='submit']")
        page.wait_for_timeout(1500)
        is_valid = page.eval_on_selector("form#seleniumform input[name='name']", "el => el.checkValidity()")
        assert not is_valid, "Expected 'name' input to be invalid after empty submit"

        form = page.locator("form#seleniumform")
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
        popup_close = page.locator("div#exit_popup button:has-text('×')")
        if popup_close.is_visible():
            popup_close.click()
            page.wait_for_timeout(500)
        form.locator("button[type='submit']").click()
        page.wait_for_selector(".success-msg", timeout=10000)
        msg = page.locator(".success-msg").inner_text()
        print("🎉 Success Message:", msg)
        assert "Thanks for contacting us" in msg
        page.wait_for_timeout(4000)  # wait 4 seconds before ending
        browser.close()

# Final runner
def test_all_three_scenarios():
    run_slider_test()
    run_simple_form_test()
    run_input_form_submit_test()
