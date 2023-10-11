import { httpRequest } from "../..//services/HttpService";

export async function robarCarta(mano, actualizarMano)
{
    const response = await httpRequest('GET', '/cartas/robar');
    const nuevaCarta = {cartaNombre: 'aterrador', id: 1, tipo: 0};
    const manoNueva = [...mano, nuevaCarta];
    actualizarMano(manoNueva);
}