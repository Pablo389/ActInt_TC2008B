from fastapi import FastAPI, WebSocket
from model.warehouse_model import WarehouseModel
import numpy as np
from vision.vision import ComputerVision

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Warehouse Simulation API"}

@app.websocket("/ws/simulation/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Configuración inicial del modelo
    parameters = {
        'R': 5,      # Número de robots
        'K': 20,     # Número de cajas
        'P': 4,      # Número de pilas
        'M': 11,     # Altura de la cuadrícula
        'N': 11,     # Ancho de la cuadrícula
        'steps': 500 # Número de pasos
    }
    model = WarehouseModel(parameters)
    model.setup()  # Inicializa el modelo

    while True:
        data = await websocket.receive_text()  # Espera mensaje del cliente
        if data == "step":  # Si el mensaje es "step", avanza un paso en la simulación
            if model.t >= model.p.steps:
                model.end()
                await websocket.send_json({"status": "simulation finished"})
                break
            model.step()

            agents_data = []
            for robot in model.robots:
                agent_type = 1 
                x, y = model.grid.positions[robot]
                print(robot.carrying_object) # ver si el robot esta cargando una caja
                is_carrying = 0
                if robot.carrying_object:
                    is_carrying = 1
                agents_data.append({'agentType': agent_type, 'agentId': robot.id, 'x': x, 'y': y, 'carryingObject': is_carrying})
            
            
            actual_valid_objects = 0
            for object in model.objects:
                if object in model.grid.positions:
                    actual_valid_objects += 1
                    agent_type = 2 
                    x, y = model.grid.positions[object] 
                    agents_data.append({'agentType': agent_type,  'agentId': object.id,'x': x, 'y': y})
            
            #Ver cuantas cajas inicializamos y cuantas hay ahora
            print(len(model.objects))
            print(actual_valid_objects)

            for pile in model.piles:
                agent_type = 3 
                x, y = model.grid.positions[pile]  
                agents_data.append({'agentType': agent_type, 'agentId': pile.id, 'x': x, 'y': y, 'height': pile.get_height()})
                            
            model.print_grid()
            
            #Regresa los pasos y la información de posicion de los agentes
            await websocket.send_json({"status": "step completed", 'step': model.t, "state": agents_data})
        elif data == "close":
            await websocket.close()
            break

@app.websocket("/ws/vision/")
async def websocket_endpoint_frame(websocket: WebSocket):
    await websocket.accept()

    
    while True:
        data = await websocket.receive_text()  # Espera mensaje del cliente
        if data:
         
            vision = ComputerVision(data)

          
            await websocket.send_json({"data": vision})
        elif data == "close":
            await websocket.close()
            break