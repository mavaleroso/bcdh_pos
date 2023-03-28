from django.db import models


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
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
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
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'company'

class Generic(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'generic'

class SubGeneric(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'sub_generic'

class Brand(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'brand'

class Unit(models.Model):
    item_unit = models.CharField(max_length=128, blank=True, null=True)
    sub_item_unit = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'unit'

# class Users(models.Model):
#     first_name = models.CharField(max_length=128, blank=True, null=True)
#     middle_name = models.CharField(max_length=128, blank=True, null=True)
#     last_name = models.CharField(max_length=128, blank=True, null=True)
#     birthdate = models.DateField(blank=True, null=True)
#     sex = models.CharField(max_length=128, blank=True, null=True)
#     address = models.CharField(max_length=128, blank=True, null=True)
#     email = models.CharField(max_length=128, blank=True, null=True)
#     position = models.CharField(max_length=128, blank=True, null=True)
#     username = models.CharField(max_length=128, blank=True, null=True)
#     password = models.CharField(max_length=128, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'user'



# class item(models.Model):
#     type_id = models.CharField(max_length=128, blank=True, null=True)
#     generic_id = models.ForeignKey(Generic, models.DO_NOTHING)
#     sub_generic_id = models.ForeignKey(SubGeneric, models.DO_NOTHING)
#     description = models.CharField(max_length=300, blank=True, null=True)
#     brand_id = models.ForeignKey(Brand, models.DO_NOTHING)
#     company_id = models.ForeignKey(Company, models.DO_NOTHING)
#     unit_id = models.ForeignKey(Unit, models.DO_NOTHING)
#     quantity = models.IntegerField()
#     unit_price = models.IntegerField()
#     retail_price = models.IntegerField()
#     is_damaged = models.CharField(max_length=128, blank=True, null=True)
#     user_id = models.ForeignKey(Users, models.DO_NOTHING)
#     delivered_date = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'item'
