from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(
    ['http://localhost:9200'],
    # basic_auth=('username', 'password'),  # Uncomment if authentication is needed
)

# Test the connection
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

# Get cluster info
info = es.info()
print(f"Cluster name: {info['cluster_name']}")
print(f"Elasticsearch version: {info['version']['number']}")