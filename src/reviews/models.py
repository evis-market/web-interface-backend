import uuid

from django.core.exceptions import ValidationError
from django.db import models

from reviews.managers import CommentManager, ReviewManager
from seller_products.models import SellerProduct


def validate_rating(value):
    if value not in (0, 1, 2, 3, 4, 5):
        raise ValidationError('rating value = %(value)s is not an integer ranged from 0 to 5', params={'value': value})


class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[validate_rating])

    objects = ReviewManager()


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    message = models.TextField()

    objects = CommentManager()
