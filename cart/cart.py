"""Cart"""

from django.conf import settings
from song.models import Song

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, song):
        song_id = str(song.id)
        if song_id not in self.cart:
            self.cart[song_id] = song.id
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, song):
        song_id = str(song.id)
        if song_id in self.cart:
            del self.cart[song_id]
            self.save()

    def __iter__(self):
        song_ids = self.cart.keys()
        songs = Song.objects.filter(id__in=song_ids)
        for song in songs:
            self.cart[str(song_id)]= song.id

    # def __len__(self):
    #     pass

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
