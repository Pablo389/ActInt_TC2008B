from fastapi import FastAPI, WebSocket
from model.warehouse_model import WarehouseModel
import numpy as np

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
        'M': 10,     # Altura de la cuadrícula
        'N': 10,     # Ancho de la cuadrícula
        'steps': 500 # Número de pasos
    }
    model = WarehouseModel(parameters)
    model.setup()  # Inicializa el modelo

    while True:
        data = await websocket.receive_text()  # Espera mensaje del cliente
        if data == "step":  # Si el mensaje es "step", avanza un paso en la simulación
            model.step()

            agents_data = []
            for robot in model.robots:
                agent_type = 1 
                x, y = model.grid.positions[robot]
                print(robot.carrying_object) # ver si el robot esta cargando una caja
                agents_data.append({'agentType': agent_type, 'agentId': robot.id, 'x': x, 'y': y})
            
            
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
                agents_data.append({'agentType': agent_type, 'agentId': pile.id, 'x': x, 'y': y})
                            
            model.print_grid()
            
            #Regresa los pasos y la información de posicion de los agentes
            await websocket.send_json({"status": "step completed", 'step': model.t, "state": agents_data})
        elif data == "close":
            await websocket.close()
            break
