import factory
from django.conf import settings

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda n: "user{0}@example.com".format(n))
    password = factory.PostGenerationMethodCall("set_password", settings.TEST_USER_PASSWORD)
    is_staff = False
    is_superuser = False
    is_active = True
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")