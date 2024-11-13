from tabulate import tabulate

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def verify_password(self, password):
        return self.password == password

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        return False

    def add_stock(self, quantity):
        self.stock += quantity

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.name] = product

    def show_products(self):
        print("\n--- Daftar Produk Toko Indomaret ---")
        table = [[product.name, product.stock, f"Rp{product.price}"] for product in self.products.values()]
        print(tabulate(table, headers=["Nama Produk", "Stok", "Harga"], tablefmt="fancy_grid"))

    def get_product(self, name):
        return self.products.get(name, None)

class Cart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, product, quantity):
        if product.name in self.items:
            self.items[product.name]["quantity"] += quantity
        else:
            self.items[product.name] = {"product": product, "quantity": quantity}
        print(f"{quantity} {product.name} telah ditambahkan ke keranjang.")

    def show_cart(self):
        print("\n--- Rincian Keranjang Belanja ---")
        table = []
        total = 0
        for item in self.items.values():
            product = item["product"]
            quantity = item["quantity"]
            subtotal = product.price * quantity
            table.append([product.name, quantity, f"Rp{subtotal}"])
            total += subtotal
        print(tabulate(table, headers=["Nama Produk", "Jumlah", "Subtotal"], tablefmt="fancy_grid"))
        print(f"\nTotal Belanja: Rp{total}")
        return total

    def clear_cart(self):
        self.items.clear()

class Cashier:
    def __init__(self, inventory):
        self.inventory = inventory

    def checkout(self, cart):
        total = cart.show_cart()
        uang = int(input("Masukkan jumlah uang yang dibayar: "))

        if uang >= total:
            kembalian = uang - total
            print(f"Pembayaran berhasil! Kembalian Anda: Rp{kembalian}")
            for item in cart.items.values():
                product = item["product"]
                quantity = item["quantity"]
                product.reduce_stock(quantity)
            cart.clear_cart()
        else:
            print("Uang tidak mencukupi. Transaksi dibatalkan.")

class Store:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.add_product(Product("Indomie Goreng", 3000, 20))
        self.inventory.add_product(Product("Beras 1kg", 12000, 15))
        self.inventory.add_product(Product("Minyak Goreng 1L", 15000, 10))
        self.inventory.add_product(Product("Gula 1kg", 10000, 8))
        self.inventory.add_product(Product("Telur Ayam (1 butir)", 1500, 30))

        self.cart = Cart()
        self.cashier = Cashier(self.inventory)
        self.users = [
            User("admin", "adminpass", "admin"),
            User("buyer", "buyerpass", "buyer")
        ]
        self.current_user = None

    def login(self):
        print("\n--- Login ---")
        username = input("Username: ")
        password = input("Password: ")

        for user in self.users:
            if user.username == username and user.verify_password(password):
                self.current_user = user
                print(f"Login berhasil sebagai {user.role}.\n")
                return True
        print("Username atau password salah.")
        return False

    def run(self):
        while True:
            if not self.current_user:
                print("\n--- Menu Utama ---")
                print("1. Login")
                print("2. Keluar")
                choice = input("Pilih opsi: ")

                if choice == "1":
                    if not self.login():
                        continue
                elif choice == "2":
                    print("Terima kasih telah menggunakan program ini!")
                    break
                else:
                    print("Opsi tidak valid. Silakan coba lagi.")
            else:
                self.show_menu()

    def show_menu(self):
        while self.current_user:
            print("\n--- Selamat Datang di Toko Indomaret ---")
            print("1. Lihat Daftar Produk")
            if self.current_user.role == "admin":
                print("2. Tambah Stok Produk")
            elif self.current_user.role == "buyer":
                print("2. Tambah ke Keranjang")
                print("3. Lihat Keranjang dan Total Belanja")
                print("4. Bayar")
            print("5. Log Out")

            pilihan = input("Pilih opsi: ")

            if pilihan == "1":
                self.inventory.show_products()
            elif pilihan == "2":
                if self.current_user.role == "admin":
                    self.add_stock()
                elif self.current_user.role == "buyer":
                    self.add_to_cart()
            elif pilihan == "3" and self.current_user.role == "buyer":
                self.cart.show_cart()
            elif pilihan == "4" and self.current_user.role == "buyer":
                self.cashier.checkout(self.cart)
            elif pilihan == "5":
                print("Anda telah keluar.")
                self.current_user = None  # Log out
            else:
                print("Opsi tidak valid. Silakan coba lagi.")

    def add_stock(self):
        product_name = input("Masukkan nama produk yang ingin ditambah stoknya: ")
        product = self.inventory.get_product(product_name)
        if product:
            try:
                quantity = int(input("Masukkan jumlah stok yang ingin ditambah: "))
                product.add_stock(quantity)
                print(f"Stok {product_name} berhasil ditambahkan sebanyak {quantity}.")
            except ValueError:
                print("Input tidak valid. Masukkan angka untuk jumlah stok.")
        else:
            print("Produk tidak ditemukan.")

    def add_to_cart(self):
        self.inventory.show_products()
        product_name = input("Masukkan nama produk yang ingin dibeli: ")
        product = self.inventory.get_product(product_name)
        if product:
            try:
                quantity = int(input("Masukkan jumlah yang ingin dibeli: "))
                if product.stock >= quantity:
                    self.cart.add_to_cart(product, quantity)
                else:
                    print("Maaf, stok tidak mencukupi.")
            except ValueError:
                print("Input tidak valid. Masukkan angka untuk jumlah.")
        else:
            print("Produk tidak ditemukan.")

# Menjalankan Program
if __name__ == "__main__":
    store = Store()
    store.run()