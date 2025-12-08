def _init_(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

def navigate_to_homepage(self):
        self.driver.get("https://www.amazon.in")

def click_sign_in_button(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nav-link-accountList"))).click()

def enter_email(self, email):
        field = self.wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
        field.clear()
        field.send_keys(email)

def click_continue_after_email(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()

def enter_password(self, password):
        field = self.wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
        field.clear()
        field.send_keys(password)

def submit_login(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()

def login(self, email, password):
        self.navigate_to_homepage()
        self.click_sign_in_button()
        self.enter_email(email)
        self.click_continue_after_email()
        self.enter_password(password)
        self.submit_login()

def search_product(self, product_name):
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.submit()

def apply_price_filter(self, min_price, max_price):
        min_field = self.wait.until(EC.presence_of_element_located((By.ID, "low-price")))
        max_field = self.wait.until(EC.presence_of_element_located((By.ID, "high-price")))
        min_field.send_keys(str(min_price))
        max_field.send_keys(str(max_price))
        self.driver.find_element(By.XPATH, "//input[@class='a-button-input']").click()

def open_first_search_result(self):
        product = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-cel-widget='search_result_1']//h2/a")))
        product.click()

# # # # # # #

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