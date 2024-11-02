from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from faker import Faker

from apps.models import User, Category, Product


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    faker = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int)
        parser.add_argument('-c', '--category', type=int)
        parser.add_argument('-p', '--products', type=int)

    def _users(self, n: int):
        users = [User(
            is_superuser=self.faker.boolean(),
            is_active=self.faker.boolean(),
            is_staff=self.faker.boolean(),
            date_joined=self.faker.date(),
            password=make_password(str(self.faker.random_int())),
            phone=f"{self.faker.msisdn()[4:]}"
        ) for _ in range(n)]

        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {n} users"))

    def _category(self, n: int):
        categories = [
            Category(
                name=self.faker.name(),
                slug= self.faker.slug(),
                photo=self.faker.file_name(extension='png')
            ) for _ in range(n)
        ]

        Category.objects.bulk_create(categories)
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {n} categories"))

    def _products(self, n: int):
        category = Category.objects.order_by('?').first()
        subcategories = [Product(
            name=self.faker.name(),
            slug= self.faker.slug(),
            price=self.faker.random_int(),
            photo=self.faker.file_name(extension='png'),
            category_id=category.id,
            quantity=self.faker.random_int(),
            description=self.faker.text(),
            product_fee=self.faker.random_digit(),
        ) for _ in range(n)]

        Product.objects.bulk_create(subcategories)
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {n} products"))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating database ...'))
        methods = {'users', 'category', 'products'}
        for method in methods:
            options[method] and getattr(self, f"_{method}")(options[method])
        self.stdout.write(self.style.SUCCESS(f"Successfully populated databases"))

# ************************************* Updated version **********************************

import random

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.db.models import ForeignKey, OneToOneField, ManyToManyField
from faker import Faker


# class Command(BaseCommand):
#     help = "Automatically populates custom app models with fake data using Faker"
#     faker = Faker()
#
#     def add_arguments(self, parser):
#         parser.add_argument('-n', '--number', type=int, default=10, help='Number of records to create for each model')
#
#     def handle(self, *args, **options):
#         self.stdout.write(self.style.SUCCESS('Populating database...'))
#         number_of_records = options['number']
#
#         for model in apps.get_models():
#             if self.is_custom_model(model):
#                 self.populate_model(model, number_of_records)
#
#         self.stdout.write(
#             self.style.SUCCESS(f"Successfully populated {number_of_records} records for all custom models"))
#
#     def is_custom_model(self, model):
#         default_apps = ['auth', 'admin', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'django']
#         return model._meta.app_label not in default_apps
#
#     def populate_model(self, model, number_of_records):
#         if not model._meta.managed:
#             return
#
#         objects = []
#         m2m_fields = []
#
#         for _ in range(number_of_records):
#             fake_data = {}
#             for field in model._meta.get_fields():
#                 if field.auto_created:
#                     continue
#
#                 if field.is_relation:
#                     if isinstance(field, (ForeignKey, OneToOneField)):
#                         related_instance = field.related_model.objects.order_by('?').first()
#                         fake_data[field.name] = related_instance
#                     elif isinstance(field, ManyToManyField):
#                         m2m_fields.append(field)
#                 else:
#                     fake_data[field.name] = self.get_fake_data_for_field(field)
#
#             obj = model(**fake_data)
#             objects.append(obj)
#
#         model.objects.bulk_create(objects)
#
#         # Step 2: Assign ManyToMany relationships after objects have been created
#         # if m2m_fields:
#         #     for obj in objects:
#         #         for field in m2m_fields:
#         #             related_model = field.related_model
#         #             # Assign random related instances for ManyToMany field
#         #             related_instances = related_model.objects.order_by('?')[:random.randint(1, 3)]
#         #             getattr(obj, field.name).set(related_instances)  # Use 'set' to assign the related objects
#
#         self.stdout.write(
#             self.style.SUCCESS(f"Successfully populated {number_of_records} records for {model.__name__}"))
#
#     def get_fake_data_for_field(self, field):
#         if field.get_internal_type() == 'CharField':
#             return f"{self.faker.word()}_{self.faker.word()}"
#         elif field.get_internal_type() == 'SlugField':
#             return self.faker.slug()
#         elif field.get_internal_type() == 'TextField':
#             return self.faker.text()
#         elif field.get_internal_type() == 'IntegerField':
#             return random.randint(1, 100)
#         elif field.get_internal_type() == 'BooleanField':
#             return self.faker.boolean()
#         elif field.get_internal_type() == 'DateField':
#             return self.faker.date()
#         elif field.get_internal_type() == 'DateTimeField':
#             return self.faker.date_time()
#         elif field.get_internal_type() == 'EmailField':
#             return self.faker.email()
#         elif field.get_internal_type() == 'URLField':
#             return self.faker.url()
#         elif field.get_internal_type() == 'FileField':
#             return self.faker.file_name(extension='png')
#         elif field.get_internal_type() == 'DecimalField':
#             return self.faker.pydecimal(left_digits=5, right_digits=2)
#         elif field.get_internal_type() == 'FloatField':
#             return self.faker.pyfloat(left_digits=5, right_digits=2)
#         elif field.get_internal_type() == 'PasswordField':
#             return make_password(self.faker.password())
#         elif field.get_internal_type() == 'PhoneNumberField':
#             return self.faker.phone_number()
#         elif field.get_internal_type() == 'TimeField':
#             return self.faker.time()
#         return None
