from rules import predicate

@predicate
def can_edit_song(user, song):
    return user == song.originator.user
