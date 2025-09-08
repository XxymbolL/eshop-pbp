from django.test import TestCase, Client
from .models import Store

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
        store = Store.objects.create(
            name="ABIBAS YEETZY",
            price=30000000,
            description="sepatu sigma untuk semua",
        )
        store.sizes.create(size="42", stock=500)

        self.assertTrue(store.is_available)
        self.assertEqual(store.total_stock, 500)

        store.decrease_stock("42")
        self.assertEqual(store.total_stock, 499)

    def test_store_default_values(self):
        store = Store.objects.create(
            name="Test shoes",
            description="Test desc"
        )
        self.assertEqual(store.price, 0)
        self.assertEqual(store.total_stock, 0)
        self.assertFalse(store.is_available)

    def test_stock_threshold(self):
        store = Store.objects.create(
            name="last pair",
            description="Test desc",
        )
        store.sizes.create(size="42", stock=1)

        self.assertTrue(store.is_available)

        store.decrease_stock("42")
        self.assertEqual(store.total_stock, 0)
        self.assertFalse(store.is_available)
