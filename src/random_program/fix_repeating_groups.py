def parse_fix_message(fix_str):
    """ Parses a FIX message and properly decodes repeating groups """
    fix_str = fix_str.replace("|", "\x01")  # Convert FIX delimiter
    fields = [f for f in fix_str.split("\x01") if f]  # Remove empty fields

    fix_dict = {}  # Stores normal fields
    groups = {}  # Stores repeating groups
    i = 0

    while i < len(fields):
        if "=" in fields[i]:
            tag, value = fields[i].split("=", 1)
            tag = int(tag)

            # Check if it's a repeating group count field (e.g., 453)
            if tag == 453:
                group_count = int(value)
                fix_dict[tag] = group_count  # Store count
                i += 1

                if tag not in groups:
                    groups[tag] = []

                # Process repeating groups
                for _ in range(group_count):
                    group_data = {}  # ✅ New dictionary for each group entry

                    while i < len(fields):
                        if "=" not in fields[i]:  # Skip invalid fields
                            i += 1
                            continue

                        sub_tag, sub_value = fields[i].split("=", 1)
                        sub_tag = int(sub_tag)

                        # If we reach another top-level field, stop processing the group
                        if sub_tag == 453 or sub_tag in fix_dict:
                            break

                        group_data[sub_tag] = sub_value
                        i += 1  # Move to the next field

                    if group_data:  # ✅ Ensure only non-empty groups are stored
                        groups[tag].append(group_data)

                continue  # Skip incrementing i at the end to continue parsing

            # Store normal fields
            fix_dict[tag] = value

        i += 1  # Move to the next field

    return fix_dict, groups
