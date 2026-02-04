from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    Supports list, retrieve, create, update, and delete operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'created_at', 'fitness_level']
    ordering = ['username']

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users filtered by team_id"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            users = self.queryset.filter(team_id=team_id)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter required'}, status=400)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams.
    Supports list, retrieve, create, update, and delete operations.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a team"""
        team = self.get_object()
        if team.members:
            users = User.objects.filter(_id__in=team.members)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response([])


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    Supports list, retrieve, create, update, and delete operations.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_id', 'team_id', 'activity_type', 'date']
    search_fields = ['username', 'activity_type', 'notes']
    ordering_fields = ['created_at', 'duration_minutes', 'calories_burned']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user"""
        user_id = request.query_params.get('user_id', None)
        if user_id:
            activities = self.queryset.filter(user_id=user_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_id parameter required'}, status=400)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get activities for a specific team"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            activities = self.queryset.filter(team_id=team_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter required'}, status=400)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 7 days)"""
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        activities = self.queryset.filter(created_at__gte=week_ago)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard.
    Supports list, retrieve, create, update, and delete operations.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['team_id', 'username']
    ordering_fields = ['total_workouts', 'total_duration_minutes', 
                       'total_calories_burned', 'total_distance_km']
    ordering = ['-total_calories_burned']

    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get user leaderboard entries only"""
        entries = self.queryset.filter(user_id__isnull=False)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def teams(self, request):
        """Get team leaderboard entries only"""
        entries = self.queryset.filter(user_id__isnull=True, team_name__isnull=False)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N entries (default: 10)"""
        limit = int(request.query_params.get('limit', 10))
        entries = self.queryset.filter(user_id__isnull=False)[:limit]
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts.
    Supports list, retrieve, create, update, and delete operations.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'difficulty', 'duration_minutes', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = self.queryset.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'difficulty parameter required'}, status=400)
