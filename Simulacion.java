import java.util.*;

public class Simulacion {
    double tiempoActual = 0;
    int memoria;
    int tamanoMemoria;
    int CPUVelocidad;
    int cantCPU;
    int CPUDisp;
    PriorityQueue<Estado> colaEventos;
    Queue<Proceso> colaEsperaMemoria;
    Queue<Proceso> colaEsperaCPU;
    ArrayList<Double> tiemposTotales;
    Random rand;
    
    int numeroProcesos;
    double intervaloLlegada;
    
    public Simulacion(int numeroProcesos, double intervaloLlegada, int tamanoMemoria, int CPUVelocidad, int cantCPU, long semilla) {
        this.numeroProcesos = numeroProcesos;
        this.intervaloLlegada = intervaloLlegada;
        this.tamanoMemoria = tamanoMemoria;
        this.CPUVelocidad = CPUVelocidad;
        this.cantCPU = cantCPU;
        this.memoria = tamanoMemoria;
        this.CPUDisp = cantCPU;
        this.colaEventos = new PriorityQueue<>();
        this.colaEsperaMemoria = new LinkedList<>();
        this.colaEsperaCPU = new LinkedList<>();
        this.tiemposTotales = new ArrayList<>();
        this.rand = new Random(semilla);
    }
    
    private double generarExponencial(double media) {
        return -media * Math.log(1 - rand.nextDouble());
    }
    
    private void programarEvento(Estado evento) {
        colaEventos.add(evento);
    }
    
    public void correrSimulacion() {
        double tiempo = 0;
        for (int i = 0; i < numeroProcesos; i++) {
            tiempo += generarExponencial(intervaloLlegada);
            int memRequerida = rand.nextInt(10) + 1;
            int instrucciones = rand.nextInt(10) + 1;
            Proceso p = new Proceso(i, tiempo, memRequerida, instrucciones);
            programarEvento(new Estado(tiempo, TipoEstado.LLEGADA, p));
        }
        while (!colaEventos.isEmpty()) {
            Estado evento = colaEventos.poll();
            tiempoActual = evento.tiempo;
            procesarEvento(evento);
        }
    }
    
    private void procesarEvento(Estado evento) {
        Proceso p = evento.proceso;
        switch (evento.tipo) {
            case LLEGADA:
                if (memoria >= p.memoria) {
                    memoria -= p.memoria;
                    programarEvento(new Estado(tiempoActual, TipoEstado.INICIO_CPU, p));
                } else {
                    colaEsperaMemoria.add(p);
                }
                break;
            case INICIO_CPU:
                if (CPUDisp > 0) {
                    CPUDisp--;
                    programarEvento(new Estado(tiempoActual + 1, TipoEstado.FIN_CPU, p));
                } else {
                    colaEsperaCPU.add(p);
                }
                break;
            case FIN_CPU:
                int ejecutadas = Math.min(CPUVelocidad, p.cantidadInstrucciones);
                p.cantidadInstrucciones -= ejecutadas;
                CPUDisp++;
                if (!colaEsperaCPU.isEmpty()) {
                    Proceso siguiente = colaEsperaCPU.poll();
                    programarEvento(new Estado(tiempoActual, TipoEstado.INICIO_CPU, siguiente));
                }
                if (p.cantidadInstrucciones <= 0) {
                    memoria += p.memoria;
                    tiemposTotales.add(tiempoActual - p.tiempoLlegada);
                    Iterator<Proceso> iter = colaEsperaMemoria.iterator();
                    while (iter.hasNext()) {
                        Proceso esperando = iter.next();
                        if (memoria >= esperando.memoria) {
                            memoria -= esperando.memoria;
                            iter.remove();
                            programarEvento(new Estado(tiempoActual, TipoEstado.INICIO_CPU, esperando));
                        }
                    }
                } else {
                    int decision = rand.nextInt(21) + 1;
                    if (decision == 1) {
                        programarEvento(new Estado(tiempoActual + 1, TipoEstado.FIN_WAITING, p));
                    } else {
                        programarEvento(new Estado(tiempoActual, TipoEstado.INICIO_CPU, p));
                    }
                }
                break;
            case FIN_WAITING:
                programarEvento(new Estado(tiempoActual, TipoEstado.INICIO_CPU, p));
                break;
        }
    }
    
    public double getTiempoPromedio() {
        double suma = 0;
        for (double t : tiemposTotales) {
            suma += t;
        }
        return tiemposTotales.size() > 0 ? suma / tiemposTotales.size() : 0;
    }
    
    public double getDesviacion() {
        double media = getTiempoPromedio();
        double suma = 0;
        for (double t : tiemposTotales) {
            suma += (t - media) * (t - media);
        }
        return tiemposTotales.size() > 1 ? Math.sqrt(suma / (tiemposTotales.size() - 1)) : 0;
    }
}
