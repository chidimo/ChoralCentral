
from setupshell import setupshell
from season_masspart import create_seasons, create_masspart
from voicing_language import create_voicing_language
from siteusers import createsuperuser, create_roles, create_siteusers
# from author import create_authors
from song_from_file import create_songs, add_manyfields

if __name__=="__main__":
    setupshell()
    create_seasons()
    create_masspart()
    createsuperuser() #run fixtures/siteusers.py
    create_roles()
    create_siteusers(int(input("Enter number of users to create: ")))
    create_voicing_language()
    # create_authors() # optional
    create_songs("fixtures/hymnal.json")
    add_manyfields()
