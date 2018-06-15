import rules
from . import predicates

# rules

rules.add_rule('edit_song', predicates.is_song_creator)
