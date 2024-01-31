import factory

from knowledge_base.models import Document


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document
        django_get_or_create = ("identifier",)

    user_id = factory.Faker("pyint")
    identifier = factory.Sequence(lambda n: f"identifier_{n}")
    type = Document.Type.WEBSITE
    title = factory.Faker("sentence")
    content = factory.Faker("text")