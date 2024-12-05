# Initialize an empty dictionary for the structure
data = {}

# Helper function to add a tag and value to the nested dictionary
def add_to_structure(tags, value=None):
    current = data
    for tag in tags[:-1]:  # Traverse to the second-to-last level
        if tag not in current:
            current[tag] = []  # Ensure intermediate levels are lists
        # Ensure the last element in the list is a dictionary
        if not current[tag] or not isinstance(current[tag][-1], dict):
            current[tag].append({})
        current = current[tag][-1]  # Dive into the last dictionary in the list

    # Add the final tag with the value
    last_tag = tags[-1]
    if value is not None:
        current[last_tag] = value  # Assign the value directly for the final tag
    else:
        if last_tag not in current:
            current[last_tag] = []  # Create an empty list for nesting

# Simulate receiving tags from the socket
received_tags = [
    (1, None),  # Tactic
    (2, None),  # BWDP
    (3, None),  # LitVenues
    (4, None),  # LitVenue
    (5, 'a'),   # venue1
    (6, 'b'),   # venue2
    (7, None),  # ClientList
    (8, {'venue1': 'a'}),  # venue
    (9, 1),     # TimedRelease
]

# Map tag numbers to field names
tag_map = {
    1: "Tactic",
    2: "BWDP",
    3: "LitVenues",
    4: "LitVenue",
    5: "venue1",
    6: "venue2",
    7: "ClientList",
    8: "venue",
    9: "TimedRelease",
}

# Process each tag and build the structure
current_path = []
for tag, value in received_tags:
    tag_name = tag_map[tag]
    if value is None:
        # If no value is provided, it's a parent tag; add it to the path
        current_path.append(tag_name)
        add_to_structure(current_path)
    else:
        # If a value is provided, add it to the current path
        add_to_structure(current_path + [tag_name], value)
        # Backtrack for the next sibling
        current_path.pop()

# Print the resulting structure
import pprint
pprint.pprint(data)
