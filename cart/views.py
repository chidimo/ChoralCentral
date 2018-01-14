from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from song.models import Song
from .cart import Cart

@require_POST
def add_to_cart(request, song_id):
    cart = Cart(request)
    song = get_object_or_404(Song, id=song_id)
    cart.add(song)
    return redirect('cart:detail')

def remove_to_cart(request, song_id):
    cart = Cart(request)
    song = get_object_or_404(Song, id=song_id)
    cart.add(song)
    return redirect('cart:detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
