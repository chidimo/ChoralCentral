# ChoralCentral

## Production setup

1. Set DEBUG False, create production branch
1. Run `production_setup()` from `starter.py`
1. Reset all app keys (facebook, twitter, google, algolia)
1. Remake all migrations and reset db
1. 5 songs ready to upload (Bia nye chukwu ezi ekele, Ana kiranku)
1. Clear media folder, clear google drive
1. Delete `staticfiles` and rerun `python manage.py collectstatic`
1. Change my personal account and django admin password (lastpass)
1. Edit the sites app and replace example.com with choralcentral.net
1. Fix django-social-share templates

    python manage.py makemigrations siteuser

    python manage.py makemigrations song

    python manage.py makemigrations blog

    python manage.py makemigrations author

    python manage.py makemigrations song_media

    python manage.py makemigrations redirect301

    python manage.py makemigrations request

    python manage.py makemigrations drb

## Maintenance

1. Management commands

    python manage.py cc_backup_score

    python manage.py cc_backup_midi

    python manage.py cc_cleanup_scores

    python manage.py cc_cleanup_midis

    python manage.py cc_reset_api_quotas

1. Keep writing tests
1. Update site certificate
1. Optimize queries

## Optimizing database performance

1. Use of `select_related` and `prefetch_related`
1. Optimize sessions

## To do

1. Optimize for search engine
1. Permissions
1. Management command to clean thumbnails with no score (trigger when score is deleted)
1. Users contribute lyrics and author bio
1. Write as many tests as possible. Test management commands and song_media app
1. Suggest names to user based on similarity with already present names. Create it if they're sure its not the same person.
1. Consolidate multiple variation of same author name (Handel, Haendel)
1. Download user comments
1. Display comment replies properly
1. Revisit request status
1. Explore delivering midis via podcast
1. Redefine scripture reference as a model
1. Implement recommendation system
1. Implement notification on response to request
1. Store users' likes and favorites
1. Add psalm tune module
1. create mass song sheet downloadable
1. Paginate search results
1. Write privacy policy
1. Write terms of use
1. Custom authentication for all API views

## Optimizing my page

1. Minified `.css` files with <https://cssminifier.com>
1. Minified `.js` files with <https://javascript-minifier.com>
1. Compressed my custom `.css` and `.js` files using `django-compressor`
1. Moved some render-blocking javascripts to the bottom of the `<body>` tag of my base template, but `jquery` had to stay at top of page.
1. Compress `choralcentral.min.css`

## Resources

1. mysql grant privilege
1. GRANT ALL PRIVILEGES ON myproject_test.* TO 'chandan'@'localhost';
1. <https://github.com/jazzband/django-model-utils>
1. <http://www.robotstxt.org/db.html>
1. <https://docs.djangoproject.com/en/2.0/ref/settings/#settings>

## Site certificate

1. <https://help.pythonanywhere.com/pages/LetsEncrypt/>
1. `export API_TOKEN=my-api-token`
1. `pip3.5 install --user --upgrade pythonanywhere # do this in a new bash console`

### Creation

1. `cd ~/letsencrypt`
1. `/home/parousia/dehydrated/dehydrated --register --accept-terms`
1. `~/dehydrated/dehydrated --config ~/letsencrypt/config --cron --domain www.choralcentral.net --out ~/letsencrypt --challenge http-01`

### Renewal

1. `~/dehydrated/dehydrated --config ~/letsencrypt/config --cron --domain www.choralcentral.net --out ~/letsencrypt --challenge http-01`
1. `cd ~/letsencrypt && ~/dehydrated/dehydrated --cron --domain www.choralcentral.net --out . --challenge http-01 && pa_install_webapp_letsencrypt_ssl.py www.choralcentral.net # set daily task to auto-renew certificate`

### Installation

1. `cd ~/letsencrypt`
1. `~/dehydrated/dehydrated --cron --domain www.choralcentral.net --out . --challenge http-01`
1. `pa_install_webapp_letsencrypt_ssl.py www.choralcentral.net # install certificate`

## Helps

1. `pipenv install -e git+https://github.com/jazzband/django-robots.git#egg=django-robots`

## Credits

1. <https://stackoverflow.com/">
1. <https://duckduckgo.com/">
1. <https://google.com/">
1. <https://algolia.com/">
1. <https://simpleisbetterthancomplex.com/">
1. <https://linux.die.net/man/1/pdftoppm">
1. <https://askubuntu.com/">
1. <http://hilite.me">
1. <https://github.com/fcurella/django-social-share">
1. <https://en.wikipedia.org/wiki/List_of_musical_genres_by_era">

## Scenarios in social auth

1. **A clash of emails:** A valid email, `A`, exists as a `primary` account. A social account email, `B`, is now associated with `A`. Someone tries to create a new `primary` account using email `B` that is `secondary` to account `A`. I don't want that.
1. **A clash of providers:** A valid email, `A`, exists as a `primary` account *created non-socially (which means no association was made), but is nonetheless a valid email from provider `X`*. A social account email, `B`, from provider `X` is now associated with `A`. A **non-logged-in** user *invokes* provider `X` with email `A` which already has email `B` secondary to it. Result: `A` is logged-in **AND** a social association is made using provider `X`. Now there are two emails from provider `X` associated with `A`. I don't want that.
