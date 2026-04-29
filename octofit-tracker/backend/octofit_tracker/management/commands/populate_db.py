from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

# Define models for teams, activities, leaderboard, and workouts
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            # Optionally, relate user to team if you extend the User model

        # Create activities
        Activity.objects.create(user='ironman', activity_type='Running', duration=30, team='Marvel')
        Activity.objects.create(user='captainamerica', activity_type='Cycling', duration=45, team='Marvel')
        Activity.objects.create(user='batman', activity_type='Swimming', duration=60, team='DC')
        Activity.objects.create(user='superman', activity_type='Flying', duration=120, team='DC')

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=75)
        Leaderboard.objects.create(team='DC', points=180)

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity workout for heroes.', difficulty='Hard')
        Workout.objects.create(name='Sidekick Cardio', description='Cardio for sidekicks.', difficulty='Medium')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
