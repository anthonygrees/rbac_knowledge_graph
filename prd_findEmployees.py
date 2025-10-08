import csv

def findEmployee():
    with open("output.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        # Detect columns
        header_map = {}
        for col in reader.fieldnames:
            lc = col.lower()
            if "user" in lc and "code" in lc:
                header_map["userCode"] = col
            elif "position" in lc and "manager" in lc:
                header_map["managerPosition"] = col
            elif "jobtitle" in lc:
                header_map["position"] = col
            elif "department" in lc:
                header_map["department"] = col

        # Prepare data rows, skip empty userCode
        data = []
        for row in reader:
            record = {}
            for key, col in header_map.items():
                val = row[col].strip()
                if val:  # skip empty
                    # Escape quotes for Cypher
                    val = val.replace("\\", "\\\\").replace("'", "\\'")
                    record[key] = val
            if "userCode" in record:
                data.append(record)

    if not data:
        raise ValueError("No valid rows found in CSV")

    # Build query
    query = "UNWIND [\n"
    for row in data:
        parts = []
        for key in ["userCode", "position", "managerPosition", "department"]:
            if key in row:
                parts.append(f"{key}: '{row[key]}'")
        query += "  {" + ", ".join(parts) + "},\n"
    query = query.rstrip(",\n") + "\n] AS row\n"

    query += "MERGE (e:Employee {userCode: row.userCode})\n"
    if any("position" in r for r in data):
        query += "MERGE (p:Position {title: row.position})\nMERGE (e)-[:HAS_POSITION]->(p)\n"
    if any("managerPosition" in r for r in data):
        query += "MERGE (m:ManagerPosition {title: row.managerPosition})\nMERGE (e)-[:REPORTS_TO]->(m)\n"
    if any("department" in r for r in data):
        query += "MERGE (d:Department {name: row.department})\nMERGE (e)-[:IN_DEPARTMENT]->(d)\n"

    return query.strip()