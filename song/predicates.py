import rules
from rules import predicate

CONTEXT_MESSAGES = {}
CONTEXT_MESSAGES['OPERATION_FAILED'] = "You do not have sufficient right to perform this operation."
CONTEXT_MESSAGES['OPERATION_SUCCESSFUL'] = "Operation successfully completed"
CONTEXT_MESSAGES['RESTRICTED_PAGE'] = "You do not have sufficient right to view this page."
CONTEXT_MESSAGES['URL_MOVED'] = "The resource you're looking for has moved to this new url."

def user_permissions(user):
    return [each.code_name for each in user.siteuser.siteuserpermission_set.all()]

def is_song_creator(user, song):
    return user == song.creator.user
