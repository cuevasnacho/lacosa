import { httpRequest } from "../../services/HttpService";
import { ToastContainer, toast } from 'react-toastify';

function Defensa({attack_card_name, attacker_id, defense_card_id, socket}) 
{
    async function play_defense(defense_card_id, attacker_id) 
    {
        const response = await httpRequest({
            method: 'POST',
            service: `defensa/${defense_card_id}/${attacker_id}`,
        });
        
        const attacker_username = response.attacker_username;
        const defensor_username = response.defensor_username;
        const card_name = response.card_name;

        const mensaje = JSON.stringify({action: 'play_defense', data: {
            attacker_username: attacker_username,
            defensor_username: defensor_username,
            card_name: card_name,}});

        socket.send(mensaje);
    }
}