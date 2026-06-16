from fastapi import FastAPI, BackgroundTasks
import asyncio

# Absolute internal package routing
from memory.secure_memory import SecureMemory
from screen_capture.capture import ScreenEngine
from vision_engine.analyzer import VisionEngine
from action_executor.executor import ActionExecutor
from safety_controller.gatekeeper import SafetyController
from voice_engine.audio import VoiceEngine

app = FastAPI(title="Local Autonomous Agent System Core")

# Instantiate Singleton System Components
memory = SecureMemory()
screener = ScreenEngine()
vision = VisionEngine()
executor = ActionExecutor()
safety = SafetyController()
voice = VoiceEngine()

class AgentState:
    def __init__(self):
        self.is_running = False
        self.current_task = ""

state = AgentState()

@app.get("/")
def home():
    return {
        "status": "Local Autonomous Agent is online!",
        "instructions": "Go to http://127.0.0.1:8000/docs to control the agent interactive loops."
    }

@app.post("/api/task/start")
def start_agent_task(task_prompt: str, background_tasks: BackgroundTasks):
    if not state.is_running:
        state.is_running = True
        state.current_task = task_prompt
        background_tasks.add_task(execution_loop)
    return {"status": "Execution Loop Started", "task": task_prompt}

@app.post("/api/task/stop")
def stop_agent_task():
    state.is_running = False
    return {"status": "Execution Loop Paused/Stopped"}

async def execution_loop():
    print("Agentic Process Pipeline Engaged...")
    
    # Pre-seed sample secure information into memory for the example loop
    memory.save("first_name", "John")
    
    while state.is_running:
        if safety.is_paused:
            await asyncio.sleep(1)
            continue
            
        # 1. Capture screen structure
        base64_frame = screener.capture_screenshot_as_base64()
        
        # 2. Analyze screen using local model
        analysis = vision.analyze_screen(base64_frame, state.current_task)
        print(f"[Loop Context Matrix Analysis]: {analysis}")
        
        # 3. Decision Logic Parsing Engine Mock Example
        # In full production, this maps output JSON schemas directly from Ollama
        if "form" in analysis.lower() or "input" in analysis.lower():
            saved_name = memory.get("first_name")
            
            # Form Filling Flow triggered via voice check
            voice.speak(f"I see an available form target. Should I auto-populate your first name as {saved_name}?")
            
            # Listen to mic for response confirmation
            user_response = voice.listen_and_transcribe()
            
            if "yes" in user_response.lower() or "sure" in user_response.lower():
                voice.speak("Filling field now.")
                # Execute mouse click/typing actions safely
                executor.type_text(saved_name)
            else:
                voice.speak("Understood, skipping action.")
                
        # Cool-down break to ensure local processes don't loop-hammer VRAM resources
        await asyncio.sleep(5)