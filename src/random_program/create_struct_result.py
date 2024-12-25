# Initialize an empty dictionary for the structure
data = {}

# Helper function to add a tag and value to the nested dictionary
def add_to_structure(path, value=None):
    """
    Add the tag and value to the nested dictionary at the correct level.

    :param path: List of tags representing the hierarchy.
    :param value: Value to be added at the final tag level.
    """
    current = data
    for tag in path[:-1]:  # Traverse to the second-to-last level
        if tag not in current:
            # Use lists for "Tactic" and "BWDP", dictionaries for others
            if tag == "Tactic" or tag == "BWDP":
                current[tag] = []
            else:
                current[tag] = {}
        if isinstance(current[tag], list):
            # Ensure the last element in the list is a dictionary
            if not current[tag] or not isinstance(current[tag][-1], dict):
                current[tag].append({})
            current = current[tag][-1]
        else:
            current = current[tag]

    # Add the final tag and value
    last_tag = path[-1]
    if value is not None:
        if last_tag == "LitVenues":
            # Ensure LitVenues contains a dictionary for LitVenue, not a list
            current[last_tag] = {"LitVenue": value}
        else:
            current[last_tag] = value
    else:
        if last_tag not in current:
            current[last_tag] = []

# Simulated incoming tags from the socket
received_tags = [
    (1, None),  # Tactic
    (2, None),  # BWDP
    (7, None),  # ClientList
    (8, {"venue1": "a"}),  # venue
    (3, None),  # LitVenues
    (4, None),  # LitVenue
    (5, "a"),   # venue1
    (6, "b"),   # venue2
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



var = {
    "Tactic": [
        {
            "BWDP": [
                {"ClientList": [{"venue": {"venue1": "a"}}]},
                {"LitVenues": [{"LitVenue": {"venue1": "a", "venue2": "b"}}]},
                {"TimedRelease": 1},
            ]
        }
    ]
}


a = {'Tactic': [{'BWDP': [
    {'ClientList': [{'venue': {'venue1': 'a'}}]},
    {'LitVenues': [{'LitVenue': {'venue1': 'a', 'venue2': 'b'}}]},
    {'TimedRelease': 1}]
}]}

