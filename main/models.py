from django.db import models
from datetime import datetime  


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Company(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    code = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'company'

class Generic(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'generic'

class SubGeneric(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'sub_generic'

class Brand(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'brand'

class Unit(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'unit'

class UserDetails(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'user_details'


class ItemType(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'item_type'


class Item(models.Model):
    type = models.ForeignKey(ItemType, models.DO_NOTHING)
    generic = models.ForeignKey(Generic, models.DO_NOTHING)
    sub_generic = models.ForeignKey(SubGeneric, models.DO_NOTHING)
    description = models.CharField(max_length=300, blank=True, null=True)
    brand = models.ForeignKey(Brand, models.DO_NOTHING)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    unit_quantity = models.IntegerField(max_length=128, blank=True, null=True)
    quantity = models.IntegerField(max_length=128, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    retail_price = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    retail_price_unit = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    is_damaged = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    delivered_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'item'

class EditRequests(models.Model):
    item = models.ForeignKey(Item, models.DO_NOTHING)
    status = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'edit_requests'

class ClientType(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'client_type'

class Clients(models.Model):
    client_type = models.ForeignKey(ClientType, models.DO_NOTHING)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.DateField(blank=True, null=True)
    birthdate = models.CharField(max_length=128, blank=True, null=True)
    sex = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    occupation = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'clients'

class ItemDetails(models.Model):
    item = models.ForeignKey(Item, models.DO_NOTHING)
    barcode = models.CharField(max_length=128, blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'item_details'

class Location(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'location'

class ItemLocation(models.Model):
    item = models.ForeignKey(Item, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    quantity = models.IntegerField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'item_location'

class Discounts(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    percentage = models.FloatField(null=True, blank=True, default=0)
    is_fixed_amount = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'discounts'

class Sales(models.Model):
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    transaction_code = models.CharField(max_length=128, blank=True, null=True)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING)
    is_er = models.BooleanField(default=False)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    status = models.CharField(max_length=128, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'sales'

class Payment(models.Model):
    sales = models.ForeignKey(Sales, models.DO_NOTHING)
    amount_paid = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'payment'

class InpatientSales(models.Model):
    transaction_code = models.CharField(max_length=128, blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    status = models.CharField(max_length=128, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'inpatient_sales'

class OutItems(models.Model):
    sales = models.ForeignKey(Sales, models.DO_NOTHING)
    inpatient_sales = models.ForeignKey(InpatientSales, models.DO_NOTHING)
    item = models.ForeignKey(Item, models.DO_NOTHING)
    quantity = models.IntegerField(max_length=128, blank=True, null=True)
    discounted_amount = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'out_items'
