from django.http import JsonResponse
from handbook_llm_wrapper.main import create_assistant, ask_question
import os

def streaming_handler_function(token):
    print(f"--received token: ({token})----")

MODEL_PATH = os.path.expanduser('~/llms/ggml-model-Q4_1.gguf')
assistant = create_assistant(MODEL_PATH)
assistant.set_streaming_handler_function(streaming_handler_function)

def ask(request):
    question = request.GET.get('question')
    if not question:
        return JsonResponse({'error': 'No question provided'}, status=400)

    answer = ask_question(assistant, question)
    return JsonResponse({'response': answer})

