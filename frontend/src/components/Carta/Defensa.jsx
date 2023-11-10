import {  useEffect, useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { httpRequest } from '../../services/HttpService';
import { getHand } from '../Partida/functions';
import CustomButton from '../Boton/CustomButton';

function Defensa({dataSocket, manoJugador, setManoJugador, socket})
{
    const defense_card_list = dataSocket.card_to_defend;
    const attacker = dataSocket.attacker_id;
    const attack_card_name = dataSocket.attack_card_name;

    const [modal, setModal] = useState(false);
    const toggle = () => setModal(!modal);

    const backdrop = false;
    
    const defensor_id = parseInt(window.sessionStorage.getItem('user_id'));

    useEffect(() => {
        toggle();
    }, []);

    async function handle_defensa(defenseCardName, attacker_id, manoJugador)
    {
        const defenseCardId = get_defense_card_id(defenseCardName, manoJugador);
        
        if (defenseCardId === null) {
            alert("Hubo un error al obtener el id de la carta de defensa");
        }
        try 
        {
            await httpRequest({
                method: 'POST',
                service: `defensa/${defenseCardId}/${defensor_id}/${attacker_id}/0`
            });  
            getHand(setManoJugador);
            toggle();
        } 
        catch (error) 
        {
            alert(JSON.stringify(error));
            //no_defense();
            toggle();
        }

    }

    function get_defense_card_id(defenseCardName, manoJugador) {
        const foundCard = manoJugador.find(card => card.cartaNombre === defenseCardName);
        return foundCard.id;
    }
      

    function no_defense() {
        const mensaje_no_defense = JSON.stringify({
            action: 'no_defense', 
            data: {defensor_id: defensor_id, 
                    attack_card_name: attack_card_name}});
                    
        socket.send(mensaje_no_defense);
        toggle();
    }

    return(
        <>
        <Modal isOpen={modal} toggle={toggle} backdrop={backdrop} onExit={no_defense} centered >
            <ModalHeader toggle={toggle}> Defensa</ModalHeader>
            <ModalBody>
                Has sido atacado con {attack_card_name}, te podés defender con:
                <ul>
                    {defense_card_list.map((card, index) => (
                        <li key={index}>
                            {card}
                            <CustomButton onClick={() => handle_defensa(card, attacker, manoJugador)} label={'Usar'}/>
                        </li>))}
                </ul>
            </ModalBody>
            <ModalFooter>
                <CustomButton label={'No Defenderse'} onClick={no_defense}/>
            </ModalFooter>
        </Modal></>
    );
}

export default Defensa;