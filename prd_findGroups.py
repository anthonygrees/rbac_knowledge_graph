import csv
import json

def findGroups():
    # Step 1: Collect all unique groups from the CSV
    all_groups_set = set()

    with open('output.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        first_column = next(iter(reader.fieldnames))  # first column = user code

        for row in reader:
            for column in reader.fieldnames:
                if 'group' in column.lower():
                    value = row[column].strip()
                    if value:
                        all_groups_set.add(value)

    all_groups = list(all_groups_set)

    # Step 2: Generate single MERGE query for all groups
    query = f"""
    UNWIND {json.dumps(all_groups)} AS groupName
    MERGE (:RBACGroup {{name: groupName}})
    """
    
    return query