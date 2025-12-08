def _init_(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

# --- MADL ---
# {
#   "method_name": "navigate_to_homepage",
#   "class_name": "amazon_automation",
#   "intent": "Navigate to the Amazon homepage.",
#   "semantic_description": "This method navigates the browser to the Amazon India homepage using the provided WebDriver instance.",
#   "keywords": [
#     "navigation",
#     "homepage",
#     "amazon",
#     "browser",
#     "get"
#   ],
#   "parameters": "self",
#   "method_code": "def navigate_to_homepage(self):\n        self.driver.get(\"https://www.amazon.in\")"
# }
def navigate_to_homepage(self):
        self.driver.get("https://www.amazon.in")

# --- MADL ---
# {
#   "method_name": "click_sign_in_button",
#   "class_name": "amazon_automation",
#   "intent": "Click the sign-in button on the Amazon homepage.",
#   "semantic_description": "This method locates and clicks the 'Sign In' button, which is typically found in the navigation bar of the Amazon website, allowing users to initiate the login process.",
#   "keywords": [
#     "sign in",
#     "login",
#     "navigation",
#     "click",
#     "amazon"
#   ],
#   "parameters": "self",
#   "method_code": "def click_sign_in_button(self):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"nav-link-accountList\"))).click()"
# }
def click_sign_in_button(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-link-accountList"))).click()

# --- MADL ---
# {
#   "method_name": "enter_email",
#   "class_name": "amazon_automation",
#   "intent": "Enter email address into the email input field.",
#   "semantic_description": "This method locates the email input field on the page using its ID 'ap_email', clears any existing text, and then enters the provided email address into the field. This is a common action during login or registration processes.",
#   "keywords": [
#     "email",
#     "input",
#     "field",
#     "login",
#     "authentication",
#     "form"
#   ],
#   "parameters": "email (string)",
#   "method_code": "def enter_email(self, email):\n        field = self.wait.until(EC.presence_of_element_located((By.ID, \"ap_email\")))\n        field.clear()\n        field.send_keys(email)"
# }
def enter_email(self, email):
        field = self.wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
        field.clear()
        field.send_keys(email)

# --- MADL ---
# {
#   "method_name": "click_continue_after_email",
#   "class_name": "amazon_automation",
#   "intent": "Click the 'Continue' button after entering an email address.",
#   "semantic_description": "This method waits for the 'Continue' button, identified by its ID 'continue', to become clickable and then clicks it. This is a common action in user flows where a user provides an email and needs to proceed to the next step.",
#   "keywords": [
#     "click",
#     "continue",
#     "button",
#     "email",
#     "navigation"
#   ],
#   "parameters": "self",
#   "method_code": "def click_continue_after_email(self):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"continue\"))).click()"
# }
def click_continue_after_email(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()

# --- MADL ---
# {
#   "method_name": "enter_password",
#   "class_name": "amazon_automation",
#   "intent": "Enter password into the password field on a web page.",
#   "semantic_description": "This method locates the password input field by its ID ('ap_password'), clears any existing text, and then sends the provided password string to the field. This is a common action in web automation, particularly during login or registration processes.",
#   "keywords": [
#     "password",
#     "input",
#     "field",
#     "login",
#     "authentication",
#     "send keys",
#     "clear"
#   ],
#   "parameters": "self, password",
#   "method_code": "def enter_password(self, password):\n        field = self.wait.until(EC.presence_of_element_located((By.ID, \"ap_password\")))\n        field.clear()\n        field.send_keys(password)"
# }
def enter_password(self, password):
        field = self.wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
        field.clear()
        field.send_keys(password)

# --- MADL ---
# {
#   "method_name": "submit_login",
#   "class_name": "amazon_automation",
#   "intent": "Submits the login form by clicking the sign-in button.",
#   "semantic_description": "This method locates the 'signInSubmit' button on the page and clicks it, effectively submitting the login credentials that have been entered.",
#   "keywords": [
#     "login",
#     "submit",
#     "sign in",
#     "authentication",
#     "button"
#   ],
#   "parameters": "self",
#   "method_code": "def submit_login(self):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"signInSubmit\"))).click()"
# }
def submit_login(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()

# --- MADL ---
# {
#   "method_name": "login",
#   "class_name": "amazon_automation",
#   "intent": "Perform user login on the Amazon website.",
#   "semantic_description": "This method automates the process of logging into an Amazon account. It navigates to the homepage, clicks the sign-in button, enters the provided email address, proceeds to the password entry, and finally submits the login credentials.",
#   "keywords": [
#     "login",
#     "authentication",
#     "credentials",
#     "amazon",
#     "sign in"
#   ],
#   "parameters": "email, password",
#   "method_code": "def login(self, email, password):\n        self.navigate_to_homepage()\n        self.click_sign_in_button()\n        self.enter_email(email)\n        self.click_continue_after_email()\n        self.enter_password(password)\n        self.submit_login()"
# }
def login(self, email, password):
        self.navigate_to_homepage()
        self.click_sign_in_button()
        self.enter_email(email)
        self.click_continue_after_email()
        self.enter_password(password)
        self.submit_login()

# --- MADL ---
# {
#   "method_name": "search_product",
#   "class_name": "amazon_automation",
#   "intent": "Search for a product on Amazon",
#   "semantic_description": "This method locates the search bar on the Amazon homepage, clears any existing text, enters the provided product name, and submits the search query.",
#   "keywords": [
#     "search",
#     "product",
#     "amazon",
#     "automation",
#     "UI interaction"
#   ],
#   "parameters": "product_name (str)",
#   "method_code": "def search_product(self, product_name):\n        search_box = self.wait.until(EC.presence_of_element_located((By.ID, \"twotabsearchtextbox\")))\n        search_box.clear()\n        search_box.send_keys(product_name)\n        search_box.submit()"
# }
def search_product(self, product_name):
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.submit()

# --- MADL ---
# {
#   "method_name": "apply_price_filter",
#   "class_name": "amazon_automation",
#   "intent": "Applies a price filter to search results on Amazon.",
#   "semantic_description": "This method locates the minimum and maximum price input fields on an Amazon search results page, enters the provided minimum and maximum price values, and then clicks the 'Go' button to apply the filter.",
#   "keywords": [
#     "filter",
#     "price",
#     "amazon",
#     "search",
#     "input",
#     "apply"
#   ],
#   "parameters": "min_price (int/float), max_price (int/float)",
#   "method_code": "def apply_price_filter(self, min_price, max_price):\n        min_field = self.wait.until(EC.presence_of_element_located((By.ID, \"low-price\")))\n        max_field = self.wait.until(EC.presence_of_element_located((By.ID, \"high-price\")))\n        min_field.send_keys(str(min_price))\n        max_field.send_keys(str(max_price))\n        self.driver.find_element(By.XPATH, \"//input[@class='a-button-input']\").click()"
# }
def apply_price_filter(self, min_price, max_price):
        min_field = self.wait.until(EC.presence_of_element_located((By.ID, "low-price")))
        max_field = self.wait.until(EC.presence_of_element_located((By.ID, "high-price")))
        min_field.send_keys(str(min_price))
        max_field.send_keys(str(max_price))
        self.driver.find_element(By.XPATH, "//input[@class='a-button-input']").click()

# --- MADL ---
# {
#   "method_name": "open_first_search_result",
#   "class_name": "amazon_automation",
#   "intent": "Opens the first product listed in the search results.",
#   "semantic_description": "This method locates the first search result element on an Amazon page using a specific XPath, waits for it to be clickable, and then clicks on it. This action simulates a user selecting the first product from a search.",
#   "keywords": [
#     "search",
#     "result",
#     "product",
#     "open",
#     "click",
#     "navigation"
#   ],
#   "parameters": "self",
#   "method_code": "def open_first_search_result(self):\n        product = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//div[@data-cel-widget='search_result_1']//h2/a\")))\n        product.click()"
# }
def open_first_search_result(self):
        product = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-cel-widget='search_result_1']//h2/a")))
        product.click()

def add_to_cart(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button")))
        btn.click()

def open_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-cart"))).click()

def remove_first_cart_item(self):
        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Delete']")))
        delete_btn.click()

def get_cart_item_count(self):
        count_el = self.wait.until(EC.presence_of_element_located((By.ID, "nav-cart-count")))
        return int(count_el.text.strip())

def proceed_to_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.NAME, "proceedToRetailCheckout")))
        btn.click()

def choose_delivery_address(self):
        addr = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='address-book-entry-0']//a")))
        addr.click()

def choose_delivery_option(self):
        opt = self.wait.until(EC.element_to_be_clickable((By.NAME, "ppw-widgetEvent:SetPaymentPlanSelectContinueEvent")))
        opt.click()

def place_order(self):
        place = self.wait.until(EC.element_to_be_clickable((By.NAME, "placeYourOrder1")))
        place.click()

def navigate_to_orders(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-orders"))).click()

def open_first_order(self):
        order = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'order')]//a")))
        order.click()

def navigate_to_wishlist(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-wishlist"))).click()

def add_current_item_to_wishlist(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-to-wishlist-button-submit")))
        btn.click()

def select_default_wishlist(self):
        wl = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Wish List']")))
        wl.click()

def open_wishlist(self):
        self.driver.get("https://www.amazon.in/hz/wishlist/ls")

def remove_wishlist_item(self):
        remove = self.wait.until(EC.element_to_be_clickable((By.NAME, "submit.deleteItem")))
        remove.click()

def navigate_to_addresses(self):
        self.driver.get("https://www.amazon.in/a/addresses")

def add_new_address(self, name, phone, pincode, line1):
        self.wait.until(EC.element_to_be_clickable((By.ID, "ya-myab-address-add-link"))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, "address-ui-widgets-enterAddressFullName"))).send_keys(name)
        self.driver.find_element(By.ID, "address-ui-widgets-enterAddressPhoneNumber").send_keys(phone)
        self.driver.find_element(By.ID, "address-ui-widgets-enterAddressPostalCode").send_keys(pincode)
        self.driver.find_element(By.ID, "address-ui-widgets-enterAddressLine1").send_keys(line1)
        self.driver.find_element(By.ID, "address-ui-widgets-form-submit-button").click()

def delete_first_address(self):
        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'delete')]")))
        delete_btn.click()
        confirm = self.wait.until(EC.element_to_be_clickable((By.ID, "deleteAddressModal-announce")))
        confirm.click()

def logout_open_menu(self):
        hover = self.wait.until(EC.presence_of_element_located((By.ID, "nav-link-accountList")))
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles:true}));", hover)

def logout(self):
        self.logout_open_menu()
        signout = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign Out']")))
        signout.click()

def validate_logged_in(self):
        profile = self.wait.until(EC.presence_of_element_located((By.ID, "nav-link-accountList-nav-line-1")))
        return "Hello" in profile.text

def validate_cart_has_items(self):
        return self.get_cart_item_count() > 0

def validate_wishlist_has_items(self):
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "g-item-sortable")))
        return len(items) > 0

def navigate_back(self):
        self.driver.back()

def refresh_page(self):
        self.driver.refresh()