from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import timedelta

from .models import SystemItem
from .serializers import DateSerializer, SystemItemImportRequest, SystemItemImport, SystemItemHistoryResponse


class DeleteView(GenericAPIView):
    queryset = SystemItem.objects.all()

    def delete(self, request, item_id):
        serializer = DateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query = self.get_queryset()
        obj = get_object_or_404(query, id=item_id)
        obj.delete()
        return Response(status=200)


class UpdatesView(GenericAPIView):
    queryset = SystemItem.objects.filter(type='FILE')

    def get_queryset_date(self, date):
        query = self.get_queryset()
        query.filter(date__gte=date - timedelta(days=1)).filter(date__lte=date)
        return query

    def get(self, request):
        serializer = DateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data['date']
        query = self.get_queryset_date(date)
        result = SystemItemHistoryResponse({'items':query}).data
        return Response(result, status=200)


class ImportsView(GenericAPIView):
    serializer_class = SystemItemImportRequest

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = serializer.data['items']
        date = serializer.data['updateDate']
        for item in items:
            item['date'] = date
        serializer = SystemItemImport(data=items, many=True)
        serializer.is_valid()
        serializer.save()
        return Response(status=200)


class NodeView(GenericAPIView):
    queryset = SystemItem.objects.all()
    serializer_class = SystemItemImport

    def get(self, request, item_id):
        query = self.get_queryset()
        obj = get_object_or_404(query, id=item_id)
        serializer = self.get_serializer()
        result = serializer.apply(obj)
        return Response(result, status=200)
