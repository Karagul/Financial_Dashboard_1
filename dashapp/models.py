from django.contrib.auth.models import User
from django.db import models

# ToDo: Zastanowić się gdzie dać null true

# ToDo: W niektórych modelach może trzeba będzie dodać firmę, do której należy element - by później ograniczyć wyświetlanie i modyfikację

# Teoretycznie można rozdzielić zdarzenie od dokumentu, tworząc dwa modele z powiązaniem 1-do-1. Ale czy to ma sens?

class CompanyMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.company.id


class Company(models.Model):
    name = models.CharField(max_length=120, verbose_name="Company name")
    # ToDo: If possible, read NIP data automatically
    tax_no = models.CharField(
        unique=True, max_length=20, verbose_name="Tax no."
    )
    street = models.CharField(
        max_length=120, verbose_name="Street", null=True
    )
    building_no = models.CharField(
        max_length=120, verbose_name="Building no.", null=True
    )
    flat_no = models.CharField(
        max_length=120, verbose_name="Flat no.", null=True
    )
    postal_code = models.CharField(
        max_length=120, verbose_name="Postal code", null=True
    )
    city = models.CharField(
        max_length=120, verbose_name="City", null=True
    )
    # ToDo: Tutaj potrzebny będzie walidator NIP

    class Meta:
        permissions = (
            ("manager_access", "Access to manager features"),
        )


class Revenue(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)
    employee = models.ForeignKey(
        "Employee", on_delete=models.PROTECT, null=True
    )
    payment_type = models.ForeignKey("PaymentType", on_delete=models.PROTECT)
    procedure = models.ForeignKey("Procedure", on_delete=models.PROTECT)
    document_date = models.DateField(null=True)
    payment_deadline = models.DateField(null=True)
    document_id = models.CharField(max_length=80)
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    expected_payment_date = models.DateField(null=True)
    settlement_status = models.BooleanField(default=False)
    payment_expectation = models.DecimalField(
        max_digits=3, decimal_places=2, null=True
    )   # Ewentualnie przerobić na small integer?
    net_amount_foreign = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.ForeignKey(
        "Currency", on_delete=models.PROTECT, default=1
    )
    country = models.ForeignKey(
        "Country", on_delete=models.PROTECT, default=1
    )
    exchange_rate = models.DecimalField(
        max_digits=7, decimal_places=4, default=1
    )
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=23)

    company = models.ForeignKey("Company", on_delete=models.CASCADE)

    @property
    def net_amount_converted(self):
        return self.net_amount_foreign * self.exchange_rate

    @property
    def gross_amount_converted(self):
        return self.net_amount_converted * self.vat_rate


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

    company = models.ForeignKey("Company", on_delete=models.CASCADE)

    @property
    def gross_amount_converted(self):
        return self.net_amount * self.vat_rate


class Employee(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    type = models.CharField(max_length=80)     # Sales or administration
    #position

    company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    name = models.CharField(max_length=120)

    owner = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Procedure(models.Model):
    name = models.CharField(max_length=80)

    owner = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=80)
    default_vat_rate = models.DecimalField(max_digits=4, decimal_places=2)

    # company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=80)

    owner = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Project(models.Model):
    signature = models.CharField(max_length=80)
    project_start = models.DateField(null=True)     # ToDo: Wywalić null true po testach?

    owner = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.signature


class Currency(models.Model):
    abbreviation = models.CharField(max_length=5)

    # company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.abbreviation

class CostCategory(models.Model):
    name = models.CharField(max_length=80)

    # company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
