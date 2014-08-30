# Inspired by http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/

from django.db import models

class Parent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def children(self):
        return Child.objects.filter(parent=self)


class Child(models.Model):
    parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=255)