import {  useEffect, useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { httpRequest } from '../../services/HttpService';
import { getHand } from '../Partida/functions';
import CustomButton from '../Boton/CustomButton';

function Defensa({dataSocket, manoJugador, setManoJugador, socket})
{
    console.log(dataSocket);
    const defense_card_list = dataSocket.card_to_defend;
    console.log('Cartas para defenderse: '+ defense_card_list);
    const attacker = dataSocket.attacker_id;
    console.log('atacante: '+ attacker);
    const attack_card_name = dataSocket.attack_card_name;

    const [modal, setModal] = useState(false);
    const toggle = () => setModal(!modal);

    const backdrop = false;
    
    const defensor_id = window.sessionStorage.getItem('user_id');

    useEffect(() => {
        toggle();
    }, []);

    async function handle_defensa(defenseCardName, attacker_id)
    {
        const defenseCardId = get_defense_card_id(defenseCardName, manoJugador);
        console.log('defenseCardId:' + defenseCardId);
        console.log('attacker:' + attacker_id);
        
        if (defenseCardId === null) {
            alert("Hubo un error al obtener el id de la carta de defensa");
        }

        await httpRequest({
            method: 'POST',
            service: `defensa/${defenseCardId}/${defensor_id}/${attacker_id}`
        });

        getHand(setManoJugador);
        toggle();
    }

    function get_defense_card_id(defenseCardName, manoJugador) {
        for (const card of manoJugador) {
            console.log('cardName: ' + card.cardName)
            if (card.cardName === defenseCardName) {
                return card.id;
            }
        }
    }

    function no_defense() {
        const mensaje_no_defense = JSON.stringify({
            action: 'no_defense', 
            data: {defensor_id: defensor_id, 
                    attack_card_name: attack_card_name}});
                    
        socket.send(mensaje_no_defense);
        toggle();
    }

    //<CustomButton label={'Defenderse'} onClick={toggle}></CustomButton>
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
                            <CustomButton onClick={() => handle_defensa(card, attacker)} label={'Usar'}/>
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