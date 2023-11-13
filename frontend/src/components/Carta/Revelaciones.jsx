import { useState } from "react";
import { Modal, ModalBody } from 'reactstrap';
import styles from './Revelaciones.module.css';

function Revelaciones({manoJugador, ws, show}) {
  const [modalOpen, setModalOpen] = useState(false);
  const [tieneInfectado, setTieneInfectado] = useState(false);

  function toggleModal() {
    setTieneInfectado(manoJugador.some(card => card.cartaNombre === 'infectado'));
    setModalOpen(show);
  }

  function mostrarInfectado() {
    const mensaje = {
      action: 'show_cards',
      data: {
        card: 'whisky',
        mostrar: 'infectado',
      }
    }
    const respuesta = {
      action: 'revelaciones',
      data: true,
    }
    ws.send(JSON.stringify(respuesta));
    ws.send(JSON.stringify(mensaje));
    setModalOpen(!modalOpen);
  }

  function noMostrar() {
    const respuesta = {
      action: 'revelaciones',
      data: false,
    }
    ws.send(JSON.stringify(respuesta));
    setModalOpen(!modalOpen);
  }

  function mostrarMano() {
    const mensaje = {
      action: 'show_cards',
      data: {
        card: 'whisky',
        mostrar: manoJugador,
      }
    }
    const respuesta = {
      action: 'revelaciones',
      data: {tieneInfectado},
    }
    ws.send(JSON.stringify(mensaje));
    ws.send(JSON.stringify(respuesta));
    setModalOpen(!modalOpen);
  }

  useEffect(() => {
    toggleModal();
  }, [show]);

  return (
    <>
      <div className={styles.modalDiv}>
        <button type='button' onClick={toggleModal}>Abrir Modal</button>
        <Modal isOpen={modalOpen} toggle={toggleModal} backdrop={false} className={styles.modalWindow}>
          <ModalBody className={styles.modalBody}>
            <h4>
              Se jugo una carta de Revelaciones, ¿Desea mostrar su mano?
            </h4>
            <div className={styles.divBotonModal}>
              <button type='button' onClick={mostrarMano} className={styles.botonModal}>Mostrar mano</button>
              <button type='button' onClick={noMostrar} className={styles.botonModal}>No mostrar</button>
              { tieneInfectado && (
              <button
                type='button'
                onClick={mostrarInfectado}
                className={styles.botonModal}>
                  Mostrar infectado
              </button>)}
            </div>
          </ModalBody>
        </Modal>
      </div>
    </>
  );
}

export default Revelaciones;