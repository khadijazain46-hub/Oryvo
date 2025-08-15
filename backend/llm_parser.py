from groq import Groq
import json
import os

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def extract_drawing_instructions(prompt: str):
    system_prompt = "Convert this room design prompt to structured geometry."

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "generate_geometry",
                    "description": "Convert user room prompt into geometry format",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rooms": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "label": {"type": "string"},
                                        "size": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "description": "[width, height] in meters"
                                        },
                                        "position": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "description": "[x, y] position in meters"
                                        }
                                    },
                                    "required": ["label", "size", "position"]
                                }
                            }
                        },
                        "required": ["rooms"]
                    }
                }
            }
        ],
        tool_choice={"type": "function", "function": {"name": "generate_geometry"}}
    )

    args = response.choices[0].message.tool_calls[0].function.arguments
    return json.loads(args)
