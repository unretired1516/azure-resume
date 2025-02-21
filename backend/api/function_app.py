import azure.functions as func
import logging
import json
import os
from azure.data.tables import TableServiceClient

app = func.FunctionApp()

@app.route(route="VisitorCounter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Ensure that the method is GET
    if req.method != "GET":
        return func.HttpResponse(
            json.dumps({"error": "Only GET requests are supported."}),
            status_code=405,
            mimetype="application/json"
        )

    try:
        # Retrieve connection string from environment variables
        connection_string = os.getenv("AzureResumeConnectionString")
        if not connection_string:
            raise ValueError("AzureResumeConnectionString is not set.")

        # Connect to Cosmos DB Table API
        table_service_client = TableServiceClient.from_connection_string(connection_string)
        table_client = table_service_client.get_table_client(table_name="VisitorCount")

        # Get the current count
        try:
            entity = table_client.get_entity(partition_key="global", row_key="count")
            logging.info(f"Entity retrieved: {entity}")  # Log full entity
            current_count = int(entity.get("Count", 0))  # Ensure key exists
            logging.info(f"Current visitor count: {current_count}")
        except Exception as e:
            logging.warning(f"Entity not found or error retrieving count: {e}")
            current_count = 0
            entity = {"PartitionKey": "global", "RowKey": "count", "Count": current_count}

        # Increment the count
        entity["Count"] = current_count + 1

        # Use upsert_entity to insert or update
        table_client.upsert_entity(entity)
        logging.info(f"Entity after upsert: {table_client.get_entity(partition_key='global', row_key='count')}")

        # ✅ Always return a valid response
        return func.HttpResponse(
            json.dumps({"count": entity["Count"]}),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        # ✅ Ensure we return a response even in failure cases
        return func.HttpResponse(
            json.dumps({"error": f"An error occurred: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )


        # Increment the count
        entity["Count"] = current_count + 1

        # Use upsert_entity to insert or update
        table_client.upsert_entity(entity)
        logging.info(f"Entity after upsert: {table_client.get_entity(partition_key='global', row_key='count')}")

        # ✅ Always return a valid response
        return func.HttpResponse(
            json.dumps({"count": entity["Count"]}),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        # ✅ Ensure we return a response even in failure cases
        return func.HttpResponse(
            json.dumps({"error": f"An error occurred: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )