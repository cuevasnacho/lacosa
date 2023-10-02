import Mesa from '../Mesa/Mesa.jsx';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Diccionario from '../Carta/Diccionario.jsx';
import styles from './Partida.module.css';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { httpRequest } from '../../services/HttpService.js';

const Partida = function () {
  const USERNAME = JSON.parse(localStorage.getItem('username'));
  const USERID = JSON.parse(localStorage.getItem('user_id'));

  const navigate = useNavigate();

  const volverHome = () => {
    navigate('/home');
  }

  const levantarCarta = async () => {
    try {
      const response = await httpRequest({
        method: 'POST',
        service: 'levantar',
        payload: USERID
      });
      
      mycards = JSON.parse(localStorage.getItem('cards'));
      mycards.push(response.id_carta);
      window.localStorage.setItem('cards', JSON.stringify(mycards));

      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const descartar = async () => {
    try {
      const response = await httpRequest({
        method: 'POST',
        service: 'carta/descartar/' + USERID, // CARDID
      });
      
      mycards = JSON.parse(response.cards);
      window.localStorage.setItem('cards', JSON.stringify(mycards));

      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const jugarCarta = async () => {
    try {
      const response = await httpRequest({
        method: 'POST',
        service: 'carta/descartar/' + USERID, // CARDID
      });
      
      mycards = JSON.parse(response.cards);
      window.localStorage.setItem('cards', JSON.stringify(mycards));

      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const cartas = ["analisis", "lacosa", "lanzallamas", "misteriosa"];

  return (
    <div className={styles.container}>
      <div className={styles.manojugador}>
        <ManoJugador cartas={cartas} />
      </div>
      <div className={styles.mazos}>
        <button type='button' onClick={levantarCarta}/>
        <Carta carta="analisis" />
      </div>
      <div className={styles.jugadores}>

      </div>
    </div>
  )
}

export default Partida;