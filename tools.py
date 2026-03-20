tools = [
    {
        "type": "function",
        "function": {
            "name": "collect_user_info",
            "description": "Collect user's name and email when query cannot be answered from context and forward it to Aashutosh",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "User's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "User's email address"
                    },
                    "query": {
                        "type": "string",
                        "description": "User's original question"
                    }
                },
                "required": ["name", "email", "query"]
            }
        }
    }
]