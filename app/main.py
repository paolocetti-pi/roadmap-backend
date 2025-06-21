from fastapi import FastAPI, HTTPException
from . import crud
from .schemas import TaskControl

app = FastAPI(
    title="Climate and Message Service",
    description="A service to automatically fetch climate data and save messages in real-time.",
    version="1.0.0"
)

@app.post("/tasks/weather/control")
def control_weather_task(task_control: TaskControl):
    """
    Enable or disable the weather fetching task.
    """
    crud.set_task_state('fetch_weather', task_control.enabled)
    status = "enabled" if task_control.enabled else "disabled"
    return {"message": f"Weather task {status}."}

@app.post("/tasks/message/control")
def control_message_task(task_control: TaskControl):
    """
    Enable or disable the message saving task.
    """
    crud.set_task_state('save_message', task_control.enabled)
    status = "enabled" if task_control.enabled else "disabled"
    return {"message": f"Message saving task {status}."}

@app.get("/weather/{location}")
def get_weather(location: str):
    """
    Get the latest weather data for a location.
    """
    data = crud.get_weather_data(location)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Weather data not found for this location.")

@app.get("/messages")
def get_messages():
    """
    Get all saved log messages.
    """
    messages = crud.get_log_messages()
    return {"messages": messages} 