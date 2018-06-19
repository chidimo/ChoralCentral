# ChoralCentral

## Production setup

1. Set DEBUG False
1. Run `production_setup()` from `starter.py`
1. Reset all app keys (facebook, twitter, google, yahoo, algolia)
1. Remake all migrations and reset db
1. 5 songs ready to upload.
1. Clear media folder
1. Regenerate staticfiles
1. Change my personal account and django admin password (lastpass)
1. Edit the sites app and replace example.com with choralcentral.net

    python manage.py makemigrations siteuser

    python manage.py makemigrations song

    python manage.py makemigrations blog

    python manage.py makemigrations author

    python manage.py makemigrations song_media

    python manage.py makemigrations request

    python manage.py makemigrations drb

## Maintenance

1. Management commands

    python manage.py cc_backup_score

    python manage.py cc_backup_midi

    python manage.py cc_reset_api_quotas

1. Keep writing tests
1. Update site certificate
1. Optimize queries

## To do

1. Permissions
1. Management command to clean thumbnails with no score (trigger when score is deleted)
1. Users contribute lyrics and author bio
1. Optimize for search engine
1. Write as many tests as possible. Test management commands and song_media app
1. Suggest names to user based on similarity with already present names. Create it if they're sure its not the same person.
1. Consolidate multiple variation of same author name (Handel, Haendel)
1. Send weekly summary of activities upon subscription
1. Download user comments
1. Display comment replies properly
1. Revisit request status
1. Cache
1. Explore delivering midis via podcast
1. Redefine scripture reference as a model
1. Implement user mass compilation (multiple) model: MyMass
1. Implement recommendation system
1. Implement notification on response to request
1. Allow users select songs they think is similar to a particular song
1. Store users' likes and favorites
1. Add psalm tune module
1. create mass song sheet downloadable
1. Paginate search results
1. Wrap lyrics field and expand when there is match
1. Write privacy policy
1. Write terms of use
1. Fix quoted comment display
1. Write tests for social logins
1. Fix groups
1. Custom authentication for all API views
1. Posts can contain pictures

## Badges

1. First song, first post, first request, first midi, first score, enthusiast, helping hand

git+https://github.com/immensity/django-likes.git

## Optimize for search engine

some

## Libraries

1. Whitenoise
1. django-compressor. For windows, needs install Visual C++ build tools
1. django-robots

## Resources

1. mysql grant privilege
1. GRANT ALL PRIVILEGES ON myproject_test.* TO 'chandan'@'localhost';
1. <https://github.com/jazzband/django-model-utils>
1. <http://www.robotstxt.org/db.html>
