"""run fixtures/season_masspart.py"""

from masspart.models import MassPart
from season.models import Season
from setupshell import setupshell
from seed import PARTS, SEASONS

def create_seasons():
    for each in SEASONS:
        Season.objects.get_or_create(season=each)
        
def create_masspart():
    for each in PARTS:
        MassPart.objects.get_or_create(part=each)

if __name__ == "__main__":
    setupshell()
    create_masspart()
    create_seasons()
