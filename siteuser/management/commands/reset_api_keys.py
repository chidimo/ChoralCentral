from django.core.management.base import BaseCommand, CommandError
from siteuser.models import ApiKey

class Command(BaseCommand):
    help = 'Reset all API key quotas to default value'

    def add_arguments(self, parser):
        parser.add_argument('-quota', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start resetting api keys'))
        if options['quota']:
            quota = options['quota']
        else:
            quota = 100
        keys = ApiKey.objects.all()
        for key in keys:
            key.quota = quota
            key.save()
        self.stdout.write(self.style.SUCCESS('Done resetting api keys'))
