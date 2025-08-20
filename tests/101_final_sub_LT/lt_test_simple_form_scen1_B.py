from playwright.sync_api import sync_playwright
import time
import json
import urllib.parse

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

# MacOS Safari version of the test
# Global capabilities definition
capabilities = {
    "browserName": "MicrosoftEdge",
    "browserVersion": "latest",
    "LT:Options": {
        "user": "johndtwaldron",                                           # jdw username
        "accessKey": "LT_RgAgazoqPwEzCKKdfkS8MBDTz6xA6eVFCc2Y6LiRCcKq5Ph", # access key
        "platform": "macOS Monterey",
        "build": "LambdaTestPlaywrightBuild",
        "name": "Scenario 1 - Simple Form",                                # Simple Form - Scenario 1
        "network": True,
        "video": True,
        "console": True,
        "visual": True,
    }
}

def test_simple_form_lambda():
    playwright = sync_playwright().start()
    cap_str = urllib.parse.quote(json.dumps(capabilities))
    browser = playwright.chromium.connect(f"wss://cdp.lambdatest.com/playwright?capabilities={cap_str}")

    page = browser.new_page()

    # Step 1: Navigate
    page.goto("https://www.lambdatest.com/selenium-playground")
    page.click("text=Simple Form Demo")

    # Step 2: Validate we're on the correct URL
    assert "simple-form-demo" in page.url

    # Step 3: Wait for the correct input to be available
    page.wait_for_selector("input#user-message")

    # Step 4: Fill input and click
    test_message = "Welcome to LambdaTest"
    page.fill("input#user-message", test_message)
    page.click("button:has-text('Get Checked Value')")  # Updated selector

    # Step 5: Validate output
    page.wait_for_selector("#message")
    output = page.locator("#message").inner_text()
    print("✅ Output message:", output)
    assert test_message in output

    time.sleep(2)  # Allow time for video capture
    browser.close()
    playwright.stop()