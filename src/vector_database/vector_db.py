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
        self.vdb_app.loading_vdb(index_name = self.index_name)
        print(f"Document::::{docs}")
        response = self.vdb_app.adding_documents(new_info = docs)
        return response


# if __name__ == '__main__':
#     deploy_vectordatabase(index_name = 'support-chatbot')