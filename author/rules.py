import rules
from . import predicates

# rules

rules.add_rule('edit_author', predicates.is_author_creator)
