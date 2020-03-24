from asterism.views import BaseServiceView

from .indexers import Indexer


class IndexView(BaseServiceView):
    """Add data to or delete data from an index"""

    def get_service_response(self, request):
        clean = True if request.GET.get('clean') else False
        identifier = request.data.get('identifier')
        object_type = request.GET.get('object_type')
        return getattr(Indexer(), self.method)(clean=clean, object_type=object_type, identifier=identifier)


class IndexAddView(IndexView):
    """Adds a data object to index."""
    method = 'add'


class IndexDeleteView(IndexView):
    """Deletes a data object from index."""
    method = 'delete'
