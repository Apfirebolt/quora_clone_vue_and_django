from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Check connection
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

# Insert new data
def insert_data(index_name, doc_id, document):
    """
    Insert a document into Elasticsearch
    
    Args:
        index_name: Name of the index
        doc_id: Document ID
        document: Dictionary containing the document data
    """
    response = es.index(index=index_name, id=doc_id, document=document)
    return response

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_document = {
        'title': 'Sample Question',
        'content': 'This is a sample question content',
        'author': 'user123',
        'created_at': '2024-01-01T00:00:00'
    }
    
    # Insert data
    result = insert_data('questions', 1, sample_document)
    print(f"Document inserted: {result['result']}")