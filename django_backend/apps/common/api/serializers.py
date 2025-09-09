from rest_framework import serializers
from apps.common.models import Team

class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.

    This serializer converts Team model instances into JSON representations
    and validates input data for creating or updating Team instances.

    Fields:
        id (int): Unique identifier of the team.
        name (str): Name of the team.
    """
    class Meta:
        model = Team
        fields = ["id", "name"]
