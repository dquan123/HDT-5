public class Proceso {
    public int id;
    public double tiempoLlegada;
    public int memoria;
    public int cantidadInstrucciones;

    public Proceso(int id, double tiempoLlegada, int memoria, int cantidadInstrucciones) {
        this.id = id;
        this.tiempoLlegada = tiempoLlegada;
        this.memoria = memoria;
        this.cantidadInstrucciones = cantidadInstrucciones;
    }
}
