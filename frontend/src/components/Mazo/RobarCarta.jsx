import { httpRequest } from "../..//services/HttpService";

export async function robarCarta(mano, actualizarMano)
{
    const user_id = window.sessionStorage.getItem('user_id');
    const response = await httpRequest({
        method: 'POST',
        service: '/card/' + user_id
    });
    //const nuevaCarta = {cartaNombre: response.cartaNombre, id: response.id, tipo: response.tipo};
    //const manoNueva = [...mano, nuevaCarta];
    //actualizarMano(manoNueva);
}