import { httpRequest } from '../../services/HttpService';
import { nextTurn } from '../Partida/functions';
import { useParams } from 'react-router-dom';
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
                    
                    
                    actualizar((manoPrevia) => {
                       return manoPrevia.filter(cartaPrevia => cartaPrevia.id !== carta.id);
                    });

                    const username = window.sessionStorage.getItem('username');
                    const match_id = window.sessionStorage.getItem('match_id');
                    
                    nextTurn(match_id, socket, username);
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

