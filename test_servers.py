# 1: Bugajski (414889), Adamek (414896), Basiura (414817)
import unittest
from collections import Counter
 
from servers import ListServer, Product, Client, MapServer
 
server_types = (ListServer, MapServer)
 
 
class ServerTest(unittest.TestCase):
 
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))
 
 
class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
 
class TestProduct(unittest.TestCase):

    def test_valid_product_name(self):
        # Sprawdzanie poprawności nazwy produktu
        product = Product("b1", 25.0)
        self.assertTrue(product.is_name_correct)

    def test_invalid_product_name(self):
        # Sprawdzanie niepoprawnej nazwy produktu
        with self.assertRaises(ValueError):
            Product("123", 25.0)

 
if __name__ == '__main__':
    unittest.main()
# 1: Bugajski (414889), Adamek (414896), Basiura (414817)