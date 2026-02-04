from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100, null=True, blank=True)
    fitness_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.email})"


class Team(models.Model):
    _id = models.CharField(max_length=100, primary_key=True, db_column='_id')
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.JSONField(default=list)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    user_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    workout_id = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=10)

    class Meta:
        db_table = 'activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} - {self.activity_type} ({self.duration_minutes}min)"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    team_id = models.CharField(max_length=100)
    team_name = models.CharField(max_length=200, null=True, blank=True)
    total_workouts = models.IntegerField(default=0)
    total_duration_minutes = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    total_distance_km = models.FloatField(default=0)
    average_duration = models.FloatField(default=0)
    member_count = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_calories_burned']

    def __str__(self):
        if self.username:
            return f"{self.username} - {self.total_workouts} workouts"
        return f"{self.team_name} - {self.total_workouts} workouts"


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class Workout(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    exercises = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f"{self.name} ({self.difficulty})"
