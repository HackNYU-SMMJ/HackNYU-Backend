# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_number = models.IntegerField(unique=True)
    account_balance = models.DecimalField(max_digits=18, decimal_places=2)
    account_type = models.CharField(max_length=45)
    updated_at = models.DateTimeField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account'


class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=255)
    symbol = models.CharField(unique=True, max_length=20)
    asset_type = models.CharField(max_length=45)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'asset'


class AssetPriceHistory(models.Model):
    price_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    date = models.DateTimeField(blank=True, null=True)
    asset = models.ForeignKey(Asset, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'asset_price_history'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)
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


class Investment(models.Model):
    investment_id = models.AutoField(primary_key=True)
    amount_invested = models.DecimalField(max_digits=6, decimal_places=2)
    investment_date = models.DateTimeField()
    status = models.IntegerField()
    account = models.ForeignKey(Account, models.DO_NOTHING)
    asset = models.ForeignKey(Asset, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'investment'


class InvestmentPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    investment_goal = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=18, decimal_places=2)
    threshold_amount = models.DecimalField(max_digits=18, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=45)
    withdrawn_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'investment_plan'


class InvestmentPlanAsset(models.Model):
    investment_plan = models.ForeignKey(InvestmentPlan, models.DO_NOTHING)
    asset = models.ForeignKey(Asset, models.DO_NOTHING)
    allocation = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'investment_plan_asset'


class Roundup(models.Model):
    roundup_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('Transactions', models.DO_NOTHING)
    investment = models.ForeignKey(Investment, models.DO_NOTHING)
    roundup_amount = models.DecimalField(max_digits=18, decimal_places=2)
    roundup_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'roundup'


class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=45)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    transaction_date = models.DateTimeField()
    status = models.CharField(max_length=45)
    account = models.ForeignKey(Account, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transactions'
