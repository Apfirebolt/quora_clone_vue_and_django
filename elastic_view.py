from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Check connection
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

# View all data from an index
def view_all_data(index_name):
    """
    Retrieve all documents from an Elasticsearch index
    
    Args:
        index_name: Name of the index
    """
    response = es.search(index=index_name, body={"query": {"match_all": {}}, "size": 10000})
    return response['hits']['hits']


def apply_fuzzy_search(index_name, field, query):
    """
    Apply fuzzy search on a specific field in an Elasticsearch index
    
    Args:
        index_name: Name of the index
        field: Field to apply fuzzy search on
        query: Search query string
    """
    response = es.search(
        index=index_name,
        body={
            "query": {
                "fuzzy": {
                    field: {
                        "value": query,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
    )
    return response['hits']['hits']

# Example usage
if __name__ == "__main__":
    # View all data from 'titanic' index
    results = view_all_data('titanic')
    
    print(f"Total documents found: {len(results)}")
    for hit in results:
        print(f"\nDocument ID: {hit['_id']}")
        print(f"Data: {hit['_source']}")

    # Apply fuzzy search on 'name' field in 'titanic' index
    # fuzzy_results = apply_fuzzy_search('titanic', 'Name', 'Braund, Mr. Owen Harris')
    # print(f"\nFuzzy search results for 'Jon Doe': {len(fuzzy_results)} documents found")