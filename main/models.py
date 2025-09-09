import uuid
from django.db import models

SIZE_CHOICES = [(str(n), str(n)) for n in range(35, 50)]

class Shoes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        return sum(s.stock for s in self.sizes.all())

    @property
    def is_available(self):
        return self.total_stock > 0

    def decrease_stock(self, size, amount=1):
        size_row = self.sizes.get(size=size)
        if amount < 0:
            raise ValueError("tidak dapa negatif")
        if size_row.stock < amount:
            raise ValueError("stock tidak cukup")
        size_row.stock -= amount
        size_row.save()


class ShoeSize(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('shoes', 'size')