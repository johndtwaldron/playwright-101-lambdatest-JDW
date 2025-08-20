from playwright.sync_api import sync_playwright
import json
import urllib.parse

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

# Chrome version of the test on Windows latest
# Global capabilities definition
capabilities = {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "LT:Options": {
        "user": "johndtwaldron",                                            # jdw username                   
        "accessKey": "LT_RgAgazoqPwEzCKKdfkS8MBDTz6xA6eVFCc2Y6LiRCcKq5Ph",  # access key
        "platform": "Windows 10",
        "build": "LambdaTestPlaywrightBuild",
        "name": "Scenario 3 - Form Submit Test",                            # Form Submit Test - Scenario 3
        "network": True,
        "video": True,
        "console": True,
        "visual": True
    }
}

def test_form_submission_lambda():
    playwright = sync_playwright().start()
    cap_str = urllib.parse.quote(json.dumps(capabilities))
    browser = playwright.chromium.connect(f"wss://cdp.lambdatest.com/playwright?capabilities={cap_str}")
    page = browser.new_page()
    page.goto("https://www.lambdatest.com/selenium-playground")

    page.click("text=Input Form Submit")
    page.wait_for_selector("form#seleniumform")
    page.click("form#seleniumform button[type='submit']")
    page.wait_for_timeout(1500)

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

    form.locator("button[type='submit']").click()
    page.wait_for_selector(".success-msg", timeout=10000)
    msg = page.locator(".success-msg").inner_text()
    print("🎉 Success Message:", msg)
    assert "Thanks for contacting us" in msg

    browser.close()
    playwright.stop()
