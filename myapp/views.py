from unittest import result
from django.http import Http404, HttpResponse, JsonResponse 
import sqlite3
from django.shortcuts import render
from django.template.loader import render_to_string
import requests 

def index(request): 
    return HttpResponse("<h1>¡Hola, mundo!</h1>")

def index2(request): 
    context = {"nombre":"Mi Blog", "descripcion": "Este es el blog de la clase",
               "portfolio": {"proyecto1":"Desarrollo Django", "proyecto2":"Data Analitycs"},
               "clientes": ["IBM", "Oracle", "Globant", "Amazon", "Mercado Libre", "Pablo_Tech"],
               "revenue": 10000,
               "sinvalor": ""
               }
    return render(request, "myapp/index.html", context)
  
def contactos(request): 
     return HttpResponse("<h2>Norman Beltran</h2>")
 
def curso(request, nombre_curso): 
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos WHERE nombre=?", [nombre_curso])
    curso = cursor.fetchone()
    conn.close()
    if curso is None:
        raise Http404 
    nombre, inscriptos = curso
    context = {"nombre": nombre, "inscriptos": inscriptos}
    return render(request, "myapp/curso.html", context)
 
def cursos(request): 
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    cursos = cursor.fetchall()
    conn.close()
    context = {"cursos": cursos}
    return render(request, "myapp/cursos.html", context)

def cursos_api(request): 
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    #response = JsonResponse(cursor.fetchall(), safe=False)
    response = JsonResponse(dict(cursor.fetchall()))
    conn.close()
    return response

def cotizacion(request): 
    oficial = requests.get('https://api-dolar-argentina.herokuapp.com/api/dolaroficial')
    blue = requests.get('https://api-dolar-argentina.herokuapp.com/api/dolarblue')
    liqui = requests.get('https://api-dolar-argentina.herokuapp.com/api/contadoliqui')
    turista = requests.get('https://api-dolar-argentina.herokuapp.com/api/dolarturista')
    bolsa = requests.get('https://api-dolar-argentina.herokuapp.com/api/dolarbolsa')
    r1 = oficial.json()
    r2 = blue.json()
    r3 = liqui.json()
    r4 = turista.json()
    r5 = bolsa.json()
    resultados = {
        "oficial":r1,
        "blue":r2,
        "liqui":r3,
        "turista":r4,
        "bolsa":r5
    }
    return render(request, "myapp/cotizacion.html",{'list':resultados})

def aeropuertos(request): 
    f = open("aeropuertos.csv", encoding="utf-8")
    html = f"""
        <html>
        <title>Lista de aeropuertos</title>
        <table style="border: 1px solid">
          <thead>
            <tr>
              <th>Aeropuerto</th>
              <th>Ciudad</th>
              <th>País</th>
            </tr>
          </thead>            
    """
    for i in f:
        datos = i.split(",")
        nombre = datos[1].replace('"','')
        ciudad = datos[2].replace('"','')
        pais = datos[3].replace('"','')
        html += f"""
            <tr>
              <td>{nombre}</td>
              <td>{ciudad}</td>
              <td>{pais}</td>
            </tr>
        """
    html += "</table></html>"
    return HttpResponse(html)

def aeropuertos_json(request): 
    f = open("aeropuertos.csv", encoding="utf-8")
    aeropuertos = []
    for i in f:
        datos = i.split(",")
        nombre = datos[1].replace('"','')
        ciudad = datos[2].replace('"','')
        pais = datos[3].replace('"','')
        aero = {
            "nombre": nombre, 
            "ciudad": ciudad,
            "pais": pais
        }
        aeropuertos.append(aero)
    f.close()
    
    return JsonResponse(aeropuertos, safe=False)