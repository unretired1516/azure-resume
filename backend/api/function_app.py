import azure.functions as func
import logging
from azure.data.tables import TableServiceClient

app = func.FunctionApp()

@app.route(route="VisitorCounter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Connect to Azure Table Storage/CosmosDB Table API
        connection_string = "AzureResumeConnectionString"
        table_service_client = TableServiceClient.from_connection_string(connection_string)
        table_client = table_service_client.get_table_client(table_name="VisitorCount")

        # Get the current count
        entity = table_client.get_entity(partition_key="global", row_key="count")
        current_count = entity["Count"]

        # Increment the count
        new_count = current_count + 1
        
        # Update the entity
        entity["Count"] = new_count
        table_client.update_entity(entity)

        # Return the updated count as JSON
        return func.HttpResponse(
            f'{{"count": {new_count}}}',
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            '{"error": "An error occurred while updating the visitor count."}',
            status_code=500,
            mimetype="application/json"
        )