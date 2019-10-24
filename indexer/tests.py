import os
import json

from django.test import TestCase
from django.urls import reverse
from elasticsearch_dsl import connections, Search, Index, utils
from rac_es.documents import Agent, BaseDescriptionComponent, Collection, Object, Term
from rest_framework.test import APIClient

from .helpers import generate_identifier
from .indexers import Indexer, TYPES
from .mergers import BaseMerger
from .models import DataObject
from .views import IndexAddView, IndexDeleteView, MergeView, MERGERS
from scorpio import settings


class TestMergerToIndex(TestCase):
    fixtures = ['initial_state.json']

    def setUp(self):
        self.client = APIClient()
        connections.create_connection(hosts=settings.ELASTICSEARCH['default']['hosts'], timeout=60)
        try:
            BaseDescriptionComponent._index.delete()
        except Exception as e:
            print(e)
        BaseDescriptionComponent.init()
        self.object_len = len(DataObject.objects.all())

    def merge_objects(self):
        # TODO: better set of objects to be merged
        for dir in os.listdir(os.path.join(settings.BASE_DIR, 'fixtures')):
            if os.path.isdir(os.path.join(settings.BASE_DIR, 'fixtures', dir)):
                for f in os.listdir(os.path.join(settings.BASE_DIR, 'fixtures', dir)):
                    with open(os.path.join(settings.BASE_DIR, 'fixtures', dir, f), 'r') as jf:
                        instance = json.load(jf)
                        request = self.client.post(reverse("merge"), instance, format='json')
                        self.assertEqual(request.status_code, 200)
        self.assertEqual(self.object_len, len(DataObject.objects.all()))
        # check field values
        # check valid against jsonschema - or should this be baked into merger?

    def index_objects(self):
        request = self.client.post(reverse("index-add"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(self.object_len, request.data['count'])
        self.assertEqual(self.object_len, BaseDescriptionComponent.search().count())

    def delete_objects(self):
        for obj in DataObject.objects.all():
            for id_obj in obj.data['external_identifiers']:
                request = self.client.post(reverse("index-delete"), {"source": id_obj['source'], "identifier": id_obj['identifier']})
                self.assertEqual(request.status_code, 200)
        self.assertEqual(0, BaseDescriptionComponent.search().count())

    def test_process(self):
        self.merge_objects()
        self.index_objects()
        self.delete_objects()
