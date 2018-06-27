from django.contrib.contenttypes.models import ContentType

def star_or_unstar_object(siteuser, pk, app_label, model):
    """
    Generic function for starring objects

    Parameters
    ------------
    app_label : str
        Sent with ajax request
    model_name : str
        Sent with ajax request
    """
    # Get the object
    obj_ct = ContentType.objects.get(app_label=app_label, model=model)
    model_instance = obj_ct.get_object_for_this_type(pk=pk)

    if model_instance.likes.filter(screen_name=siteuser.screen_name).exists():
        model_instance.likes.remove(siteuser)
        data = {'success' : True, 'message' : 'You disliked this {}'.format(model)}
    else:
        model_instance.likes.add(siteuser)
        data = {'success' : True, 'message' : 'You liked this {}'.format(model)}

    like_count = model_instance.likes.count()
    model_instance.save(update_fields=['like_count'])
    return data
