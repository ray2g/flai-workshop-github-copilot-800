from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Clearing existing data...'))
        
        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        self.stdout.write(self.style.SUCCESS('Creating unique index on users email field...'))
        
        # Create unique index on email field
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Populating teams...'))
        
        # Create Teams
        teams = [
            {
                '_id': 'team_marvel',
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now(),
                'members': []
            },
            {
                '_id': 'team_dc',
                'name': 'Team DC',
                'description': 'Justice League',
                'created_at': datetime.now(),
                'members': []
            }
        ]
        db.teams.insert_many(teams)

        self.stdout.write(self.style.SUCCESS('Populating users...'))
        
        # Create Users - Marvel Heroes
        marvel_users = [
            {
                'email': 'tony.stark@marvel.com',
                'username': 'ironman',
                'first_name': 'Tony',
                'last_name': 'Stark',
                'team_id': 'team_marvel',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'steve.rogers@marvel.com',
                'username': 'captainamerica',
                'first_name': 'Steve',
                'last_name': 'Rogers',
                'team_id': 'team_marvel',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'natasha.romanoff@marvel.com',
                'username': 'blackwidow',
                'first_name': 'Natasha',
                'last_name': 'Romanoff',
                'team_id': 'team_marvel',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'bruce.banner@marvel.com',
                'username': 'hulk',
                'first_name': 'Bruce',
                'last_name': 'Banner',
                'team_id': 'team_marvel',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'thor.odinson@marvel.com',
                'username': 'thor',
                'first_name': 'Thor',
                'last_name': 'Odinson',
                'team_id': 'team_marvel',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            }
        ]

        # Create Users - DC Heroes
        dc_users = [
            {
                'email': 'bruce.wayne@dc.com',
                'username': 'batman',
                'first_name': 'Bruce',
                'last_name': 'Wayne',
                'team_id': 'team_dc',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'clark.kent@dc.com',
                'username': 'superman',
                'first_name': 'Clark',
                'last_name': 'Kent',
                'team_id': 'team_dc',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'diana.prince@dc.com',
                'username': 'wonderwoman',
                'first_name': 'Diana',
                'last_name': 'Prince',
                'team_id': 'team_dc',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'barry.allen@dc.com',
                'username': 'flash',
                'first_name': 'Barry',
                'last_name': 'Allen',
                'team_id': 'team_dc',
                'fitness_level': 'advanced',
                'created_at': datetime.now()
            },
            {
                'email': 'arthur.curry@dc.com',
                'username': 'aquaman',
                'first_name': 'Arthur',
                'last_name': 'Curry',
                'team_id': 'team_dc',
                'fitness_level': 'intermediate',
                'created_at': datetime.now()
            }
        ]

        all_users = marvel_users + dc_users
        result = db.users.insert_many(all_users)
        user_ids = result.inserted_ids

        # Update teams with member ids
        marvel_user_ids = user_ids[:5]
        dc_user_ids = user_ids[5:]
        
        db.teams.update_one(
            {'_id': 'team_marvel'},
            {'$set': {'members': marvel_user_ids}}
        )
        db.teams.update_one(
            {'_id': 'team_dc'},
            {'$set': {'members': dc_user_ids}}
        )

        self.stdout.write(self.style.SUCCESS('Populating workouts...'))
        
        # Create Workouts
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'High-intensity military-style workout',
                'difficulty': 'advanced',
                'duration_minutes': 45,
                'exercises': [
                    {'name': 'Push-ups', 'sets': 3, 'reps': 20},
                    {'name': 'Pull-ups', 'sets': 3, 'reps': 15},
                    {'name': 'Squats', 'sets': 3, 'reps': 25},
                    {'name': 'Burpees', 'sets': 3, 'reps': 15}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Speedster Circuit',
                'description': 'Fast-paced cardio and agility workout',
                'difficulty': 'intermediate',
                'duration_minutes': 30,
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 5, 'duration': '1 minute'},
                    {'name': 'Ladder Drills', 'sets': 3, 'duration': '2 minutes'},
                    {'name': 'Box Jumps', 'sets': 3, 'reps': 15},
                    {'name': 'High Knees', 'sets': 3, 'duration': '1 minute'}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Warrior Strength',
                'description': 'Build strength like an Amazonian warrior',
                'difficulty': 'advanced',
                'duration_minutes': 60,
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 10},
                    {'name': 'Bench Press', 'sets': 4, 'reps': 12},
                    {'name': 'Overhead Press', 'sets': 3, 'reps': 10},
                    {'name': 'Barbell Rows', 'sets': 3, 'reps': 12}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Aquatic Endurance',
                'description': 'Swimming and water-based exercises',
                'difficulty': 'intermediate',
                'duration_minutes': 40,
                'exercises': [
                    {'name': 'Swimming', 'sets': 1, 'duration': '20 minutes'},
                    {'name': 'Water Treading', 'sets': 3, 'duration': '3 minutes'},
                    {'name': 'Pool Push-ups', 'sets': 3, 'reps': 15}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Tech Genius Cardio',
                'description': 'Efficient cardio workout',
                'difficulty': 'beginner',
                'duration_minutes': 25,
                'exercises': [
                    {'name': 'Jogging', 'sets': 1, 'duration': '15 minutes'},
                    {'name': 'Jumping Jacks', 'sets': 3, 'reps': 20},
                    {'name': 'Mountain Climbers', 'sets': 3, 'reps': 15}
                ],
                'created_at': datetime.now()
            }
        ]
        workout_result = db.workouts.insert_many(workouts)
        workout_ids = workout_result.inserted_ids

        self.stdout.write(self.style.SUCCESS('Populating activities...'))
        
        # Create Activities
        activities = []
        activity_types = ['running', 'cycling', 'swimming', 'weightlifting', 'yoga', 'martial_arts']
        
        for i, user in enumerate(all_users):
            for day in range(7):
                activity_date = datetime.now() - timedelta(days=day)
                num_activities = random.randint(1, 3)
                
                for _ in range(num_activities):
                    activity = {
                        'user_id': user_ids[i],
                        'username': user['username'],
                        'team_id': user['team_id'],
                        'activity_type': random.choice(activity_types),
                        'duration_minutes': random.randint(20, 90),
                        'calories_burned': random.randint(150, 600),
                        'distance_km': round(random.uniform(2.0, 15.0), 2) if random.choice([True, False]) else None,
                        'workout_id': random.choice(workout_ids) if random.choice([True, False]) else None,
                        'notes': f'{user["first_name"]} training session',
                        'created_at': activity_date,
                        'date': activity_date.strftime('%Y-%m-%d')
                    }
                    activities.append(activity)
        
        db.activities.insert_many(activities)

        self.stdout.write(self.style.SUCCESS('Populating leaderboard...'))
        
        # Create Leaderboard entries
        leaderboard_entries = []
        
        # Calculate user stats from activities
        for i, user in enumerate(all_users):
            user_activities = [a for a in activities if a['user_id'] == user_ids[i]]
            total_duration = sum(a['duration_minutes'] for a in user_activities)
            total_calories = sum(a['calories_burned'] for a in user_activities)
            total_workouts = len(user_activities)
            
            leaderboard_entry = {
                'user_id': user_ids[i],
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'team_id': user['team_id'],
                'total_workouts': total_workouts,
                'total_duration_minutes': total_duration,
                'total_calories_burned': total_calories,
                'total_distance_km': round(sum(a.get('distance_km', 0) or 0 for a in user_activities), 2),
                'average_duration': round(total_duration / total_workouts, 2) if total_workouts > 0 else 0,
                'updated_at': datetime.now()
            }
            leaderboard_entries.append(leaderboard_entry)
        
        db.leaderboard.insert_many(leaderboard_entries)

        # Calculate team stats
        marvel_activities = [a for a in activities if a['team_id'] == 'team_marvel']
        dc_activities = [a for a in activities if a['team_id'] == 'team_dc']
        
        team_leaderboard = [
            {
                'team_id': 'team_marvel',
                'team_name': 'Team Marvel',
                'total_workouts': len(marvel_activities),
                'total_duration_minutes': sum(a['duration_minutes'] for a in marvel_activities),
                'total_calories_burned': sum(a['calories_burned'] for a in marvel_activities),
                'member_count': len(marvel_users),
                'updated_at': datetime.now()
            },
            {
                'team_id': 'team_dc',
                'team_name': 'Team DC',
                'total_workouts': len(dc_activities),
                'total_duration_minutes': sum(a['duration_minutes'] for a in dc_activities),
                'total_calories_burned': sum(a['calories_burned'] for a in dc_activities),
                'member_count': len(dc_users),
                'updated_at': datetime.now()
            }
        ]
        
        db.leaderboard.insert_many(team_leaderboard)

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams)} teams'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities)} activities'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workouts'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries) + len(team_leaderboard)} leaderboard entries'))
        
        client.close()
