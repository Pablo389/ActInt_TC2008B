from fastapi import FastAPI, WebSocket
from model.warehouse_model import WarehouseModel

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
                agent_type = 1  # Tipo de agente (1: Robot, 2: Object, 3: Pile)
                x, y = model.grid.positions[robot]
                agents_data.append({'id': agent_type, 'x': x, 'y': y})

            for pile in model.piles:
                agent_type = 3  # Tipo de agente (1: Robot, 2: Object, 3: Pile)
                x, y = model.grid.positions[pile]  # Obtener la posición del agente
                agents_data.append({'id': agent_type, 'x': x, 'y': y})
            
            await websocket.send_json({"status": "step completed", "state": agents_data})
        elif data == "close":
            await websocket.close()
            break
