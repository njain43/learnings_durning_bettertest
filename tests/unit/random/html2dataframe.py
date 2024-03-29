# import pandas as pd
#
# # Replace 'your_url_or_file.html' with the URL or file path of your HTML content.
# # If you have HTML content in a string, you can use pd.read_html(your_html_string)
# url_or_file = 'sample.html'
#
# # Read HTML tables into a list of DataFrames
# df_list = pd.read_html(url_or_file)

# df_list now contains a list of DataFrames, where each DataFrame corresponds to a table in the HTML content.

# You can access individual DataFrames from the list, e.g., df_list[0] for the first table.

# Example: To pri/nt the first DataFrame from the list

# df = df_list[0]
# print(df)


import subprocess

# List of commands to run
commands = ["command1", "command2", "command3"]

# Counter for failed commands
failed_commands_count = 0

for command in commands:
    try:
        # Run the command in a subprocess
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Command failed, increment the counter
        failed_commands_count += 1
        print(f"Command '{command}' failed with exit code {e.returncode}")

print(f"Number of failed commands: {failed_commands_count}")





