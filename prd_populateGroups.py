import csv
import json
from prd_cypher import executeCypher
import time

def processRow(user_code, groups):
    if not groups:
        return True

    query = f"""
    MATCH (e:Employee {{userCode: {json.dumps(user_code)}}})
    UNWIND {json.dumps(groups)} AS groupName
      MATCH (g:RBACGroup {{name: groupName}})
      MERGE (e)-[:PART_OF]->(g)
    """

    for attempt in range(1, 4):  # hardcoded 3 retries
        try:
            executeCypher(query)
            time.sleep(0.05)
            return True
        except Exception as e:
            print(f"Attempt {attempt} failed for user {user_code}: {e}")
            time.sleep(0.2)  # small delay before retry

    # if all retries fail
    return False

def processRelationships():
    LIMIT_ROWS = 4000
    success_count = 0
    failure_count = 0

    with open('input.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        first_column = next(iter(reader.fieldnames))  # first column = user code

        for i, row in enumerate(reader):
            if i >= LIMIT_ROWS:
                break

            user_code = row[first_column].strip()
            groups = [
                row[column].strip()
                for column in reader.fieldnames
                if 'group' in column.lower() and row[column].strip()
            ]

            if processRow(user_code, groups):
                success_count += 1
                print(f"Row {i+1}: Success ({user_code})")
            else:
                failure_count += 1
                print(f"Row {i+1}: Failed ({user_code})")

    print(f"\nProcessing complete. Successes: {success_count}, Failures: {failure_count}")