from playwright.sync_api import sync_playwright

''' Test Scenario 2:
1. Open the https://www.lambdatest.com/selenium-playground page and
click “Drag & Drop Sliders”.
2. Select the slider “Default value 15” and drag the bar to make it 95 by
validating whether the range value shows 95.
'''

def test_click_slider_to_95():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")
        page.click("text=Drag & Drop Sliders")

        slider = page.locator("input[type='range']").nth(2)
        output = page.locator("#rangeSuccess")

        box = slider.bounding_box()
        if not box:
            raise Exception("Slider bounding box not found")

        # Click at 95% of slider width
        click_x = box["x"] + (box["width"] * 0.93)
        click_y = box["y"] + box["height"] / 2

        page.mouse.click(click_x, click_y)
        page.wait_for_timeout(500)

        final = output.inner_text()
        print("🎯 Final slider value:", final)
        assert final == "95"
        page.wait_for_timeout(4000)  # wait 4 seconds before ending
        browser.close()