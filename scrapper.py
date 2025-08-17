import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Create folders
os.makedirs("saved_pages", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)

def capture_full_screenshot(driver, save_path):
    """Capture full-page screenshot using CDP."""
    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    width = metrics["contentSize"]["width"]
    height = metrics["contentSize"]["height"]

    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "mobile": False,
        "width": width,
        "height": height,
        "deviceScaleFactor": 1,
        "screenOrientation": {"angle": 0, "type": "portraitPrimary"}
    })

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {"fromSurface": True})
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

def process_constituency(code_type, state_code, constituency_number):
    """Process a single constituency page."""
    url = f"https://results.eci.gov.in/PcResultGenJune2024/candidateswise-{code_type}{str(state_code).zfill(2)}{str(constituency_number)}.htm"
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(2)

        # Check for 404
        if "404" in driver.title or "Not Found" in driver.page_source:
            driver.quit()
            return False, f"[SKIP] {url} - 404 Not Found"

        # Save text
        txt_file = os.path.join("saved_pages", f"{code_type}{str(state_code).zfill(2)}{str(constituency_number)}.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(driver.find_element(By.TAG_NAME, "body").text)

        # Save screenshot
        png_file = os.path.join("screenshots", f"{code_type}{str(state_code).zfill(2)}{str(constituency_number)}.png")
        capture_full_screenshot(driver, png_file)

        driver.quit()
        return True, f"[OK] {url} -> {txt_file}, {png_file}"

    except WebDriverException as e:
        return False, f"[SKIP] {url} - WebDriverException: {e}"
    except Exception as e:
        return False, f"[SKIP] {url} - {e}"

# Define state and union territory ranges
state_range = range(1, 30)
ut_range = range(1, 10)

results = []
start_time = time.time()

# Loop over states and UTs
for code_type, codes in [("S", state_range), ("U", ut_range)]:
    for state_code in codes:
        consecutive_404 = 0
        constituency_number = 1

        while True:
            success, message = process_constituency(code_type, state_code, constituency_number)
            print(message)
            results.append(message)

            if success:
                consecutive_404 = 0
            else:
                consecutive_404 += 1

            if consecutive_404 >= 3:
                print(f"Skipping {code_type}{str(state_code).zfill(2)} after 3 consecutive 404s")
                break  # move to next state/UT

            constituency_number += 1

# Save log
with open("logs/results_log.txt", "w", encoding="utf-8") as log_file:
    log_file.write("\n".join(results))

print(f"Finished in {time.time() - start_time:.2f} seconds")
