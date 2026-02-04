from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'team_id', 'fitness_level', 'created_at']
    list_filter = ['fitness_level', 'team_id', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['_id', 'name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['username', 'activity_type', 'duration_minutes', 'calories_burned', 
                    'team_id', 'date', 'created_at']
    list_filter = ['activity_type', 'team_id', 'date']
    search_fields = ['username', 'activity_type', 'notes']
    ordering = ['-created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['username', 'team_name', 'total_workouts', 'total_duration_minutes',
                    'total_calories_burned', 'total_distance_km', 'updated_at']
    list_filter = ['team_id']
    search_fields = ['username', 'team_name']
    ordering = ['-total_calories_burned']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'duration_minutes', 'created_at']
    list_filter = ['difficulty']
    search_fields = ['name', 'description']
    ordering = ['name']
