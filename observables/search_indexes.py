import datetime
from haystack import indexes
from . import models


class ObservableIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    created_date = indexes.DateTimeField(model_attr='created_date')

    def get_model(self):
        return models.Observable

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_date__lte=datetime.datetime.now())
