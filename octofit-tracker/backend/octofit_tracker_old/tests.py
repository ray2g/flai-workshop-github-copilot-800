from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            team_id='team_test',
            fitness_level='beginner'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(str(self.user), 'testuser (test@example.com)')

    def test_user_fields(self):
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.fitness_level, 'beginner')


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            _id='team_test',
            name='Test Team',
            description='A test team',
            members=[]
        )

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            username='testuser',
            team_id='team_test',
            activity_type='running',
            duration_minutes=30,
            calories_burned=300,
            distance_km=5.0,
            notes='Morning run',
            date='2026-02-04'
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.username, 'testuser')
        self.assertEqual(self.activity.duration_minutes, 30)
        self.assertEqual(self.activity.calories_burned, 300)


class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'api@example.com',
            'username': 'apiuser',
            'first_name': 'API',
            'last_name': 'User',
            'team_id': 'team_test',
            'fitness_level': 'intermediate'
        }

    def test_create_user(self):
        response = self.client.post('/api/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'apiuser')

    def test_get_users(self):
        User.objects.create(**self.user_data)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            '_id': 'team_api_test',
            'name': 'API Test Team',
            'description': 'Team for API testing',
            'members': []
        }

    def test_create_team(self):
        response = self.client.post('/api/teams/', self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_get_teams(self):
        Team.objects.create(**self.team_data)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'username': 'testuser',
            'team_id': 'team_test',
            'activity_type': 'cycling',
            'duration_minutes': 45,
            'calories_burned': 400,
            'distance_km': 15.0,
            'notes': 'Evening ride',
            'date': '2026-02-04'
        }

    def test_create_activity(self):
        response = self.client.post('/api/activities/', self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)

    def test_get_activities(self):
        Activity.objects.create(**self.activity_data)
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'A test workout routine',
            'difficulty': 'beginner',
            'duration_minutes': 30,
            'exercises': [
                {'name': 'Push-ups', 'sets': 3, 'reps': 10}
            ]
        }

    def test_create_workout(self):
        response = self.client.post('/api/workouts/', self.workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)

    def test_get_workouts(self):
        Workout.objects.create(**self.workout_data)
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_leaderboard(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_leaderboard(self):
        response = self.client.get('/api/leaderboard/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_leaderboard(self):
        response = self.client.get('/api/leaderboard/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
