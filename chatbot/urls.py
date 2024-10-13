
from django.urls import path
from . import views
urlpatterns = [
        path('chat-bot-response',views.chat_bot,name="chat-bot"),
        path('get-info',views.get_information,name="get_information")

]
