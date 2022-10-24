import re

# ? Why not build the entire search string with this script?
# * Replacing the set names to be "file friendly"
def sanitize_string(name):
    name = re.sub("[',:]","",name)
    name = re.sub("['\s]","_", name)    # ? Does this work with cards // like this?
    name = name.lower()
    if re.search("$_",name):            # ? What does this line exist for, again?
        name = name.rstrip(name[-1])
    return name