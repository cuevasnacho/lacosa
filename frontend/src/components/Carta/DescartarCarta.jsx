import { httpRequest } from '../../services/HttpService';
import { getHand } from '../Partida/functions';
/*
    actualizar: funcion que actualiza la mano del jugador
    mano: array de cartas que tiene el jugador
    carta: carta que se quiere descartar
*/
export async function descartarCarta(actualizar, mano, carta, socket) 
    {
        if(carta.cartaNombre === 'lacosa')
            alert(`No puedes descartar ni jugar la carta ${carta.cartaNombre}`);
        else
        {
            try 
            {
                if (mano.length > 4) 
                {
                    const playerID = window.sessionStorage.getItem('user_id');
                    
                    await httpRequest({
                        method: 'PUT',
                        service: 'carta/descartar/' + playerID + '/' + carta.id,
                    });
                    getHand(actualizar);
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

