from django.http import JsonResponse
from handbook_llm_wrapper.main import create_assistant, ask_question
import os

MODEL_PATH = os.path.expanduser('~/llms/ggml-model-Q4_1.gguf')
assistant = create_assistant(MODEL_PATH)

def ask(request):
    question = request.GET.get('question')
    if not question:
        return JsonResponse({'error': 'No question provided'}, status=400)

    answer = ask_question(assistant, question)
    return JsonResponse({'response': answer})

