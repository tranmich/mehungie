# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS               # lets Squarespace call us
import openai, os, json

app = Flask(__name__)
CORS(app, origins="*")                    # loosen for MVP; tighten later

openai.api_key = os.environ["OPENAI_API_KEY"]

FEATURES = {                              # hard-coded seed burger
    "restaurant": "Burger JABS",
    "dish": "Oklahoma Smash Burger",
    "location": "630 St Clair W, Toronto",
    "features": [
        "double smashed patties",
        "griddle-sliced onions",
        "American cheese",
        "house pickles",
        "JABS sauce (mayo–ketchup relish)"
    ]
}

FUNCTIONS = [{
    "name": "generate_recipe",
    "description": "Return a detailed copy-cat recipe",
    "parameters": {
        "type": "object",
        "properties": {
            "title":       {"type": "string"},
            "servings":    {"type": "integer"},
            "ingredients": {"type": "array", "items": {"type": "string"}},
            "steps":       {"type": "array", "items": {"type": "string"}},
            "source_notes":{"type": "string"}
        },
        "required": ["title","ingredients","steps"]
    }
}]

@app.route("/clone-dish", methods=["POST"])
def clone_dish():
    data = request.get_json()
    dish = data.get("dish", "burger")

    # MVP: ignore lat/lng & always clone our seed burger
    messages=[{
        "role":"system",
        "content":"You are a professional test-kitchen chef."
    },{
        "role":"user",
        "content":(
            f"Create a copy-cat recipe from these clues:\n"
            f"{json.dumps(FEATURES, indent=2)}\n"
            "Use metric & imperial, Oklahoma smash technique, yield 2 burgers."
        )
    }]

    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=FUNCTIONS,
        function_call={"name":"generate_recipe"},
        response_format={"type":"json_object"}
    )

    recipe = json.loads(resp.choices[0].message.function_call.arguments)
    return jsonify(recipe)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
