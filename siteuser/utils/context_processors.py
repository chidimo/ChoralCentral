from siteuser.models import  Message

from siteuser.forms import EmailAndPassWordGetterForm

def unread_messages(request):
    try:
        unread = Message.objects.filter(receiver__user=request.user).filter(read=False).count()
        return {'unread' : unread}
    except TypeError:
        return dict()

