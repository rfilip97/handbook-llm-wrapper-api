from django.shortcuts import render
from django.http import JsonResponse


def ask_question(request):
    question = request.GET.get('question')
    if question:
        response = 'Some response'

        return JsonResponse({'response': response})
    return JsonResponse({'error': 'No question provided'}, status=400)
