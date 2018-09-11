from import_export import resources
from .models import *


class CollectionResource(resources.ModelResource):
    class Meta:
        model = Collection