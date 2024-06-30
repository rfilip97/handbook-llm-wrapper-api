from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from handbook_llm_wrapper.main import create_assistant, ask_question
import os
import pusher

pusher_client = pusher.Pusher(
    app_id=os.environ["PUSHER_APP_ID"],
    key=os.environ["PUSHER_KEY"],
    secret=os.environ["PUSHER_SECRET"],
    cluster="eu",
    ssl=True,
)

MODEL_PATH = os.path.expanduser("~/llms/ggml-model-Q8_0.gguf")
assistant = create_assistant(MODEL_PATH)


def ask(request):
    question = request.GET.get("question")
    if not question:
        return JsonResponse({"error": "No question provided"}, status=400)

    channel_name = f"private-{request.session.session_key}"

    def streaming_handler(token):
        print(f"##### {token}")

        pusher_client.trigger(channel_name, "new-token", {"token": token})

    assistant.set_streaming_handler_function(streaming_handler)

    print("waiting for answer...")
    answer = ask_question(assistant, question)
    return JsonResponse({"response": answer, "channel_name": channel_name})


@csrf_exempt
def pusher_auth(request):
    channel_name = request.POST.get("channel_name")
    socket_id = request.POST.get("socket_id")

    auth = pusher_client.authenticate(channel=channel_name, socket_id=socket_id)
    return JsonResponse(auth)
