from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import CustomUser  # Import your CustomUser model

@registry.register_document
class CustomUserDocument(Document):
    # Define fields you want to index for search
    email = fields.TextField(
        attr='email',
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    username = fields.TextField(
        attr='username',
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    firstName = fields.TextField(attr='firstName')
    lastName = fields.TextField(attr='lastName')

    is_staff = fields.BooleanField()
    is_superuser = fields.BooleanField()

    class Index:
        name = 'custom_users'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = CustomUser
        fields = [
            'id', 
        ]