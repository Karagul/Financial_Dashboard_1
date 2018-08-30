from django.contrib.auth.models import User
from django.db import models

# ToDo: After tests, consider where null=True are needed


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
    actual_payment_date = models.DateField(null=True, blank=True)
    settlement_status = models.BooleanField(default=False)
    payment_expectation = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, default=1
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

    # Null in company is allowed to permit saving via CreateForm, and then
    # adding the relation within view's form_valid
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True)

    @property
    def net_amount_converted(self):
        return round(self.net_amount_foreign * self.exchange_rate, 2)

    @property
    def gross_amount_converted(self):
        return round(self.net_amount_converted * (1 + (self.vat_rate / 100)), 2)

    @property
    def percent_payment_expectation(self):
        return str(round(self.payment_expectation * 100, 0)) + "%"

    @property
    def display_vat_rate(self):
        return str(self.vat_rate) + "%"


class Expense(models.Model):
    name = models.CharField(max_length=120)
    # Here category to choose from another model?
    type_description = models.CharField(max_length=120)
    procedure = models.ForeignKey("Procedure", on_delete=models.PROTECT)
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    document_id = models.CharField(max_length=80)
    document_date = models.DateField(null=True)
    payment_deadline = models.DateField(null=True)
    actual_payment_date = models.DateField(null=True, blank=True)
    country = models.ForeignKey("Country", on_delete=models.PROTECT, default=1)
    net_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=23)
    settlement_status = models.BooleanField()

    # Null in company is allowed to permit saving via CreateForm, and then
    # adding the relation within view's form_valid
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True)

    @property
    def gross_amount(self):
        return round(self.net_amount * (1 + (self.vat_rate / 100)), 2)

    @property
    def display_vat_rate(self):
        return str(self.vat_rate) + "%"


class Employee(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    type = models.CharField(max_length=80)
    # Potentially position, if needed in the future

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
    project_start = models.DateField(null=True)     # ToDo: Remove null?

    owner = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.signature


# Currencies are not bound to countries as payments are done in various curren.
class Currency(models.Model):
    abbreviation = models.CharField(max_length=5)

    # company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.abbreviation

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=80)

    # company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
