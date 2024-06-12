import math
import random
from flask import Flask, render_template, request

app = Flask(__name__)

def poblacion_inicial(max_poblacion, num_vars):
    # Crear población Inicial Aleatoria
    poblacion = []
    for i in range(max_poblacion):
        gen = []
        for j in range(num_vars):
            if random.random() > 0.5:
                gen.append(1)
            else:
                gen.append(0)
        poblacion.append(gen[:])
    return poblacion

def adaptacion_3sat(gen, solucion):
    # Contar las cláusulas correctas
    n = 3
    cont = 0
    clausula_ok = True
    for i in range(len(gen)):
        n = n - 1
        if (gen[i] != solucion[i]):
            clausula_ok = False
            if n == 0:
                if clausula_ok:
                    cont = cont + 1
                n = 3
                clausula_ok = True
        if n > 0:
            if clausula_ok:
                cont = cont + 1
    return cont

def evalua_poblacion(poblacion, solucion):
    # Evalua todos los genes de la población.
    adaptacion = []
    for i in range(len(poblacion)):
        adaptacion.append(adaptacion_3sat(poblacion[i], solucion))
    return adaptacion

def seleccion(poblacion, solucion):
    adaptacion = evalua_poblacion(poblacion, solucion)
    # Suma de todas las puntuaciones
    total = 0
    for i in range(len(adaptacion)):
        total = total + adaptacion[i]
    # Tomar dos elementos
    val1 = random.randint(0,total)
    val2 = random.randint(0,total)
    sum_sel = 0
    for i in range (len(adaptacion)):
        sum_sel = sum_sel + adaptacion[i]
        if sum_sel >= val1:
            gen1 = poblacion[i]
            break
    sum_sel = 0
    for i in range(len(adaptacion)):
        sum_sel = sum_sel + adaptacion[i]
        if sum_sel >= val2:
            gen2 = poblacion[i]
            break
    return gen1, gen2

def cruce(gen1, gen2):
    # Cruza 2 genes y obtiene 2 descendientes
    nuevo_gen1 = []
    nuevo_gen2 = []
    corte = random.randint(0,len(gen1))
    nuevo_gen1[0:corte] = gen1[0:corte]
    nuevo_gen1[corte:] = gen2[corte:]
    nuevo_gen2[0:corte] = gen2[0:corte]
    nuevo_gen2[corte:] = gen1[corte:]
    return nuevo_gen1, nuevo_gen2

def mutacion(prob, gen):
    # Muta Gen con una probabilidad prob.
    if random.random() < prob:
        cromosoma = random.randint(0, len(gen) - 1)
        if gen[cromosoma] == 0:
            gen[cromosoma] = 1
        else:
            gen[cromosoma] = 0
    return gen

def elimina_peores_genes(poblacion, solucion):
    # Elimina los dos peores genes
    adaptacion = evalua_poblacion(poblacion, solucion)
    indices_peores = sorted(range(len(adaptacion)), key=lambda k: adaptacion[k])[:2]
    indices_peores.reverse()

    for i in indices_peores:
        if i < len(poblacion):
            del poblacion[i]
        if i < len(adaptacion):
            del adaptacion[i]

def mejor_gen(poblacion, solucion):
    # Devuelve el mejor gen de la población
    adaptacion = evalua_poblacion(poblacion, solucion)
    return poblacion[adaptacion.index(max(adaptacion))]

def algoritmo_genetico(max_iter, max_poblacion, num_vars):
    fin = False
    solucion = poblacion_inicial(1, num_vars)[0]
    poblacion = poblacion_inicial(max_poblacion, num_vars)

    iteraciones = 0
    while not fin:
        iteraciones = iteraciones + 1
        for i in range((len(poblacion))//2):
            gen1, gen2 = seleccion(poblacion, solucion)
            nuevo_gen1, nuevo_gen2 = cruce(gen1, gen2)
            nuevo_gen1 = mutacion(0.1, nuevo_gen1)
            nuevo_gen2 = mutacion(0.1, nuevo_gen2)
            poblacion.append(nuevo_gen1)
            poblacion.append(nuevo_gen2)
            elimina_peores_genes(poblacion, solucion)

        if (max_iter < iteraciones):
            fin = True

    mejor = mejor_gen(poblacion, solucion)
    adaptacion_mejor = adaptacion_3sat(mejor, solucion)
    return mejor, adaptacion_mejor

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        max_iter = int(request.form['max_iter'])
        max_poblacion = int(request.form['max_poblacion'])
        num_vars = int(request.form['num_vars'])
        random.seed()

        mejor_gen_resultado = algoritmo_genetico(max_iter, max_poblacion, num_vars)
        print("Mejor gen Encontrado: " + str(mejor_gen_resultado[0]))
        print("Función de adaptación: " + str(mejor_gen_resultado[1]))
        mejor_gen = str(mejor_gen_resultado[0])
        funcion_adaptacion = str(mejor_gen_resultado[1])
        return render_template("index.html", resultado=mejor_gen, funcion=funcion_adaptacion)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)