import ManoJugador from '../ManoJugador/ManoJugador'

function DescartarCarta({ComponenteMano, nombreCarta}){
    const manoActual = ComponenteMano.props.cartas;

    const nuevaMano = manoActual.filter(carta => carta !== nombreCarta);

    return(
        <ManoJugador cartas={nuevaMano} />
    );
}

export default DescartarCarta;