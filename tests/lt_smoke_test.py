from playwright.sync_api import sync_playwright
import json

def test_lambda_smoke():
    capabilities = {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "LT:Options": {
            "platform": "Windows 10",
            "build": "Smoke Test Build",
            "name": "LT Smoke Test",
            "user": "johndtwaldron",
            "accessKey": "LT_RgAgazoqPwEzCKKdfkS8MBDTz6xA6eVFCc2Y6LiRCcKq5Ph",
            "network": True,
            "console": True,
            "video": True,
            "visual": True
        }
    }

    ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={json.dumps(capabilities)}"

    with sync_playwright() as p:
        print("⏳ Connecting to LambdaTest Grid...")
        browser = p.chromium.connect(ws_endpoint)
        page = browser.new_page()
        page.goto("https://example.com")
        print("✅ Page loaded:", page.title())
        page.wait_for_timeout(3000)
        browser.close()
