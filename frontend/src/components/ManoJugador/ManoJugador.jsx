import Carta from '../Carta/Carta.jsx'
import style from './ManoJugador.module.css'

function ManoJugador({cartas}) {
    return (
        <div className={style.ManoJugador}>
            {cartas.map((carta, index) => (
                <Carta key={index} carta={carta} />
            ))}
        </div>
    );
}

export default ManoJugador;