from playwright.sync_api import sync_playwright

''' Test Scenario 1:
1. Open LambdaTest’s Selenium Playground from
https://www.lambdatest.com/selenium-playground
2. Click “Simple Form Demo”.
3. Validate that the URL contains “simple-form-demo”.
4. Create a variable for a string value e.g.: “Welcome to LambdaTest”.
5. Use this variable to enter values in the “Enter Message” text box.
6. Click “Get Checked Value”.
7. Validate whether the same text message is displayed in the right-hand
panel under the “Your Message:” section.
'''

def test_simple_form():
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