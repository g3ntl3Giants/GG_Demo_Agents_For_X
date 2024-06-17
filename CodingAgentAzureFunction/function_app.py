import azure.functions as func
import datetime
import json
import logging
from pydantic import BaseModel
import chatbot

app = func.FunctionApp()

def http_error(status_code, detail):
    return func.HttpResponse(
        json.dumps({"detail": detail}),
        status_code=status_code,
        mimetype="application/json"
    )

@app.route(route="CodingAgentAzureFunction", auth_level=func.AuthLevel.FUNCTION)
def CodingAgentAzureFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
class ChatRequest(BaseModel):
    user_input: str
    
@app.route(route="CodingAgentFunction/chat", methods="POST", auth_level=func.AuthLevel.FUNCTION)
def chat_with_bot(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request = ChatRequest(**req.get_json())
        response = chatbot.chat_with_user(request.user_input)
        if "error" in response:
            return http_error(500, response["error"])
        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json"
        )
    except Exception as e:
        return http_error(500, str(e))