from playwright.sync_api import sync_playwright, expect
import uuid

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    BASE_URL = "http://127.0.0.1:8000"
    test_email = f"verify_{uuid.uuid4()}@example.com"
    test_password = "password123"

    try:
        # --- 1. Home Page ---
        print("Navigating to Home page...")
        page.goto(f"{BASE_URL}/")
        page.screenshot(path="01_home_page.png")

        # --- 2. Registration ---
        print("Navigating to Register page...")
        page.get_by_role("link", name="Register").click()
        expect(page).to_have_url(f"{BASE_URL}/register")

        print("Filling out registration form...")
        page.get_by_label("Username").fill("verifyuser")
        page.get_by_label("Email").fill(test_email)
        page.get_by_label("Password").fill(test_password)
        page.get_by_role("button", name="Register").click()

        # --- 3. Login ---
        print("Verifying redirect to login and flash message...")
        expect(page.get_by_text("Registration successful! Please log in.")).to_be_visible()
        page.screenshot(path="02_registration_success.png")

        print("Logging in...")
        page.get_by_label("Email").fill(test_email)
        page.get_by_label("Password").fill(test_password)
        page.get_by_role("button", name="Login").click()

        # --- 4. Dashboard ---
        print("Verifying dashboard...")
        expect(page.get_by_text("Welcome, verifyuser!")).to_be_visible()
        page.screenshot(path="03_dashboard.png")

        # --- 5. News Page ---
        print("Verifying News page...")
        page.get_by_role("link", name="News").click()
        expect(page.get_by_text("Latest Cybersecurity News")).to_be_visible()
        page.screenshot(path="04_news_page.png")

        # --- 6. Blog Page ---
        print("Verifying Blog page...")
        page.get_by_role("link", name="Blog").click()
        expect(page.get_by_text("Latest Blog Posts")).to_be_visible()
        page.screenshot(path="05_blog_page.png")

        # --- 7. Tasks Page ---
        print("Verifying Tasks page...")
        page.get_by_role("link", name="Tasks").click()
        expect(page.get_by_text("Your Daily Cybersecurity Task")).to_be_visible()
        page.screenshot(path="06_tasks_page.png")

        # --- 8. Tools Page & Password Analyzer ---
        print("Verifying Tools page...")
        page.get_by_role("link", name="Tools").click()
        expect(page.get_by_text("Password Strength Analyzer")).to_be_visible()
        page.screenshot(path="07_tools_page.png")

        print("Using Password Analyzer...")
        page.get_by_role("link", name="Use Tool").click()
        page.get_by_placeholder("Enter password...").fill("weak")
        page.get_by_role("button", name="Analyze").click()
        expect(page.get_by_text("Strength: Very Weak")).to_be_visible()
        page.screenshot(path="08_password_analyzer_result.png")

        # --- 9. Pricing & Payment Instructions ---
        print("Verifying Pricing page...")
        page.get_by_role("link", name="Pricing").click()
        page.screenshot(path="09_pricing_page_loggedin.png")

        print("Verifying Payment Instructions...")
        page.get_by_role("link", name="Choose Pro").click()
        expect(page.get_by_text("Manual Payment Instructions")).to_be_visible()
        page.screenshot(path="10_payment_instructions.png")

        # --- 10. Logout ---
        print("Logging out...")
        page.get_by_role("link", name="Logout").click()
        expect(page.get_by_text("You have been logged out.")).to_be_visible()
        page.screenshot(path="11_logout_page.png")

        print("Frontend verification successful!")

    except Exception as e:
        print(f"An error occurred during verification: {e}")
        page.screenshot(path="error.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)