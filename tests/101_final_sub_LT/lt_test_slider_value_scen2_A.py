from playwright.sync_api import sync_playwright
import json
import urllib.parse

''' Test Scenario 2:
1. Open the https://www.lambdatest.com/selenium-playground page and
click “Drag & Drop Sliders”.
2. Select the slider “Default value 15” and drag the bar to make it 95 by
validating whether the range value shows 95.
'''

# Chrome version of the test on Windows latest
# Global capabilities definition
capabilities = {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "LT:Options": {
        "user": "johndtwaldron",                                           # jdw username
        "accessKey": "LT_RgAgazoqPwEzCKKdfkS8MBDTz6xA6eVFCc2Y6LiRCcKq5Ph", # access key
        "platform": "Windows 10",
        "build": "LambdaTestPlaywrightBuild",
        "name": "Scenario 2 - Slider Value Test",                          # Slider Value Test - Scenario 2
        "network": True,
        "video": True,
        "console": True,
        "visual": True,
        "terminal": True
    }   
}

def test_click_slider_to_95_lambda():
        playwright = sync_playwright().start()
        cap_str = urllib.parse.quote(json.dumps(capabilities))
        browser = playwright.chromium.connect(f"wss://cdp.lambdatest.com/playwright?capabilities={cap_str}")
        page = browser.new_page()
        
        page.goto("https://www.lambdatest.com/selenium-playground")
        page.click("text=Drag & Drop Sliders")

        page.wait_for_timeout(1000) # 1000?
        # check for pop ups and the like: handle it
        try:
            cookie_button = page.locator("#cookie-consent-close")
            if cookie_button.is_visible():
                cookie_button.click()
                print("🍪 Cookie banner dismissed")
        except Exception as e:
            print("ℹ️ No cookie banner")

        # Accept all cookies if that button shows
        try:
            accept_button = page.locator("text=Allow All")
            if accept_button.is_visible():
                accept_button.click()
                print("✅ Accepted 'Accept All' cookies")
        except Exception:
            print("ℹ️ No 'Accept All' button")

        # Close newsletter popup/modal if it appears
        try:
            popup_close = page.locator(".close-popup, .close-button, .popup-dismiss").first
            if popup_close.is_visible():
                page.screenshot(path="before_modal_dismiss.png")
                popup_close.click()
                page.screenshot(path="after_modal_dismiss.png")
                print("❌ Newsletter popup closed")
        except Exception:
            print("ℹ️ No newsletter popup")

        slider = page.locator("input[type='range']").nth(2)
        output = page.locator("#rangeSuccess")

        # Wait for bounding box to be ready
        page.wait_for_timeout(1000)  # wait for slider to settle
        assert slider.is_visible(), "⚠️ Slider is not visible!"

        #page.add_locator_handler("text=Allow All") <- for cookie banner

        box = slider.bounding_box()
        print("🧠 Bounding box:", box)
        if not box:
            raise Exception("Slider bounding box not found")

        # Log initial value
        print("📍 Initial slider value:", output.inner_text())
        page.screenshot(path="slider_before_click.png") # Visual confirmation before click

        # Click at 95% of slider width
        click_x = box["x"] + (box["width"] * 0.9375) #9375 to 94 shift seems to work better for LT
        click_y = box["y"] + box["height"] / 2

        page.screenshot(path="full_before_click.png", full_page=True)
        print("🖱 Clicking at:", click_x, click_y)
        page.mouse.click(click_x, click_y)
        page.wait_for_timeout(500)

        final = output.inner_text()
        print("🎯 Final slider value:", final)
        assert final == "95"

        page.wait_for_timeout(4000)  # wait 4 seconds before ending
        browser.close()
        #page.wait_for_timeout(2000)  # Visual confirmation
        #browser.close()
        playwright.stop()