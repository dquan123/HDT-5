#Librerias
import simpy
import random
import statistics
import matplotlib.pyplot as plt

#Función que simula el proceso
def proceso(env, nombre, RAM, cpu, CPUVelocidad, tiempos):
    llegada = env.now #Se registra el momento de llegada
    mem_requerida = random.randint(1, 10) #Se genera aleatoriamente la cantidad de memoria requerida
    yield RAM.get(mem_requerida) #Se solicita la cantidad de memoria requerida del contenedor (yield se usa para que espere hasta que haya suficiente memoria)
    instrucciones = random.randint(1, 10) #Se genera un número aleatorio de instrucciones
    while instrucciones > 0: #Ciclo que se recorre mientra aún hayan instrucciones por ejecutar
        with cpu.request() as req: #El proceso solicita acceso al CPU para que se libere el recurso al completarse la instrucción
            yield req #Se espera hasta que haya suficiente memoria
            yield env.timeout(1) #Se simula un quantum de una unidad de tiempo
            ejecutadas = min(CPUVelocidad, instrucciones) #Se ejecutan las instrucciones hasta la velocidad del CPU, si quedan menos se ejecutan todas
            instrucciones -= ejecutadas #Se restan las instrucciones que ya fueron ejecutadas
            if instrucciones > 0: #Si aún quedan instrucciones por ejecutarse
                decision = random.randint(1, 21) #Se decide aleatoriamente si realiza una operación I/O o regresa a la cola del CPU
                if decision == 1: #Si se realiza una operación I/O
                    yield env.timeout(1) #Se simula un quantum de una unidad de tiempo
                else: #Si ya no quedan instrucciones por ejecutarse
                    yield env.timeout(0) #Vuelve a la cola sin retardo adicional
    yield RAM.put(mem_requerida) #Una vex terminado, libera la memoria solicitada
    tiempos.append(env.now - llegada) #Se calcula el tiempo total que el proceso estuvo en el sistema

#Esta función crea los procesos de forma secuencial
def generador_procesos(env, numero_procesos, intervalo_llegada, RAM, cpu, CPUVelocidad, tiempos): #Recibe los parámetros de las estrategias y la cantidad de procesos a ejecutar
    for i in range(numero_procesos): #Se recorre un ciclo para la cantidad de procesos (ya que se va simulando 1 por 1)
        env.process(proceso(env, f"Proceso_{i}", RAM, cpu, CPUVelocidad, tiempos)) #Se crea un nuevo proceso pasándole los parámetros necesarios para cada iteración del ciclo
        yield env.timeout(random.expovariate(1.0/intervalo_llegada)) #Luego de que se calculó el tiempo, esto hace que se espere ese tiempo antes de crear el siguiente proceso

def simulacion(numero_procesos, intervalo_llegada, tamano_memoria=100, CPUVelocidad=3, cantCPU=1, semilla=42):
    random.seed(semilla) #Se fija la semilla
    env = simpy.Environment() #Se crea el entorno SimPy
    RAM = simpy.Container(env, init=tamano_memoria, capacity=tamano_memoria) #Se define la RAM usando container y con la capacidad igual al tamano de la memoria
    cpu = simpy.Resource(env, capacity=cantCPU) #Se define CPU con su respectiva capacidad usando un Resource
    tiempos = []
    env.process(generador_procesos(env, numero_procesos, intervalo_llegada, RAM, cpu, CPUVelocidad, tiempos)) #Se inicia el generador de procesos
    env.run() #Se ejecuta la simualcion
    promedio = statistics.mean(tiempos) #Se calcula el tiempo promedio
    desviacion = statistics.stdev(tiempos) if len(tiempos) > 1 else 0 #Se calcula la desviacion estandar
    return promedio, desviacion, tiempos #Devuelve promedio, desviacion y tiempos.


#Función para que se ejecuten simulaciones con diferenstes valores de prueba de procesos e intervalos de llegadom graficando los resultados
def experimento_original():
    procesos_lista = [25, 50, 100, 200] #Cantidades de procesos a evaluar de prueba
    intervalos = [10, 5, 1] #Diferentes intervalos de llegada de prueba
    resultados = {} #Diccionario para almacenar los resultados de cada intervalo

    #Ciclo para realizar simulaciones por cada intervalo de llegada
    for intervalo in intervalos:
        resultados[intervalo] = [] #Lista de resultados para cada intervalo

        # Se prueban los distintos valores de procesos en una simulación
        for num in procesos_lista:
            prom, desv, _ = simulacion(num,intervalo) #Se realiza una simulación con el valor de proceso e intervalo actual
            resultados[intervalo].append((num, prom, desv)) #Se guarda en resultados el núemro de procesos actual y los resultados obtenidos
            print(f"Intervalo: {intervalo}, Procesos: {num} -- Tiempo Promedio: {prom:.2f}, Desviación {desv:.2f}") #Mostrar resultados

    #Gráfico de los resultados
    plt.figure(figsize = (8,6))
    #Se obtiene los resultados por cada intervalo de llegada para graficarlos
    for intervalo in intervalos:
        x= [dato[0]  for dato in resultados[intervalo]] #En eje x se grafican los números de procesos
        y= [dato[1] for dato in resultados[intervalo]] #En eje y aparecen los tiempos promedio que duró la simulación
        yerr = [dato[1] for dato in resultados[intervalo]]
        plt.errorbar(x, y, yerr= yerr, marker ="o", capsize = 5, label=f"Intervalo {intervalo}") #Se muestra las desviaciones estandar

    #Etiquetas y título del gráfico
    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo promedio en el sistema")
    plt.title("Simulación original")
    plt.legend()
    plt.grid(True)
    plt.show()
