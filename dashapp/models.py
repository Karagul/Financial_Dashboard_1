from django.db import models

# Zastanowić się gdzie dać null true

# W niektórych modelach może trzeba będzie dodać firmę, do której należy element - by później ograniczyć wyświetlanie i modyfikację

class Revenue(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)
    employee = models.ForeignKey("Employee", on_delete=models.PROTECT, null=True)
    payment_type = models.ForeignKey("PaymentType", on_delete=models.PROTECT)
    procedure = models.ForeignKey("Procedure", on_delete=models.PROTECT)
    document_date = models.DateField(null=True)
    payment_deadline = models.DateField(null=True)
    document_id = models.CharField(max_length=80)
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    expected_payment_date = models.DateField(null=True)
    settlement_status = models.BooleanField(default=False)
    payment_expectation = models.DecimalField(max_digits=3, decimal_places=2, null=True)   # Ewentualnie przerobić na small integer?
    net_amount_foreign = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.ForeignKey("Currency", on_delete=models.PROTECT, default=1)
    country = models.ForeignKey("Country", on_delete=models.PROTECT, default=1)
    exchange_rate = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=23)

class Cost(models.Model):
    name = models.CharField(max_length=120)
    # Category to choose from another table
    type_description = models.CharField(max_length=120)
    procedure = models.ForeignKey("Procedure", on_delete=models.PROTECT)
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    document_id = models.CharField(max_length=80)
    document_date = models.DateField(null=True)
    payment_deadline = models.DateField(null=True)
    expected_payment_date = models.DateField(null=True)
    country = models.ForeignKey("Country", on_delete=models.PROTECT, default=1)
    net_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=23)
    settlement_status = models.BooleanField()

class Employee(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    type = models.CharField(max_length=80)     # Sales or administration
    #position

class Customer(models.Model):
    name = models.CharField(max_length=120)

class Procedure(models.Model):
    name = models.CharField(max_length=80)

class Country(models.Model):
    name = models.CharField(max_length=80)
    default_vat_rate = models.DecimalField(max_digits=4, decimal_places=2)

class PaymentType(models.Model):
    name = models.CharField(max_length=80)

class Project(models.Model):
    signature = models.CharField(max_length=80)
    project_start = models.DateField(null=True)     # Wywalić null true po testach?

class Currency(models.Model):
    abbreviation = models.CharField(max_length=5)

class CostCategory(models.Model):
    name = models.CharField(max_length=80)
