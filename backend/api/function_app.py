import azure.functions as func
import logging
import json
import os
from azure.data.tables import TableServiceClient


app = func.FunctionApp()

@app.route(route="VisitorCounter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Connect to Azure Table Storage/CosmosDB Table API
        connection_string = os.getenv("AzureResumeConnectionString")
        table_service_client = TableServiceClient.from_connection_string(connection_string)
        table_client = table_service_client.get_table_client(table_name="VisitorCount")

        # Get the current count
        try:
            entity = table_client.get_entity(partition_key="global", row_key="count")
            current_count = int(entity["Count"])  # Ensure it's an integer
        except:
         logging.warning("Entity not found, initializing count to 0.")
        current_count = 0
        entity = {"PartitionKey": "global", "RowKey": "count", "Count": current_count}
        table_client.upsert_entity(entity)

        # Increment the count
        new_count = current_count + 1

        # Update the entity
        entity["Count"] = new_count
        table_client.update_entity(entity, mode="Replace")

        # Return the updated count as JSON
        return func.HttpResponse(
            json.dumps({"count": new_count}),
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "An error occurred while updating the visitor count."}),
            status_code=500,
            mimetype="application/json"
        )