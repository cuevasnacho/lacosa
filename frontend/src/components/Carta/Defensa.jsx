import {  useEffect, useState } from 'react';
import { Modal, ModalHeader, ModalBody, Button, ModalFooter } from 'reactstrap';
import { httpRequest } from '../../services/HttpService';
import { getHand } from '../Partida/functions';

function Defensa({dataSocket, manoJugador, stage, setManoJugador, socket})
{
    const defense_card_list = dataSocket.card_to_defend;
    const attacker = dataSocket.attacker_id;
    const attack_card_name = dataSocket.atack_card_name;

    const [modal, setModal] = useState(true);
    const toggle = () => setModal(!modal);

    const backdrop = false;
    
    const defensor_id = window.sessionStorage.getItem('user_id');
    let defenseCardId = null;

    useEffect(() => {
        if (stage === 4) {
            toggle();
        }
    }, []);

    async function handleDefensa(defenseCardName, attacker_id)
    {
        defenseCardId = getDefenseCardId(defenseCardName, manoJugador);
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

    function getDefenseCardId(defenseCardName, manoJugador) {
        for (const card of manoJugador) {
            if (card.cardName === defenseCardName) {
                return card.id;
            }
        }
    }

    function noDefense() {
        const mensaje_no_defense = JSON.stringify({
            action: 'no_defense', 
            data: {defensor_id: defensor_id, 
                    attack_card_name: attack_card_name}});
                    
        socket.send(mensaje_no_defense);
        toggle();
    }

    return(
        <>
        <Modal isOpen={modal} toggle={toggle} backdrop={backdrop} onExit={noDefense} >
            <ModalHeader toggle={toggle}> Defensa</ModalHeader>
            <ModalBody>
                Has sido atacado con {attack_card_name}, te podés defender con:
                <ul>
                    {defense_card_list.map((card, index) => (
                        <li key={index}>
                            {card}
                            <Button onClick={() => handleDefensa(card, attacker)}>
                                Usar
                            </Button>
                        </li>))}
                </ul>
            </ModalBody>
            <ModalFooter>
                <Button color='secondary' onClick={noDefense}>
                    No defenderse
                </Button>
            </ModalFooter>
        </Modal></>
    );
}

export default Defensa;