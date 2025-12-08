# --- MADL ---
# {
#   "method_name": "_init_",
#   "class_name": "",
#   "intent": "Auto-generated intent for _init_.",
#   "semantic_description": "Auto-generated description for _init_.",
#   "keywords": [],
#   "parameters": "def _init_(self, driver)",
#   "method_code": "def _init_(self, driver):\n        self.driver = driver\n        self.wait = WebDriverWait(driver, 10)\n"
# }

# --- END MADL ---


def _init_(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

def navigate_to_homepage(self):
        self.driver.get("https://www.amazon.in")

def click_sign_in_button(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-link-accountList"))).click()

# --- MADL ---
# {
#   "method_name": "enter_email",
#   "class_name": "",
#   "intent": "Auto-generated intent for enter_email.",
#   "semantic_description": "Auto-generated description for enter_email.",
#   "keywords": [],
#   "parameters": "def enter_email(self, email)",
#   "method_code": "def enter_email(self, email):\n        field = self.wait.until(EC.presence_of_element_located((By.ID, \"ap_email\")))\n        field.clear()\n        field.send_keys(email)\n"
# }

# --- END MADL ---


def enter_email(self, email):
        field = self.wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
        field.clear()
        field.send_keys(email)

def click_continue_after_email(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()

# --- MADL ---
# {
#   "method_name": "enter_password",
#   "class_name": "",
#   "intent": "Auto-generated intent for enter_password.",
#   "semantic_description": "Auto-generated description for enter_password.",
#   "keywords": [],
#   "parameters": "def enter_password(self, password)",
#   "method_code": "def enter_password(self, password):\n        field = self.wait.until(EC.presence_of_element_located((By.ID, \"ap_password\")))\n        field.clear()\n        field.send_keys(password)\n"
# }

# --- END MADL ---


def enter_password(self, password):
        field = self.wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
        field.clear()
        field.send_keys(password)

def submit_login(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()

# --- MADL ---
# {
#   "method_name": "login",
#   "class_name": "",
#   "intent": "Auto-generated intent for login.",
#   "semantic_description": "Auto-generated description for login.",
#   "keywords": [],
#   "parameters": "def login(self, email, password)",
#   "method_code": "def login(self, email, password):\n        self.navigate_to_homepage()\n        self.click_sign_in_button()\n        self.enter_email(email)\n        self.click_continue_after_email()\n        self.enter_password(password)\n        self.submit_login()\n"
# }

# --- END MADL ---


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
#   "class_name": "",
#   "intent": "Auto-generated intent for search_product.",
#   "semantic_description": "Auto-generated description for search_product.",
#   "keywords": [],
#   "parameters": "def search_product(self, product_name)",
#   "method_code": "def search_product(self, product_name):\n        search_box = self.wait.until(EC.presence_of_element_located((By.ID, \"twotabsearchtextbox\")))\n        search_box.clear()\n        search_box.send_keys(product_name)\n        search_box.submit()\n"
# }

# --- END MADL ---


def search_product(self, product_name):
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.submit()

# --- MADL ---
# {
#   "method_name": "apply_price_filter",
#   "class_name": "",
#   "intent": "Auto-generated intent for apply_price_filter.",
#   "semantic_description": "Auto-generated description for apply_price_filter.",
#   "keywords": [],
#   "parameters": "def apply_price_filter(self, min_price, max_price)",
#   "method_code": "def apply_price_filter(self, min_price, max_price):\n        min_field = self.wait.until(EC.presence_of_element_located((By.ID, \"low-price\")))\n        max_field = self.wait.until(EC.presence_of_element_located((By.ID, \"high-price\")))\n        min_field.send_keys(str(min_price))\n        max_field.send_keys(str(max_price))\n        self.driver.find_element(By.XPATH, \"//input[@class='a-button-input']\").click()\n"
# }

# --- END MADL ---


def apply_price_filter(self, min_price, max_price):
        min_field = self.wait.until(EC.presence_of_element_located((By.ID, "low-price")))
        max_field = self.wait.until(EC.presence_of_element_located((By.ID, "high-price")))
        min_field.send_keys(str(min_price))
        max_field.send_keys(str(max_price))
        self.driver.find_element(By.XPATH, "//input[@class='a-button-input']").click()

# --- MADL ---
# {
#   "method_name": "open_first_search_result",
#   "class_name": "",
#   "intent": "Auto-generated intent for open_first_search_result.",
#   "semantic_description": "Auto-generated description for open_first_search_result.",
#   "keywords": [],
#   "parameters": "def open_first_search_result(self)",
#   "method_code": "def open_first_search_result(self):\n        product = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//div[@data-cel-widget='search_result_1']//h2/a\")))\n        product.click()\n"
# }

# --- END MADL ---


def open_first_search_result(self):
        product = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-cel-widget='search_result_1']//h2/a")))
        product.click()

# # # # # # #

# --- MADL ---
# {
#   "method_name": "add_to_cart",
#   "class_name": "",
#   "intent": "Auto-generated intent for add_to_cart.",
#   "semantic_description": "Auto-generated description for add_to_cart.",
#   "keywords": [],
#   "parameters": "def add_to_cart(self)",
#   "method_code": "def add_to_cart(self):\n        btn = self.wait.until(EC.element_to_be_clickable((By.ID, \"add-to-cart-button\")))\n        btn.click()\n"
# }

# --- END MADL ---


def add_to_cart(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button")))
        btn.click()

# --- MADL ---
# {
#   "method_name": "open_cart",
#   "class_name": "",
#   "intent": "Auto-generated intent for open_cart.",
#   "semantic_description": "Auto-generated description for open_cart.",
#   "keywords": [],
#   "parameters": "def open_cart(self)",
#   "method_code": "def open_cart(self):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"nav-cart\"))).click()\n"
# }

# --- END MADL ---


def open_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-cart"))).click()

# --- MADL ---
# {
#   "method_name": "remove_first_cart_item",
#   "class_name": "",
#   "intent": "Auto-generated intent for remove_first_cart_item.",
#   "semantic_description": "Auto-generated description for remove_first_cart_item.",
#   "keywords": [],
#   "parameters": "def remove_first_cart_item(self)",
#   "method_code": "def remove_first_cart_item(self):\n        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//input[@value='Delete']\")))\n        delete_btn.click()\n"
# }

# --- END MADL ---


def remove_first_cart_item(self):
        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Delete']")))
        delete_btn.click()

# --- MADL ---
# {
#   "method_name": "get_cart_item_count",
#   "class_name": "",
#   "intent": "Auto-generated intent for get_cart_item_count.",
#   "semantic_description": "Auto-generated description for get_cart_item_count.",
#   "keywords": [],
#   "parameters": "def get_cart_item_count(self)",
#   "method_code": "def get_cart_item_count(self):\n        count_el = self.wait.until(EC.presence_of_element_located((By.ID, \"nav-cart-count\")))\n        return int(count_el.text.strip())\n"
# }

# --- END MADL ---


def get_cart_item_count(self):
        count_el = self.wait.until(EC.presence_of_element_located((By.ID, "nav-cart-count")))
        return int(count_el.text.strip())

# --- MADL ---
# {
#   "method_name": "proceed_to_checkout",
#   "class_name": "",
#   "intent": "Auto-generated intent for proceed_to_checkout.",
#   "semantic_description": "Auto-generated description for proceed_to_checkout.",
#   "keywords": [],
#   "parameters": "def proceed_to_checkout(self)",
#   "method_code": "def proceed_to_checkout(self):\n        btn = self.wait.until(EC.element_to_be_clickable((By.NAME, \"proceedToRetailCheckout\")))\n        btn.click()\n"
# }

# --- END MADL ---


def proceed_to_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.NAME, "proceedToRetailCheckout")))
        btn.click()

# --- MADL ---
# {
#   "method_name": "choose_delivery_address",
#   "class_name": "",
#   "intent": "Auto-generated intent for choose_delivery_address.",
#   "semantic_description": "Auto-generated description for choose_delivery_address.",
#   "keywords": [],
#   "parameters": "def choose_delivery_address(self)",
#   "method_code": "def choose_delivery_address(self):\n        addr = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//div[@id='address-book-entry-0']//a\")))\n        addr.click()\n"
# }

# --- END MADL ---


def choose_delivery_address(self):
        addr = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='address-book-entry-0']//a")))
        addr.click()

# --- MADL ---
# {
#   "method_name": "choose_delivery_option",
#   "class_name": "",
#   "intent": "Auto-generated intent for choose_delivery_option.",
#   "semantic_description": "Auto-generated description for choose_delivery_option.",
#   "keywords": [],
#   "parameters": "def choose_delivery_option(self)",
#   "method_code": "def choose_delivery_option(self):\n        opt = self.wait.until(EC.element_to_be_clickable((By.NAME, \"ppw-widgetEvent:SetPaymentPlanSelectContinueEvent\")))\n        opt.click()\n"
# }

# --- END MADL ---


def choose_delivery_option(self):
        opt = self.wait.until(EC.element_to_be_clickable((By.NAME, "ppw-widgetEvent:SetPaymentPlanSelectContinueEvent")))
        opt.click()

# --- MADL ---
# {
#   "method_name": "place_order",
#   "class_name": "",
#   "intent": "Auto-generated intent for place_order.",
#   "semantic_description": "Auto-generated description for place_order.",
#   "keywords": [],
#   "parameters": "def place_order(self)",
#   "method_code": "def place_order(self):\n        place = self.wait.until(EC.element_to_be_clickable((By.NAME, \"placeYourOrder1\")))\n        place.click()\n"
# }

# --- END MADL ---


def place_order(self):
        place = self.wait.until(EC.element_to_be_clickable((By.NAME, "placeYourOrder1")))
        place.click()

# --- MADL ---
# {
#   "method_name": "navigate_to_orders",
#   "class_name": "",
#   "intent": "Auto-generated intent for navigate_to_orders.",
#   "semantic_description": "Auto-generated description for navigate_to_orders.",
#   "keywords": [],
#   "parameters": "def navigate_to_orders(self)",
#   "method_code": "def navigate_to_orders(self):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"nav-orders\"))).click()\n"
# }

# --- END MADL ---


def navigate_to_orders(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-orders"))).click()

# --- MADL ---
# {
#   "method_name": "open_first_order",
#   "class_name": "",
#   "intent": "Auto-generated intent for open_first_order.",
#   "semantic_description": "Auto-generated description for open_first_order.",
#   "keywords": [],
#   "parameters": "def open_first_order(self)",
#   "method_code": "def open_first_order(self):\n        order = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//div[contains(@class,'order')]//a\")))\n        order.click()\n"
# }

# --- END MADL ---


def open_first_order(self):
        order = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'order')]//a")))
        order.click()

# --- MADL ---
# {
#   "method_name": "navigate_to_wishlist",
#   "class_name": "",
#   "intent": "Auto-generated intent for navigate_to_wishlist.",
#   "semantic_description": "Auto-generated description for navigate_to_wishlist.",
#   "keywords": [],
#   "parameters": "def navigate_to_wishlist(self)",
#   "method_code": "def navigate_to_wishlist(self):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"nav-wishlist\"))).click()\n"
# }

# --- END MADL ---


def navigate_to_wishlist(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-wishlist"))).click()

# --- MADL ---
# {
#   "method_name": "add_current_item_to_wishlist",
#   "class_name": "",
#   "intent": "Auto-generated intent for add_current_item_to_wishlist.",
#   "semantic_description": "Auto-generated description for add_current_item_to_wishlist.",
#   "keywords": [],
#   "parameters": "def add_current_item_to_wishlist(self)",
#   "method_code": "def add_current_item_to_wishlist(self):\n        btn = self.wait.until(EC.element_to_be_clickable((By.ID, \"add-to-wishlist-button-submit\")))\n        btn.click()\n"
# }

# --- END MADL ---


def add_current_item_to_wishlist(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-to-wishlist-button-submit")))
        btn.click()

# --- MADL ---
# {
#   "method_name": "select_default_wishlist",
#   "class_name": "",
#   "intent": "Auto-generated intent for select_default_wishlist.",
#   "semantic_description": "Auto-generated description for select_default_wishlist.",
#   "keywords": [],
#   "parameters": "def select_default_wishlist(self)",
#   "method_code": "def select_default_wishlist(self):\n        wl = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//span[text()='Wish List']\")))\n        wl.click()\n"
# }

# --- END MADL ---


def select_default_wishlist(self):
        wl = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Wish List']")))
        wl.click()

# --- MADL ---
# {
#   "method_name": "open_wishlist",
#   "class_name": "",
#   "intent": "Auto-generated intent for open_wishlist.",
#   "semantic_description": "Auto-generated description for open_wishlist.",
#   "keywords": [],
#   "parameters": "def open_wishlist(self)",
#   "method_code": "def open_wishlist(self):\n        self.driver.get(\"https://www.amazon.in/hz/wishlist/ls\")\n"
# }

# --- END MADL ---


def open_wishlist(self):
        self.driver.get("https://www.amazon.in/hz/wishlist/ls")

# --- MADL ---
# {
#   "method_name": "remove_wishlist_item",
#   "class_name": "",
#   "intent": "Auto-generated intent for remove_wishlist_item.",
#   "semantic_description": "Auto-generated description for remove_wishlist_item.",
#   "keywords": [],
#   "parameters": "def remove_wishlist_item(self)",
#   "method_code": "def remove_wishlist_item(self):\n        remove = self.wait.until(EC.element_to_be_clickable((By.NAME, \"submit.deleteItem\")))\n        remove.click()\n"
# }

# --- END MADL ---


def remove_wishlist_item(self):
        remove = self.wait.until(EC.element_to_be_clickable((By.NAME, "submit.deleteItem")))
        remove.click()

# --- MADL ---
# {
#   "method_name": "navigate_to_addresses",
#   "class_name": "",
#   "intent": "Auto-generated intent for navigate_to_addresses.",
#   "semantic_description": "Auto-generated description for navigate_to_addresses.",
#   "keywords": [],
#   "parameters": "def navigate_to_addresses(self)",
#   "method_code": "def navigate_to_addresses(self):\n        self.driver.get(\"https://www.amazon.in/a/addresses\")\n"
# }

# --- END MADL ---


def navigate_to_addresses(self):
        self.driver.get("https://www.amazon.in/a/addresses")

# --- MADL ---
# {
#   "method_name": "add_new_address",
#   "class_name": "",
#   "intent": "Auto-generated intent for add_new_address.",
#   "semantic_description": "Auto-generated description for add_new_address.",
#   "keywords": [],
#   "parameters": "def add_new_address(self, name, phone, pincode, line1)",
#   "method_code": "def add_new_address(self, name, phone, pincode, line1):\n        self.wait.until(EC.element_to_be_clickable((By.ID, \"ya-myab-address-add-link\"))).click()\n        self.wait.until(EC.presence_of_element_located((By.ID, \"address-ui-widgets-enterAddressFullName\"))).send_keys(name)\n        self.driver.find_element(By.ID, \"address-ui-widgets-enterAddressPhoneNumber\").send_keys(phone)\n        self.driver.find_element(By.ID, \"address-ui-widgets-enterAddressPostalCode\").send_keys(pincode)\n        self.driver.find_element(By.ID, \"address-ui-widgets-enterAddressLine1\").send_keys(line1)\n        self.driver.find_element(By.ID, \"address-ui-widgets-form-submit-button\").click()\n"
# }

# --- END MADL ---


def add_new_address(self, name, phone, pincode, line1):
        self.wait.until(EC.element_to_be_clickable((By.ID, "ya-myab-address-add-link"))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, "address-ui-widgets-enterAddressFullName"))).send_keys(name)
        self.driver.find_element(By.ID, "address-ui-widgets-enterAddressPhoneNumber").send_keys(phone)
        self.driver.find_element(By.ID, "address-ui-widgets-enterAddressPostalCode").send_keys(pincode)
        self.driver.find_element(By.ID, "address-ui-widgets-enterAddressLine1").send_keys(line1)
        self.driver.find_element(By.ID, "address-ui-widgets-form-submit-button").click()

# --- MADL ---
# {
#   "method_name": "delete_first_address",
#   "class_name": "",
#   "intent": "Auto-generated intent for delete_first_address.",
#   "semantic_description": "Auto-generated description for delete_first_address.",
#   "keywords": [],
#   "parameters": "def delete_first_address(self)",
#   "method_code": "def delete_first_address(self):\n        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//a[contains(@href, 'delete')]\")))\n        delete_btn.click()\n        confirm = self.wait.until(EC.element_to_be_clickable((By.ID, \"deleteAddressModal-announce\")))\n        confirm.click()\n"
# }

# --- END MADL ---


def delete_first_address(self):
        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'delete')]")))
        delete_btn.click()
        confirm = self.wait.until(EC.element_to_be_clickable((By.ID, "deleteAddressModal-announce")))
        confirm.click()

# --- MADL ---
# {
#   "method_name": "logout",
#   "class_name": "",
#   "intent": "Auto-generated intent for logout.",
#   "semantic_description": "Auto-generated description for logout.",
#   "keywords": [],
#   "parameters": "def logout(self)",
#   "method_code": "def logout(self):\n        self.logout_open_menu()\n        signout = self.wait.until(EC.element_to_be_clickable((By.XPATH, \"//span[text()='Sign Out']\")))\n        signout.click()\n"
# }

# --- END MADL ---


# --- MADL ---
# {
#   "method_name": "logout_open_menu",
#   "class_name": "",
#   "intent": "Auto-generated intent for logout_open_menu.",
#   "semantic_description": "Auto-generated description for logout_open_menu.",
#   "keywords": [],
#   "parameters": "def logout_open_menu(self)",
#   "method_code": "def logout_open_menu(self):\n        hover = self.wait.until(EC.presence_of_element_located((By.ID, \"nav-link-accountList\")))\n        self.driver.execute_script(\"arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles:true}));\", hover)\n"
# }

# --- END MADL ---


def logout_open_menu(self):
        hover = self.wait.until(EC.presence_of_element_located((By.ID, "nav-link-accountList")))
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles:true}));", hover)

def logout(self):
        self.logout_open_menu()
        signout = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign Out']")))
        signout.click()

# --- MADL ---
# {
#   "method_name": "validate_logged_in",
#   "class_name": "",
#   "intent": "Auto-generated intent for validate_logged_in.",
#   "semantic_description": "Auto-generated description for validate_logged_in.",
#   "keywords": [],
#   "parameters": "def validate_logged_in(self)",
#   "method_code": "def validate_logged_in(self):\n        profile = self.wait.until(EC.presence_of_element_located((By.ID, \"nav-link-accountList-nav-line-1\")))\n        return \"Hello\" in profile.text\n"
# }

# --- END MADL ---


def validate_logged_in(self):
        profile = self.wait.until(EC.presence_of_element_located((By.ID, "nav-link-accountList-nav-line-1")))
        return "Hello" in profile.text

# --- MADL ---
# {
#   "method_name": "validate_cart_has_items",
#   "class_name": "",
#   "intent": "Auto-generated intent for validate_cart_has_items.",
#   "semantic_description": "Auto-generated description for validate_cart_has_items.",
#   "keywords": [],
#   "parameters": "def validate_cart_has_items(self)",
#   "method_code": "def validate_cart_has_items(self):\n        return self.get_cart_item_count() > 0\n"
# }

# --- END MADL ---


def validate_cart_has_items(self):
        return self.get_cart_item_count() > 0

# --- MADL ---
# {
#   "method_name": "validate_wishlist_has_items",
#   "class_name": "",
#   "intent": "Auto-generated intent for validate_wishlist_has_items.",
#   "semantic_description": "Auto-generated description for validate_wishlist_has_items.",
#   "keywords": [],
#   "parameters": "def validate_wishlist_has_items(self)",
#   "method_code": "def validate_wishlist_has_items(self):\n        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, \"g-item-sortable\")))\n        return len(items) > 0\n"
# }

# --- END MADL ---


def validate_wishlist_has_items(self):
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "g-item-sortable")))
        return len(items) > 0

# --- MADL ---
# {
#   "method_name": "navigate_back",
#   "class_name": "",
#   "intent": "Auto-generated intent for navigate_back.",
#   "semantic_description": "Auto-generated description for navigate_back.",
#   "keywords": [],
#   "parameters": "def navigate_back(self)",
#   "method_code": "def navigate_back(self):\n        self.driver.back()\n"
# }

# --- END MADL ---


def navigate_back(self):
        self.driver.back()

# --- MADL ---
# {
#   "method_name": "refresh_page",
#   "class_name": "",
#   "intent": "Auto-generated intent for refresh_page.",
#   "semantic_description": "Auto-generated description for refresh_page.",
#   "keywords": [],
#   "parameters": "def refresh_page(self)",
#   "method_code": "def refresh_page(self):\n        self.driver.refresh()"
# }

# --- END MADL ---


def refresh_page(self):
        self.driver.refresh()