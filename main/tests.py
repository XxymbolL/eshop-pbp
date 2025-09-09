from django.test import TestCase, Client
from .models import Shoes

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_shop_creation(self):
        shoes = Shoes.objects.create(
            name="ABIBAS YEETZY",
            price=30000000,
            description="sepatu sigma untuk semua",
        )
        shoes.sizes.create(size="42", stock=500)

        self.assertTrue(shoes.is_available)
        self.assertEqual(shoes.total_stock, 500)

        shoes.decrease_stock("42")
        self.assertEqual(shoes.total_stock, 499)

    def test_shoes_default_values(self):
        shoes = Shoes.objects.create(
            name="Test shoes",
            description="Test desc"
        )
        self.assertEqual(shoes.price, 0)
        self.assertEqual(shoes.total_stock, 0)
        self.assertFalse(shoes.is_available)

    def test_stock_threshold(self):
        shoes = Shoes.objects.create(
            name="last pair",
            description="Test desc",
        )
        shoes.sizes.create(size="42", stock=1)

        self.assertTrue(shoes.is_available)

        shoes.decrease_stock("42")
        self.assertEqual(shoes.total_stock, 0)
        self.assertFalse(shoes.is_available)
