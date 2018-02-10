"""run fixtures/blog.py"""

# pylint: disable=C0301, E1101, W0611, C0411, C0111

from random import randint, choice

from py_webber import LoremPysum

from siteuser.models import SiteUser
from song.models import Song
from blog.models import Post, Comment

def create_posts():
    USERS = SiteUser.objects.all()
    SONGS = Song.objects.all()
    TEX = LoremPysum()

    numb = int(input("Enter number of posts to create "))
    for _ in range(numb):

        title = TEX.title()
        body = TEX.sentences(count=randint(4, 8))

        selector = randint(0, 1)
        if selector and (len(SONGS) > 0):
            _ = Post.objects.get_or_create(
                    creator=choice(USERS),
                    title=title,
                    body=body,
                    song=choice(SONGS),
                    status=choice(["DRAFT", "PUBLISHED"]))
        else:
            _ = Post.objects.get_or_create(
                    creator=choice(USERS),
                    title=title,
                    body=body,
                    status=choice(["DRAFT", "PUBLISHED"]))

def comment_on_posts():
    for post in Post.objects.all():
        for _ in range(randint(5, 50)):
            _ = Comment.objects.create(creator=choice(USERS), post=post, comment=TEX.sentence())

if __name__ == "__main__":
    pass
