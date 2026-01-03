TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "query_hr_database",
                "description": "... use for HR queries ...",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "Set to 'hr' for HR database queries"
                        },
                        "id": {
                            "type": "string",
                            "description": "Employee ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Employee name (optional, for name-based queries)"
                        }
                    },
                    "required": ["source", "id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "query_project_database",
                "description": "... use for project queries ...",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_name": { "type": "string" },
                        "project_id": { "type": "integer" }
                    }
                }
            }
        }
    ]
