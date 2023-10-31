import { httpRequest } from "../../services/HttpService";

export async function descartarCarta(carta, webSocket) 
{
    const username = window.sessionStorage.getItem('username');
    const match_id = window.sessionStorage.getItem('match_id');
    const playerID = window.sessionStorage.getItem('user_id');
    let manoJugador = useSelector(getMano);

    
    if(carta.cartaNombre === 'lacosa')
        alert(`No puedes descartar ni jugar la carta ${carta.cartaNombre}`);
    else
    {
        try 
        {
            if (manoJugador.length > 4) 
            {
                await httpRequest({
                    method: 'PUT',
                    service: 'carta/descartar/' + playerID + '/' + carta.id,
                });
                
                const nuevaMano = manoJugador.filter(cartaPrevia => cartaPrevia.id !== carta.id);

                nextTurn(match_id, webSocket, username);
            
                return nuevaMano;
            }
            else
            {
                alert("No puedes descartar la carta, ya que no tienes suficientes cartas en la mano");
            }
        } 
        catch (error) 
        {
            alert(error);
        }
    }
}