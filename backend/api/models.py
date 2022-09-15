from django.db import models


SystemItemType = (
    ('FILE', 'FILE'),
    ('FOLDER', 'FOLDER'),
)


class SystemItem(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=255)
    parent = models.ForeignKey('SystemItem', on_delete=models.CASCADE, null=True, related_name='childrens')
    type = models.CharField(choices=SystemItemType, max_length=10)
    size = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.parent:
            parent = self.parent
            parent.date = self.date
            parent.save()
