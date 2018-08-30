# Financial Dashboard 1
Bootcamp final project. Python/Django version of a financial dashboard I once made for a customer using MS Excel. It attempts to imitate a possible website service/application with similar features, but used by many companies and their various managers and employees. The initial version was prepared in ~7 days.


# General Information
This solution is a so-called 'executive dashboard', intended to provide a company's management staff with key information related to its performance in finance and sales areas.

Its general goal is to allow collection of data in form of various revenues and expenses (understood as documents or simply operations) and process them to provide information on, for example: general financial situation (income statement, cash flow), delayed payments, project profitability, salespeople performance etc.

The application allows use of two types of accounts: employee (responsible for data input) and manager (having access to reports and other executive features). It has working permissions, which (hopefully correctly) forbid users from accessing other companies' data or using executive features without authorisation. Key general views are working, but currently provide limited information (to be expanded). It is possible to add and modify documents and their data is used for calculations. More specific features are listed below.

The original project was prepared for a law firm using simplified accounting methods and customised for its purposes. Therefore, some features were designed with that customer's needs in mind, rather than formal tax accounting. Some financial matters are simplified, as this tool is not supposed to be used to calculate accounting data in accordance with International Accounting Standards or any other formal standards or regulations. It follows some general principles and potentially could be adjusted for other purposes.

Warning:
This is more a proof-of-concept or prototype rather than an actual, working tool to be used in business environment. It is still missing several key features and there are some simplifications in place. The latter include:
* Simplified accounting in general
* Taxes calculated on monthly basis
* (As of yet) no general settings for key global values (e.g. tax rates)
* Lack of data backups

# Key Features
Current features:
* Company registration and creation of respective groups and manger account
* Employee and Manager accounts
* Permissions, access restriction and company-groups
* Models for documents, companies, customers and various others
* Initial dashboard views
* Revenue and cost views, including modals with details, document-adding and modifications
* Simplified income statement view with chart and data-table
* Initial data-tables and charts, using filtered and calculated data
* Initial visual style using Bootstrap, including modals, navbar etc.
* Functions for calculating and filtering documents by date

Features to be possibly implemented in the future:
* Proper documentation
* Proper tests
* Proper widgets for form fields
* Corrected selection options for form fields
* Completed and expanded dashboards
* Temporary password generation for created employees
* Global company settings
* Reports on projects, procedures, salespeople
* Projections for future months
* Data filters
* Search for documents
* User modification, removal and password reset
* Possibly a mixin for simplifying view dispatches
* External data import/export
* Processing reports into pdf fields to be exported


# Main Requirements / Technology Used
* Python 3.7.0
* Django 2.1
* Bootstrap 3.3.7 (& django-bootstrap 10.0.1)
* PostgreSQL
* JavaScript / jQuery
* Highcharts 6.1.1 demo

Bootstrap & Highcharts are used locally in dashapp/static/lib

# Author
Bartosz Wójcik
bartosz.wojcik@bartvessh.com
