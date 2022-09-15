from rest_framework import serializers
from django.db import transaction
from .exceptions import ValidationException

from .models import SystemItemType, SystemItem


class DateSerializer(serializers.Serializer):
    date = serializers.DateTimeField()


class SystemItemsSerializer(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField(required=False, max_length=255)
    parentId = serializers.CharField(required=False, allow_null=True, source='parent_id')
    type = serializers.ChoiceField(choices=SystemItemType)
    size = serializers.IntegerField(allow_null=True, required=False)


class SystemItemImport(SystemItemsSerializer):
    date = serializers.DateTimeField()

    def validate(self, attrs):
        attrs = super().validate(attrs)

        parent_id = attrs.get('parentId', None)
        if parent_id is not None:
            if not SystemItem.objects.filter(type='FOLDER').filter(id=parent_id).exists():
                raise ValidationException

        size = attrs.get('size', None)
        item_type = attrs.get('type')
        if size is not None:
            if item_type == 'FILE':
                if size <= 0:
                    raise ValidationException
            else:
                raise ValidationException
        else:
            if item_type == 'FILE':
                raise ValidationException

        if item_type == 'FOLDER':
            if attrs.get('url', None) is not None:
                raise ValidationException

        return attrs

    @staticmethod
    def apply(obj):
        result = SystemItemImport(obj).data
        item_type = result['type']
        if item_type == 'FILE':
            result['children'] = None
        else:
            result['url'] = None
            children = []
            children_size = 0

            for child in obj.childrens.all():
                child_validated = SystemItemImport.apply(child)
                children.append(child_validated)
                child_size = child_validated['size']
                if child_size:
                    children_size += child_size

            result['children'] = children
            result['size'] = children_size
        print(result)
        return result

    @transaction.atomic
    def create(self, validated_data):
        instance = SystemItem.objects.filter(id=validated_data['id'])
        if instance.exists():
            instance = instance.get()
            self.update(instance, validated_data)
        else:
            instance = SystemItem.objects.create(**validated_data)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data: dict):
        for field, value in validated_data.items():
            if field == 'id':
                continue
            if field == 'type':
                if getattr(instance, field) != value:
                    raise ValidationException
            if isinstance(value, list):
                getattr(instance, field).set(value)
            else:
                setattr(instance, field, value)
        instance.save()
        return instance


class SystemItemImportRequest(serializers.Serializer):
    items = serializers.ListField(child=SystemItemsSerializer())
    updateDate = serializers.DateTimeField()


class SystemItemHistoryUnit(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField(required=False, allow_null=True)
    parentId = serializers.CharField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=SystemItemType)
    size = serializers.IntegerField(allow_null=True, required=False)
    date = serializers.DateTimeField()


class SystemItemHistoryResponse(serializers.Serializer):
    items = serializers.ListField(child=SystemItemHistoryUnit())
