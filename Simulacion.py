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

