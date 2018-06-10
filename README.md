# ChoralCentral

https://pypi.org/project/python-decouple/#why-not-just-use-environment-variables

## Priority

1. Update site certificate
1. Consolidate multiple variation of same author name (Handel, Haendel)
1. Reset all app keys (facebook, twitter, google, yahoo)
1. Turn off debug
1. Reset db, tidy up migrations and have 5 songs ready to upload.
1. Optimize for search engine
1. Write as many tests as possible. Test management commands and song_media app
1. Suggest names to user based on similarity with already present names. Create it if they're sure its not the same person.
1. In siteusers index, count only published songs and posts
1. Clear media folder

## To do

1. Send weekly summary of activities upon subscription
1. Download user comments
1. Display comment replies properly
1. Revisit request status
1. Cache
1. Explore delivering midis via podcast
1. Redefine scripture reference as a model
1. mysql grant privilege
1. GRANT ALL PRIVILEGES ON myproject_test.* TO 'chandan'@'localhost';
1. https://docs.djangoproject.com/en/2.0/topics/db/multi-db/
1. Implement user mass compilation (multiple) model: MyMass
1. Implement recommendation system
1. Implement notification on response to request
1. Implement view "exchange with this user"
1. Allow users select songs they think is similar to a particular song
1. Store users' likes and favorites
1. Add psalm tune module
1. create mass song sheet downloadable
1. Paginate search results
1. Wrap lyrics field and expand when there is match
1. Write privacy policy
1. Write terms of use
1. Write proper like script
1. mp3 and midi display in song detail view
1. Fix quoted comment display
1. Write post likers view
1. Write tests for social logins
1. Fix groups
1. Implement notification system (for request reply)
1. Custom authentication for all API views
1. Posts can contain pictures

## Management commands

    python manage.py cc_backup_score
    python manage.py cc_backup_midi
    python manage.py cc_reset_api_quotas

## Badges

1. First song, post, request

## Resources

1. <https://github.com/jazzband/django-model-utils>
