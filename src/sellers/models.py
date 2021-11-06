from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from sellers.managers import ContactManager, SellerManager


class Seller(models.Model):
    seller = models.OneToOneField('users.User', related_name='Seller', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Name', max_length=190, db_index=True)
    descr = models.TextField('Description', blank=True, null=True)
    logo = models.FileField('Logo', upload_to='seller_logo/', help_text='Logo', blank=True, null=True)
    wallet_for_payments_erc20 = models.CharField('ERC-20 wallet', blank=True, null=True, max_length=42)
    rating = models.FloatField('Rating', null=False, default=0,
                               validators=[MinValueValidator(0), MaxValueValidator(5.0)])

    objects = SellerManager()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'sellers'
        verbose_name_plural = 'Sellers'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def contacts(self):
        return Contact.objects.get_all_by_seller(seller=self)


class Contact(models.Model):
    TYPE_ID_URL = 1
    TYPE_ID_PHONE = 2
    TYPE_ID_EMAIL = 3
    TYPES = [
        (TYPE_ID_URL, 'URL'),
        (TYPE_ID_PHONE, 'Phone'),
        (TYPE_ID_EMAIL, 'Email'),
    ]

    id = models.AutoField('ID', primary_key=True)
    seller = models.ForeignKey('Seller', related_name='Contact', on_delete=models.CASCADE)
    type_id = models.IntegerField('Contact type', choices=TYPES)
    value = models.CharField('Value', max_length=190)
    comment = models.CharField('Comment', max_length=190, blank=True, default='')

    objects = ContactManager()

    class Meta:
        db_table = 'seller_contacts'
        verbose_name_plural = 'Seller contacts'
        ordering = ('type_id',)

    def __str__(self):
        return self.value
