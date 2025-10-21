# RBAC Knowledge Graph

A Python-based tool for building and populating a Role-Based Access Control (RBAC) knowledge graph using Cypher queries. This project imports organizational data from CSV files and creates a graph database representing employees, their positions, departments, and RBAC group memberships.

## Overview

This tool processes CSV data to construct a knowledge graph with the following node types:
- **Employee**: Individual users identified by userCode
- **Position**: Job titles/positions
- **ManagerPosition**: Managerial positions for reporting structure
- **Department**: Organizational departments
- **RBACGroup**: Role-based access control groups

## Features

- Import employee data from CSV files
- Create organizational hierarchy relationships
- Map RBAC group memberships
- Batch processing with retry logic
- Integration with Airia graph database API

## File Structure

- `prd_main.py` - Main entry point with orchestration functions
- `prd_cypher.py` - Executes Cypher queries against the graph API
- `prd_findEmployees.py` - Parses employee data and generates employee/position/department nodes
- `prd_findGroups.py` - Extracts unique RBAC groups from CSV
- `prd_populateGroups.py` - Creates relationships between employees and RBAC groups
- `prd_findGraphs.py` - Utility to list available graphs
- `prd_graphStats.py` - Retrieves node count statistics

## Setup

### Prerequisites

- Python 3.x
- `requests` library

Install dependencies:
```bash
pip install requests
```

### Configuration

Update the API key and graph ID in the following files:
- `prd_cypher.py:8` - Replace `"akey-placeholder"` with your API key
- `prd_cypher.py:6` - Update graph ID in the API endpoint URL
- `prd_findGraphs.py:6` - Replace API key
- `[Person2].[Person3] key and graph ID

## Usage

### CSV File Format

The tool expects CSV files with the following columns:
- User code column (containing employee identifiers)
- Position/JobTitle column
- Manager Position column
- Department column
- Group columns (any columns with "group" in the name)

Files used:
- `output.csv` - For employee, position, and department data
- `input.csv` - For group membership relationships

### Running the Import

1. Uncomment the desired function calls in `prd_main.py`:

```python
addEmployees()     # Import employees, positions, departments
addGroups()        # Import RBAC groups
addRelationships() # Create employee-to-group relationships
```

2. Run the main script:
```bash
python prd_main.py
```

### Utilities

Check available graphs:
```bash
python prd_findGraphs.py
```

Get node count statistics:
```bash
python [Person2].py
```

## Graph Schema

### Nodes
- `Employee {userCode}`
- `Position {title}`
- `ManagerPosition {title}`
- `Department {name}`
- `RBACGroup {name}`

### Relationships
- `(Employee)-[:HAS_POSITION]->(Position)`
- `(Employee)-[:REPORTS_TO]->(ManagerPosition)`
- `(Employee)-[:IN_DEPARTMENT]->(Department)`
- `(Employee)-[:PART_OF]->(RBACGroup)`

## Processing Details

- Employee import uses `MERGE` operations to avoid duplicates
- Group relationships are processed row-by-row with a 4000 row limit
- Automatic retry logic (3 attempts) for failed operations
- 50ms delay between successful operations
- 200ms delay between retry attempts

## API Integration

This tool integrates with the Airia graph database API:
- Base URL: `https://prodaus.api.airia.ai`
- Authentication: API key via `X-API-Key` header
- Endpoints used:
  - `POST /Graphs/{graphId}/cypher` - Execute [Person4]pher queries
  - `GET /Graphs` - List available graphs
  - `GET /Graphs/{graphId}/nodes/count` - Get node statistics

## Notes

- CSV files must use UTF-8 encoding with BOM (utf-8-sig)
- Empty values are skipped during import
- Special characters in CSV data are escaped for [Person4]pher compatibility
- The main script functions are currently commented out by default for safety
