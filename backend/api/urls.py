from django.urls import path
from .views import ImportsView, DeleteView, NodeView#, NodeHistoryView, UpdatesView

urlpatterns = [
    path('imports', ImportsView.as_view()),
    path('delete/<str:item_id>', DeleteView.as_view()),
    path('nodes/<str:item_id>', NodeView.as_view()),

    # extra
    # path('updates', UpdatesView.as_view()),
    # path('node/<str:item_id>/history', NodeHistoryView.as_view()),
]
