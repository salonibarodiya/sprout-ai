import os
from flask import Flask, request, jsonify, render_template
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration, Part
from database import add_baby_task, get_today_plan, clear_all_tasks

app = Flask(__name__, template_folder='templates')

PROJECT_ID = "sprout-ai-492515"
vertexai.init(project=PROJECT_ID, location="us-central1")

# Explicit Tool Setup
sprout_tools = Tool(function_declarations=[
    FunctionDeclaration.from_func(add_baby_task),
    FunctionDeclaration.from_func(get_today_plan),
    FunctionDeclaration.from_func(clear_all_tasks),
])

model = GenerativeModel(
    model_name="gemini-2.5-flash", 
    tools=[sprout_tools],
    system_instruction="You are Sprout AI. ALWAYS call get_today_plan first. If user says 'delete' or 'clear', call clear_all_tasks."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_msg = request.json.get("message")
        chat_session = model.start_chat()
        response = chat_session.send_message(user_msg)
        
        active_agent = "Sprout Coordinator"
        full_text = []

        # Turn-based handling (Up to 5 turns)
        for _ in range(5):
            candidate = response.candidates[0]
            
            # 1. Collect any text that IS available
            for part in candidate.content.parts:
                # Manual check instead of using .text property
                part_dict = Part.to_dict(part)
                if 'text' in part_dict:
                    full_text.append(part_dict['text'])
            
            # 2. Check for function calls
            found_fc = False
            for part in candidate.content.parts:
                part_dict = Part.to_dict(part)
                if 'function_call' in part_dict:
                    found_fc = True
                    active_agent = "DB_Connector_v1"
                    f_name = part_dict['function_call']['name']
                    f_args = part_dict['function_call'].get('args', {})
                    
                    # Execute tool
                    if f_name == "get_today_plan":
                        res = get_today_plan()
                    elif f_name == "clear_all_tasks":
                        res = clear_all_tasks()
                    else:
                        res = add_baby_task(time=f_args.get('time'), activity=f_args.get('activity'))
                    
                    # Feed result back
                    response = chat_session.send_message(
                        Part.from_function_response(name=f_name, response={"result": res})
                    )
                    break 
            
            if not found_fc:
                break

        final_reply = " ".join(full_text).strip()
        if not final_reply:
            # Fallback if AI only performed actions
            final_reply = "Process complete, dear! Anything else?"

        return jsonify({"reply": final_reply, "agent": active_agent})

    except Exception as e:
        # Detailed error logging for you
        print(f"DEBUG: {str(e)}")
        return jsonify({"reply": f"Technical Glitch: {str(e)}", "agent": "System-Log"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))