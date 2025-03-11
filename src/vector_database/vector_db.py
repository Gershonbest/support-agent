import os
from dotenv import load_dotenv
import sys

load_dotenv()

from src.vector_database.utils import PineconeManagment


class VectorDatabase:
    def __init__(self, index_name):
        self.vdb_app = PineconeManagment()
        self.index_name = index_name

    def deploy_vectordatabase(self):
        docs = self.vdb_app.reading_datasource()
        self.vdb_app.creating_index(index_name = self.index_name, docs = docs)

    def ingest_index(self):
        docs = self.vdb_app.reading_datasource()
        self.vdb_app.add_doc_to_vdb(index_name=self.index_name, docs= docs)
