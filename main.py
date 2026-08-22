from fastapi import FastAPI
import requests as req
import datetime
import json


app = FastAPI()


@app.get("/0")
async def root():
    message = '|HOME|'
    return message


@app.get("/1")
async def page1():
    # Simulate calling a weather API      
    start_date = datetime.date.today().strftime('%Y-%m-%d')
    current_hour = ('0'+str(datetime.datetime.now().hour))[-2:]
    print(start_date)
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude=36.7783&longitude=119.4179&start_date={start_date}&end_date={start_date}&hourly=temperature_2m"
    response = req.get(url).content
    weather_information = json.loads(response)
    time_index = [weather_information['hourly']['time'].index(i) for i in weather_information['hourly']['time'] if f'T{current_hour}' in i]
    temperature = weather_information['hourly']['temperature_2m'][time_index[0]]
    return temperature

@app.get("/2")
async def page2():
    response = str(datetime.datetime.now())
    print(response)
    return response

