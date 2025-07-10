from fastapi import FastAPI, status, HTTPException, Query
# import os
import json
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="Train-Station API",
    version="1.0.0"
)

def load_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

trains_db = load_data("trains.json")
stations_db = load_data("stations.json")



# class Train(BaseModel):
#     # station_id: str
#     days: List[str]
#     arrival: str
#     departure: str
#     day: str

# class TrainWithStationId(Train):
#     # station_id: str
#     days: List[str]
#     arrival: str
#     departure: str
#     day: str

# class Station(BaseModel):
#     # train_id: str
#     days: List[str]
#     arrival: str
#     departure: str
    

class Stop(BaseModel):
    arrival: str
    departure: str
    day: str
    days: List[str]

class NewTrainRequest(BaseModel):
    train_id: str
    schedule: Dict[str, Stop]


class AddToStationRequest(BaseModel):
    train_id: str
    arrival: str
    departure: str
    days: List[str]



def save_data():
    try:
        with open("trains.json", "w") as f:
            json.dump(trains_db, f, indent=4)
        with open("stations.json", "w") as f:
            json.dump(stations_db, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

@app.get("/")
def hello():
    return "Hello world, hey there!"


# --- Train APIs ---

@app.get('/trains', 
        #  response_model=Dict[str, Dict[str, Station]], 
         status_code=status.HTTP_200_OK)
def get_all_trains_info():
    trains_info = {}

    for train_id, schedule in trains_db.items():
        stations = list(schedule.keys())
        if stations:
            start_station = stations[0]
            end_station = stations[-1]

            trains_info[train_id] = f"{start_station} to {end_station}"

    return trains_info


@app.get('/trains/{train_id}', 
        #  response_model=Dict[str, Station], 
         status_code=status.HTTP_200_OK)
def get_train_info(train_id: str):
    train = trains_db[train_id]

    if not train:
        raise HTTPException(
            status_code=404,
            detail=f"Train with {train_id} not found."
        )


    return train


@app.post('/trains',
        #    response_model=Dict[str, Station], 
          status_code=status.HTTP_201_CREATED)
def add_train(train_info: NewTrainRequest):
    train_id = train_info.train_id

    # print("train_id", train_id)

    if train_id in trains_db:
        raise HTTPException(
            status_code=409,
            detail=f"A train with similar Id {train_id} already exists"
        )
    
    # Update trains_db
    trains_db[train_id] = train_info.schedule.model_dump()
    
    # Also update stations_db for consistency
    for station_name, stop_info in train_info.schedule.items():
        if station_name not in stations_db:
            stations_db[station_name] = {}
        stations_db[station_name][train_id] = {
            "arrival": stop_info.arrival,
            "departure": stop_info.departure,
            "days": stop_info.days
        }

    
    save_data()
        
    return {"message": "Train added successfully", "train_id": train_id}


# ----- Station APIs -----

@app.get('/stations', status_code=status.HTTP_200_OK)
def get_all_station_names():
    return list(stations_db.keys())



@app.get('/stations/{station_name}', status_code=status.HTTP_200_OK)
def get_station_schedule(station_name: str):
    if station_name not in stations_db:
        raise HTTPException(
            status_code=404,
            detail="station not found"
        )

    return { station_name : stations_db[station_name]}

@app.post('/stations/{station_name}', status_code=status.HTTP_201_CREATED)
def add_or_update_station(station_name: str, train_info: AddToStationRequest):

    train_id = train_info.train_id
    
    if station_name not in stations_db:
        stations_db[station_name] = {}
        
    stations_db[station_name][train_id] = {
        "arrival": train_info.arrival,
        "departure": train_info.departure,
        "days": train_info.days
    }

    save_data()
    
    return {"message": f"Train {train_id} added to station {station_name} schedule."}



# --- Search API ---

@app.get('/search', status_code=status.HTTP_200_OK)
def get_between_trains_data(origin: str = Query(..., alias="from"), destination: str = Query(..., alias="to")):
    if origin not in stations_db or destination not in stations_db:
        raise HTTPException(status_code=404, detail="One or both stations not found.")


    matching_trains = []

    for train_id, schedule in trains_db.items():
        station_names = list(schedule.keys())
        
        try:
            origin_index = station_names.index(origin)
            destination_index = station_names.index(destination)
            
            if origin_index < destination_index:
                origin_stop = schedule[origin]
                destination_stop = schedule[destination]
                
                matching_trains.append({
                    "train_id": train_id,
                    "origin": {
                        "station": origin,
                        "departure": origin_stop["departure"],
                    },
                    "destination": {
                        "station": destination,
                        "arrival": destination_stop["arrival"],
                    },
                    "operational_days": origin_stop["days"]
                })
        except ValueError:
            continue
            
    return matching_trains


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)