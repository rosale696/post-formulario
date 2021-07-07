from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json

app = FastAPI(title = "FastAPI con Jinja2")
app.mount("/rutarecursos", StaticFiles(directory="recursos"), name="mirecurso")
miPlantilla = Jinja2Templates(directory="plantillas")

async def cargarJSON():
    with open('lista_alumnos.json',"r") as archivo_json:
        datos = json.load(archivo_json)
        #print(datos)
    return datos

async def guardarJSON(datosAgregar:List):
    with open('lista_alumnos.json',"w") as archivo_json:
        #json.dump(datosAgregar, archivo_json)
        json.dump(datosAgregar, archivo_json, indent=4)


@app.get("/inicio/", response_class=HTMLResponse)
async def read_item(request: Request):
    return miPlantilla.TemplateResponse("index.html",{"request":request})


@app.get("/lista", response_class=HTMLResponse)
async def iniciar(request: Request):
    datos = await cargarJSON()
    return miPlantilla.TemplateResponse("listaIntegrantes.html",{"request":request,"lista":datos})


@app.post("/agregar")
async def agregar(request:Request):
    datos = await cargarJSON()
    nuevos_datos = {}
    datos_formulario = await request.form()
    #print(len(datos))
    #print(datos)
    #print("fin de prueba")
    ultmimo_id = datos[-1].get("item_id")  #valor del ide del ultimo elemento de la lista
    #print(datos_formulario)
    #print(datos_formulario["f_nombre"])
    #print(datos_formulario.items)
    nuevos_datos["item_id"] = ultmimo_id+1
    nuevos_datos["matricula"] = int(datos_formulario["f_matricula"])
    nuevos_datos["nombre"] = datos_formulario["f_nombre"]
    nuevos_datos["edad"] = int(datos_formulario["f_edad"])
    #print(nuevos_datos)
    datos.append(nuevos_datos)
    #print(datos)

    await guardarJSON(datos)

    return RedirectResponse("/lista",303)

@app.get("/eliminar/{id}")
async def eliminar(request:Request,id:int):
    datos = await cargarJSON()

    del datos[id]

    await guardarJSON(datos)

    return RedirectResponse("/lista",303)