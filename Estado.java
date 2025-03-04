public class Estado implements Comparable<Estado> {
    public double tiempo;
    public TipoEstado tipo;
    public Proceso proceso;

    public Estado(double tiempo, TipoEstado tipo, Proceso proceso) {
        this.tiempo = tiempo;
        this.tipo = tipo;
        this.proceso = proceso;
    }

    @Override
    public int compareTo(Estado other) {
        return Double.compare(this.tiempo, other.tiempo);
    }
}
