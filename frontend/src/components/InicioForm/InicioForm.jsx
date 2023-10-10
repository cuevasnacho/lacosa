import styles from './InicioForm.module.css';
import { httpRequest } from '../../services/HttpService.js';

import { useForm } from 'react-hook-form';
//import { useNavigate } from 'react-router-dom';


const InicioForm = () => {
  const {
    register,
    handleSubmit,
    formState: {errors},
  } = useForm();
  
  const onSubmit = async (data) => {
    try {
      // Log the data before sending the POST request
      console.log('Data to be sent:', data);
      
      const response = await httpRequest({
        method: 'POST',
        service: 'players/',
        payload: data
      });
      
      window.sessionStorage.setItem('user_id', response.player_id);
      window.sessionStorage.setItem('username', response.player_name);
      window.sessionStorage.setItem('Host', false);
      
      window.location = '/home';

    } catch (error) {
      console.log(error);
    }
  };

  return(
    <div className={styles.InicioForm}>
      <h3>INGRESE EL NOMBRE DE SU USUARIO</h3>
      <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
        <input 
          className={styles.userinput}
          {...register('player_name', {
            required: { value: true, message: 'Debes ingresar un nombre!' },
            validate: {
              value: (value) => {
                if (value !== 'sistema' && value !== '') {
                  return true;
                }
                alert(`Tu nombre no puede ser ${value}`);
                return false;
              },
            },
            maxLength: { value: 20, message: '20 caracteres máximo' },
          })}
          data-testid="player_name"
        />
        <div>
          {errors.player_name && <p className={styles.textdanger}>{errors.player_name.message}</p>}
        </div>
        <input type="submit" value="Ingresar" className={styles.Buttons}/>
      </form>
  </div>
  )
};

export default InicioForm;
