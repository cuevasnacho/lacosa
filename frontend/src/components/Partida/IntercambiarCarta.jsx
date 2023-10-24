import { httpRequest } from "../../services/HttpService";

export async function intercambiar({carta, idJugador, socket}) {
    const response = await httpRequest({
        method: 'GET',
        service: `partida/${idJugador}/next`,
    });
    const id_next_player = response.id_next;

    const mensaje = JSON.stringify({action: 'intercambiar_carta', 
        data: {}})
}