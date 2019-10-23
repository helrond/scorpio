from asterism.views import prepare_response
from rest_framework.views import APIView

from .indexers import Indexer
from .mergers import AgentMerger, CollectionMerger, ObjectMerger, TermMerger

MERGERS = {
    "agent": AgentMerger,
    "collection": CollectionMerger,
    "object": ObjectMerger,
    "term": TermMerger
}


class IndexView(APIView):
    """Add data to or delete data from an index"""
    def post(self, request, format=None):
        clean = True if request.GET.get('clean') else False
        try:
            resp = getattr(Indexer, self.method)(clean)
            return Response(prepare_response(resp, data.id), status=200)
        except Exception as e:
            return Response(prepare_response(resp, data.id), status=500)


class IndexAddView(IndexView):
    """Adds a data object to index."""
    method = 'add'


class IndexDeleteView(IndexView):
    """Deletes a data object from index."""
    method = 'delete'


class MergeView(APIView):
    """Merges transformed data objects."""
    def post(self, request, format=None):
        data = request.data.get('data')
        try:
            merger = MERGERS[data.type]
            resp = merger.merge(data)
            return Response(prepare_response(resp, data.id), status=200)
        except Exception as e:
            return Response(prepare_response(resp, data.id), status=500)
