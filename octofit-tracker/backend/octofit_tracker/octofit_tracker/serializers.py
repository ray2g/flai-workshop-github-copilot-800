from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['_id', 'email', 'username', 'first_name', 'last_name', 
                  'team_id', 'fitness_level', 'created_at']
        read_only_fields = ['_id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'members']
        read_only_fields = ['created_at']
    
    def get_members(self, obj):
        """Convert ObjectIds to user information"""
        import ast
        members_data = obj.members
        
        # If members is a string, parse it
        if isinstance(members_data, str):
            try:
                # Remove 'ObjectId()' wrappers and parse the string
                members_str = members_data.replace("ObjectId('", "'").replace("')", "'")
                members_data = ast.literal_eval(members_str)
            except:
                return []
        
        # If members is not a list, return empty array
        if not isinstance(members_data, list):
            return []
        
        # Convert ObjectIds to strings and fetch user data
        member_list = []
        for member_id in members_data:
            try:
                # Convert to ObjectId if it's a string
                if isinstance(member_id, str):
                    member_id = ObjectId(member_id)
                
                # Fetch user by ObjectId
                user = User.objects.filter(_id=member_id).first()
                if user:
                    member_list.append({
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    })
            except Exception as e:
                print(f"Error processing member {member_id}: {e}")
                continue
        
        return member_list


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
