import React from 'react';
import {useForm} from 'react-hook-form';
import styles from './FormCrearPartida.module.css';
import {httpRequest} from '../../../services/HttpService';
import videobg from '../../../media/videobg.mp4';

function FormCrearPartida() {
  const HOST_ID = parseInt(window.sessionStorage.getItem('user_id'));

  const {
    register,
    handleSubmit,
    formState: {errors},
  } = useForm();
  
  const onSubmit = async (data) => {
    let algonuevo = {
      lobby_name: data.lobby_name,
      lobby_min: parseInt(data.lobby_min),
      lobby_max: parseInt(data.lobby_max),
      player_id: HOST_ID
    }

    try 
    {      
      const response = await httpRequest({
        method: 'POST',
        service: 'lobbys/',
        payload: algonuevo
      });

      window.sessionStorage.setItem('Host', true);
      window.sessionStorage.setItem('Partida', JSON.stringify(data));
      window.sessionStorage.setItem('lobby_id', response.lobby_id);
      
      window.location = `/lobby/${response.lobby_id}`;
      
    } 
    catch (error) 
    {
      console.log(error);
    }
    
  };

  return (
    <>
      <div className={styles.container}>
      <h2 className={styles.titulo}>Formulario de Creación</h2>
        <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
          <div>
            <label>Nombre de la Partida</label>
            <input
              type="text"
              id = "lobby_name"
              {...register('lobby_name', {
                required: {
                  value: true,
                  message: 'Nombre de la partida requerido',
                },
                maxLength: {
                  value: 20,
                  message: 'Nombre de la partida demasiado largo',
                },
                minLength: {
                  value: 4,
                  message: 'Nombre de la partida demasiado corto',
                },
              })}
              placeholder="Nombre de partida"
              autoComplete='off'
              className={styles.input}
            />
            {errors.lobby_name && <p>{errors.lobby_name.message}</p>}
          </div>

          <div>
            <label>Mínimo de Jugadores</label>
            <input
              type="number"
              id = "lobby_min"
              {...register('lobby_min', {
                required: {
                  value: '',
                  message: 'Mínimo de jugadores requerido',
                },
                max: {
                  value: 12,
                  message: 'Mínimo de jugadores demasiado alto',
                },
                min: {
                  value: 4,
                  message: 'Mínimo de jugadores demasiado bajo',
                },
              })}
              placeholder="Ingrese un minimo"
              className={styles.input}
            />
          </div>

          <div>
            <label>Máximo de Jugadores</label>
            <input
              type="number"
              id = "lobby_max"
              {...register('lobby_max', {
                required: {
                  value: null,
                  message: 'Máximo de jugadores requerido',
                },
                max: {
                  value: 12,
                  message: 'Máximo de jugadores demasiado alto',
                },
                min: {
                  value: 4,
                  message: 'Máximo de jugadores demasiado bajo',
                },
              })}
              placeholder="Ingrese un maximo"
              className={styles.input}
            />
          </div>

          <div>
            <label>Contraseña</label>
            <input
              type="password"
              id = "lobby_password"
              {...register('lobby_password', {
                maxLength: {
                  value: 20,
                  message: 'Contraseña demasiado larga',
                },
                minLength: {
                  value: 4,
                  message: 'Contraseña demasiado corta',
                },
              })}
              className={styles.input}
            />
          </div>

          <input type="submit" value="Crear" className={styles.submit}/>
        </form>
        <video src={videobg} type="video/mp4" autoPlay loop muted />
      </div>
    </>
  );
}

export default FormCrearPartida;
