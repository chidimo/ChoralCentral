import rules
from rules import predicate

RULE_MESSAGES = {}
RULE_MESSAGES['OPERATION_FAILED'] = "You do not have sufficient right to perform this operation."
RULE_MESSAGES['OPERATION_SUCCESSFUL'] = "Operation successfully completed"
RULE_MESSAGES['RESTRICTED_PAGE'] = "You do not have sufficient right to view this page."

def user_permissions(user):
    return [each.code_name for each in user.siteuser.siteuserpermission_set.all()]

def is_author_creator(user, author):
    return user == author.originator.user
