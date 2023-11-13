import { useEffect, useState } from 'react';
import { Modal, ModalBody } from 'reactstrap';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import { arrangePlayers, nextTurn, getHand, intercambiarDefensa } from './functions.jsx';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from './Partida.module.css';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Jugadores from '../Jugador/Jugadores.jsx';
import Mazo from '../Mazo/Mazo.jsx';
import MazoDescarte from '../Mazo/MazoDescarte.jsx';
import Chat from '../Chat/Chat.jsx';
import Finalizar from '../FinalizarPartida/Finalizar.jsx';
import LogPartida from '../LogPartida/LogPartida.jsx';

function Partida () {
  const idPlayer = JSON.parse(sessionStorage.getItem('user_id'));
  const username = window.sessionStorage.getItem('username');
  const { idPartida } = useParams();
  const [websocket, setWebsocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [jugadas,setJugadas]=useState([])
  const [jugador,setJugador] = useState({})
  const [stage, setStage] = useState(0);
  const [playerState, setPlayerState] = useState({});
  const [isLaCosa, setIsLaCosa] = useState(false);
  const [socketData, setSocketData] = useState({});
  const [manoJugador, setManoJugador] = useState([]);   // Indica las cartas que tengo en la mano
  const [matchState, setMatchState] = useState([]); // username: string, id: int, esTurno: bool, posicion: int, eliminado: bool	
  const [mazoDescarteState, setMazoDescarteState] = useState(2);  // Dice que carta se va a mostrar en el mazo de descarte
  const [isOver, setIsOver] = useState(false);

  const [modalOpen, setModalOpen] = useState(false);
  const [tieneInfectado, setTieneInfectado] = useState(false);

  function toggleModal() {
    setTieneInfectado(manoJugador.some(card => card.cartaNombre === 'infectado'));
    setModalOpen(!modalOpen);
  }

  function mostrarInfectado() {
    const mensaje = {
      action: 'show_cards',
      data: {
        card: 'whisky',
        mostrar: 'infectado',
      }
    }
    websocket.send(mensaje);
    setModalOpen(!modalOpen);
  }

  function noMostrar() {
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
    websocket.send(mensaje);
    setModalOpen(!modalOpen);
  }

  async function getStatus() {
    const responseStatus = await httpRequest({
      method: 'GET',
      service: `partida/status/${idPartida}/${idPlayer}`,
    });
    const status = responseStatus;
    setJugador(status.jugador)
    console.log({status})
    const jugadores = arrangePlayers(status.jugadores);
    setMatchState(jugadores);
    setPlayerState(status.jugador);
  }

  async function initializeGame() {
    getStatus();
    window.sessionStorage.setItem('match_id', idPartida);
    const cards = await getHand(setManoJugador);
    setIsLaCosa(cards.some(card => card.cartaNombre === 'lacosa'));
  }

  function toastStage(text) {
    toast.info(text, {
      position: toast.POSITION.TOP_LEFT,
    })
  }

  function declarar() {
    websocket.send(JSON.stringify({action: 'end_game', data: true}))
  }
  
  useEffect (() => {
    const url_pasivo = `ws://localhost:8000/ws/match/pasivo/${idPartida}/${idPlayer}`;
    const url_activo = `ws://localhost:8000/ws/match/activo/${idPartida}/${idPlayer}`;
    const ws = new WebSocket(url_pasivo);
    const ws_activo = new WebSocket(url_activo);

    ws.onopen = (event) => {
      initializeGame();
    };
    setWebsocket(ws);

    //funcion agregada (va guardando el historial completo de jugadas)
    const receiveJugada=(jugada)=>setJugadas((state)=>[...state,jugada])
    let jugada="";
    // recieve message every start page
    ws_activo.onmessage = (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'iniciar_turno':
          toastStage(info.action);
          setStage(1);
          break;

        case 'forzar_jugada':
          toastStage(info.action);
          setStage(2);
          break;

        case 'elegir_jugada':
          toastStage(info.action);
          setStage(3);
          break;

        case 'iniciar_defensa':
          toastStage(info.action);
          setStage(4);
          break;

        case 'iniciar_intercambio':
          toastStage(info.action);
          setSocketData(info.data);
          setStage(5);
          break;

        case 'sol_intercambio':
          toastStage(info.action);
          setSocketData(info.data);
          const oponent_id = parseInt(info.data.oponent_id);
          const card_id = parseInt(info.data.card_id);
          setStage(6);

          intercambiarDefensa(oponent_id, card_id)
            .then(canDefend => {
              if (canDefend) {
                // proceso de defensa
              }
              else {
                setStage(7);
              }
            });
          break;

        case 'revelaciones':
          toggleModal();
          break;
        
        case 'fin_turno':
          toastStage(info.action);
          setStage(0);
          nextTurn(idPartida, ws, username);
          break;

        case 'cuarentena':
          toastStage(info.data);
          break;
      }
    };
    
    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'message':
          const message = info.data;
          setMessages([...messages, message]);
          break;
          
        case 'end_game':
          const respuesta = info.data;
          setIsOver(respuesta);
          break;

        case 'play_card':
          const tipo_carta_descartada = info.data.tipo ? 1 : 0;
          setMazoDescarteState(tipo_carta_descartada);
          getStatus();
          toast(`${info.data.player} jugó la carta ${info.data.card} sobre ${info.data.target}`, {theme: 'dark'});
          jugada = {msj:`${info.data.player} jugó la carta ${info.data.card} sobre ${info.data.target}`}
          receiveJugada(jugada)
          let jugadores2=[
            {id:5,right:false,left:true},
            {id:6,right:true,left:false},
            {id:7,right:true,left:true},
            {id:8,right:true,left:true}
          ]
          for (let i = 0; i < jugadores2.length; i++) {
            if(jugadores2[i].id === idPlayer){
              setJugador(jugadores2[i])
            }
          }
          break;

        case 'next_turn':
          getStatus();
          toast(`Finalizo  el turno de ${info.data}`, {theme: 'dark'});
          break;
        
        case 'show_cards':
          const cartas = info.data;
          let mensaje_cartas = "Cartas: ";
          for (let i = 0; i < cartas.length; i++) {
            mensaje_cartas = mensaje_cartas.concat(cartas[i] + ", ");
            console.log(cartas[i]);
          }
          toast(`${mensaje_cartas}`, {theme: 'dark'});
          break;

        case 'notify_defense':
          toast(`Podes defenderte de ${info.data.atacante_username} con ${info.data.card_defense_name}`);
          break;
      }
    };
   
    // clean up function when we close page
    return () => {ws.close(); ws_activo.close();}
  }, [messages,mazoDescarteState]);

  return (
    <div className={styles.container}>
      {isOver && <Finalizar idpartida = {idPartida} idjugador={idPlayer}/>}
      <ToastContainer />
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
      {playerState.esTurno && (<div className={styles.tuTurno}/>)}
      <div className={styles.detalleMesa}>
        { isLaCosa && 
        (<button 
          type='button' 
          onClick={declarar}
          className={styles.botonDeclarar}>
            Declarar
        </button>
        )}
      </div>
      <Mazo stage={stage} mano={manoJugador} actualizarMano={setManoJugador}/>
      <MazoDescarte mazoDescarteState={mazoDescarteState}/>
      <ManoJugador 
        cartas={manoJugador} 
        stage={stage}
        actstage={setStage}
        data={socketData}
        actualizar={setManoJugador} 
        socket={websocket} 
        jugadores={matchState}/>
      <Jugadores jugadores={matchState} jugador={jugador}/>
      <Chat ws={websocket} messages={messages}/>
      <LogPartida messages={jugadas}></LogPartida>
    </div>
  );
}
export default Partida;
