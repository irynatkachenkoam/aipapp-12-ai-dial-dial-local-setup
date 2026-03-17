import uvicorn

from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response
from starlette.responses import JSONResponse


# ChatCompletion is an abstract class for applications and model adapters
class EchoApplication(ChatCompletion):
    async def chat_completion(
        self, request: Request, response: Response
    ) -> None:
        # Get last message (the newest) from the history
        last_user_message = request.messages[-1]

        # Generate response with a single choice
        with response.create_single_choice() as choice:
            # Fill the content of the response with the last user's content
            choice.append_content(f"abracadabra\n{last_user_message.content}" or "Oops...")


# DIAL App extends FastAPI to provide an user-friendly interface for routing requests to your applications
app = DIALApp()
app.add_chat_completion("echo", EchoApplication())

@app.get("/health")
async def health():
    return JSONResponse({"status": "healthy"}, status_code=200)

# Run builded app
if __name__ == "__main__":
    uvicorn.run(app, port=5022, host="0.0.0.0")