import ManoJugador from '../ManoJugador/ManoJugador'

function DescartarCarta({cartas, nombreCarta}){
    const manoActual = cartas;

    const nuevaMano = manoActual.filter(carta => carta !== nombreCarta);

    return(
        <ManoJugador cartas={nuevaMano} />
    );
}

export default DescartarCarta;