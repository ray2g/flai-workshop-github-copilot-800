from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['_id', 'email', 'username', 'first_name', 'last_name', 
                  'team_id', 'fitness_level', 'created_at']
        read_only_fields = ['_id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'members']
        read_only_fields = ['created_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'username', 'team_id', 'activity_type',
                  'duration_minutes', 'calories_burned', 'distance_km',
                  'workout_id', 'notes', 'created_at', 'date']
        read_only_fields = ['_id', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_id', 'username', 'first_name', 'last_name',
                  'team_id', 'team_name', 'total_workouts', 'total_duration_minutes',
                  'total_calories_burned', 'total_distance_km', 'average_duration',
                  'member_count', 'updated_at']
        read_only_fields = ['_id', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'difficulty', 'duration_minutes',
                  'exercises', 'created_at']
        read_only_fields = ['_id', 'created_at']
