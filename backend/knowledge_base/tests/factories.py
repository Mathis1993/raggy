import factory

from knowledge_base.models import Document


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    user_id = factory.Faker("pyint")
    content = factory.Faker("text")