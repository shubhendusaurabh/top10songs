from rest_framework import serializers

from .models import Chart, Song, CustomChart

class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song

class ChartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chart