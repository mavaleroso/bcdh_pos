from django.db import models

from main.models import ( ItemType, Generic, SubGeneric, Brand, AuthUser)

# Create your models here.
class Items(models.Model):
    barcode = models.CharField(max_length=128, blank=True, null=True)
    type = models.ForeignKey(ItemType, models.DO_NOTHING)
    generic = models.ForeignKey(Generic, models.DO_NOTHING)
    sub_generic = models.ForeignKey(SubGeneric, models.DO_NOTHING)
    description = models.CharField(max_length=300, blank=True, null=True)
    classification = models.CharField(max_length=128, blank=True, null=True)
    brand = models.ForeignKey(Brand, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'items'