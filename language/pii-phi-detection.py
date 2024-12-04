import oci
from oci.ai_language import AIServiceLanguageClient
from oci.ai_language.models import (
    TextDocument,
    BatchDetectHealthEntityDetails,
)

# Load OCI configuration
config = oci.config.from_file()

# Initialize AI Language Client
ai_client = AIServiceLanguageClient(config)

# Compartment and project details
compartment_id = "<COMAPRTMENT_ID>"
project_id = "<PROJECT_ID>"

# Health Entity Detection Endpoint
endpoint_id = "<ENDPOINT_ID>"

# Initialize Object Storage Client
object_storage_client = oci.object_storage.ObjectStorageClient(config)

# Object Storage details
namespace = "your_namespace"  # Replace with your namespace
bucket_name = "your_bucket_name"  # Replace with your bucket name
object_name = "your_file_name.txt"  # Replace with your object file name

try:
    # Get Object from Object Storage
    object_data = object_storage_client.get_object(namespace, bucket_name, object_name)
    file_content = object_data.data.text  # Read the text content of the file
    print("File content retrieved from Object Storage:")
    print(file_content)
    
    # Prepare input documents for Health Entity Detection
    documents = [TextDocument(key="doc1", text=file_content, language_code="en")]

    # Link ontologies for health entity detection
    link_ontologies = ["RXNORM", "SNOMEDCT", "ICD10CM"]

    # Health Entity Detection Request
    batch_detect_health_entity_details = BatchDetectHealthEntityDetails(
        endpoint_id=endpoint_id,
        documents=documents,
        link_ontologies=link_ontologies,
        is_detect_assertions=True,
        is_detect_relationships=True
    )

    # Perform Health Entity Detection
    health_response = ai_client.batch_detect_health_entity(batch_detect_health_entity_details)
    print("Health Entity Detection Output:")
    print(health_response.data)

except Exception as e:
    print(f"Error: {e}")
