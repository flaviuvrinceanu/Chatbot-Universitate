from django.shortcuts import render
from django.http import JsonResponse
from Preprocessor.Preprocessor_class import Preprocessor
from chatbot.models import Model

def index(request):
    return render(request, 'chatbot/index.html', {'message': 'Hello, World'})

def reply(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_message = data.get('message')
        preprocessor = Preprocessor()
        model = Model()

        pipeline_message = preprocessor.begin_pipeline(user_message)
        response = model.generate(pipeline_message)

        return JsonResponse({'reply': response, 'old_message': user_message})