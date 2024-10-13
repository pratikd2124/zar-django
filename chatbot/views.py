from django.shortcuts import render
from django.http import JsonResponse
from .funtions import MainChatbot
from django.views.decorators.csrf import csrf_exempt
import json

chain = MainChatbot()

@csrf_exempt  # You can remove this if you're using CSRF tokens correctly
def chat_bot(request):
    if request.method == 'POST':
        # try:
            data = json.loads(request.body)
            query = data.get('message')  # Expecting 'message' key

            # Ensure 'query' is valid
            if not query:
                return JsonResponse({"error": "Malformed input, 'message' is required."}, status=400)

            # Invoke the chain with the query
            result = chain.invoke({"input": query})
            return JsonResponse({
                "status": "success",
                "NewMessage": result['answer']
            })

        # except Exception as e:
        #     print(e)
        #     return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        

from main_app.models import User
from main_app.serializers import UserSerializer
from django.db.models import Q

def get_information(request):
    query = request.GET.get('query', '')
    if query:
        user = User.objects.filter(type__in=['Material Provider', 'Service Provider']).filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(bio__icontains=query) | 
            Q(firm_name__icontains=query) | 
            Q(contact_person__icontains=query) | 
            Q(brand_name__icontains=query)
        ).first()
        
        if user:
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)
    return JsonResponse({'error': 'No user found'}, status=404)