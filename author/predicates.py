import rules
from rules import predicate

CONTEXT_MESSAGES = {}
CONTEXT_MESSAGES['OPERATION_FAILED'] = "You do not have sufficient right to perform this operation."
CONTEXT_MESSAGES['OPERATION_SUCCESSFUL'] = "Operation successfully completed"
CONTEXT_MESSAGES['RESTRICTED_PAGE'] = "You do not have sufficient right to view this page."

def user_permissions(user):
    return [each.code_name for each in user.siteuser.siteuserpermission_set.all()]

def is_author_creator(user, author):
    return user == author.creator.user
