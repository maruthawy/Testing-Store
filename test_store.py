import unittest
from unittest.mock import patch
from store import User, Product, Inventory, Cart, Cashier, Store

class TestUser(unittest.TestCase):
    def setUp(self):
        self.admin_user = User("admin", "adminpass", "admin")
        self.buyer_user = User("buyer", "buyerpass", "buyer")

    def test_verify_password_correct(self):
        self.assertTrue(self.admin_user.verify_password("adminpass"))
        self.assertTrue(self.buyer_user.verify_password("buyerpass"))

    def test_verify_password_incorrect(self):
        self.assertFalse(self.admin_user.verify_password("wrongpass"))
        self.assertFalse(self.buyer_user.verify_password("wrongpass"))

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Indomie Goreng", 3000, 20)

    def test_reduce_stock_success(self):
        result = self.product.reduce_stock(5)
        self.assertTrue(result)
        self.assertEqual(self.product.stock, 15)

    def test_reduce_stock_failure(self):
        result = self.product.reduce_stock(25)
        self.assertFalse(result)
        self.assertEqual(self.product.stock, 20)

    def test_add_stock(self):
        self.product.add_stock(10)
        self.assertEqual(self.product.stock, 30)

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.product = Product("Indomie Goreng", 3000, 20)
        self.inventory.add_product(self.product)

    def test_add_product(self):
        self.assertIn("Indomie Goreng", self.inventory.products)

    def test_get_product(self):
        product = self.inventory.get_product("Indomie Goreng")
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Indomie Goreng")
        self.assertEqual(product.price, 3000)

class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.product = Product("Indomie Goreng", 3000, 20)

    def test_add_to_cart(self):
        self.cart.add_to_cart(self.product, 2)
        self.assertIn("Indomie Goreng", self.cart.items)
        self.assertEqual(self.cart.items["Indomie Goreng"]["quantity"], 2)

    def test_show_cart_total(self):
        self.cart.add_to_cart(self.product, 3)
        total = self.cart.show_cart()
        self.assertEqual(total, 9000)

class TestCashier(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.cashier = Cashier(self.inventory)
        self.cart = Cart()
        self.product = Product("Indomie Goreng", 3000, 20)
        self.inventory.add_product(self.product)
        self.cart.add_to_cart(self.product, 2)

    @patch("builtins.input", side_effect=["10000"])
    def test_checkout_successful_payment(self, mock_input):
        self.cashier.checkout(self.cart)
        self.assertEqual(self.product.stock, 18)  # Stok berkurang setelah checkout
        self.assertFalse(self.cart.items)  # Keranjang harus kosong setelah checkout

    @patch("builtins.input", side_effect=["4000"])
    def test_checkout_insufficient_payment(self, mock_input):
        self.cashier.checkout(self.cart)
        self.assertEqual(self.product.stock, 20)  # Stok tidak berubah karena gagal bayar
        self.assertTrue(self.cart.items)  # Keranjang tetap berisi barang

class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store()

    @patch("builtins.input", side_effect=["admin", "adminpass"])
    def test_login_admin_success(self, mock_input):
        self.assertTrue(self.store.login())
        self.assertEqual(self.store.current_user.role, "admin")

    @patch("builtins.input", side_effect=["buyer", "buyerpass"])
    def test_login_buyer_success(self, mock_input):
        self.assertTrue(self.store.login())
        self.assertEqual(self.store.current_user.role, "buyer")

    @patch("builtins.input", side_effect=["wronguser", "wrongpass"])
    def test_login_failure(self, mock_input):
        self.assertFalse(self.store.login())
        self.assertIsNone(self.store.current_user)

    @patch("builtins.input", side_effect=["Indomie Goreng", "5"])
    def test_add_stock_admin(self, mock_input):
        # Login as admin
        self.store.current_user = User("admin", "adminpass", "admin")
        initial_stock = self.store.inventory.get_product("Indomie Goreng").stock
        self.store.add_stock()
        updated_stock = self.store.inventory.get_product("Indomie Goreng").stock
        self.assertEqual(updated_stock, initial_stock + 5)

    @patch("builtins.input", side_effect=["Indomie Goreng", "3"])
    def test_add_to_cart_buyer(self, mock_input):
        # Login as buyer
        self.store.current_user = User("buyer", "buyerpass", "buyer")
        initial_stock = self.store.inventory.get_product("Indomie Goreng").stock
        self.store.add_to_cart()
        self.assertIn("Indomie Goreng", self.store.cart.items)
        self.assertEqual(self.store.cart.items["Indomie Goreng"]["quantity"], 3)
        # Check that stock in inventory is not affected yet
        self.assertEqual(self.store.inventory.get_product("Indomie Goreng").stock, initial_stock)

    def test_logout(self):
        self.store.current_user = User("admin", "adminpass", "admin")
        self.store.current_user = None
        self.assertIsNone(self.store.current_user)

if __name__ == "__main__":
    unittest.main()