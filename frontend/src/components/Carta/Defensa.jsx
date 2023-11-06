import { useState } from 'react';
import { Modal, ModalHeader, ModalBody, Button } from 'reactstrap';
import { httpRequest } from '../../services/HttpService';

function Defensa(defense_card_list)
{
    const [modal, setModal] = useState(true);
    const toggle = () => setModal(!modal);
    const [defenseCardId, setDefenseCardId] = useState(null);
    const defensor_id = window.sessionStorage.getItem('user_id');

    async function handleDefensa(card, stage, attacker_id)
    {
        if (stage != 4) {
            return null;
        }

        setDefenseCardId(card.id);

        await httpRequest({
            method: 'POST',
            service: `defensa/${defenseCardId}/${defensor_id}/${attacker_id}`
        });
    }

    return(
        <Modal isOpen={modal} toggle={toggle}>
            <ModalHeader toggle={toggle}> Defensa</ModalHeader>
            <ModalBody>
                Has sido atacado, te podes defender con:
                <ul>
                    { defense_card_list.map((card, index) => (
                        <li key={index}>
                            {card.name}
                            <Button onClick={handleDefensa(card)}>
                                Usar
                            </Button>
                        </li>))
                    }
                </ul>
            </ModalBody>
        </Modal>
    );
}

export default Defensa;