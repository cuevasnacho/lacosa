import styles from './InicioForm.module.css';
import { httpRequest } from '../../services/HttpService.js';

import { useForm } from 'react-hook-form';
import { useHistory } from 'react-router-dom';

const InicioForm = () => {
  const history = useHistory();
  
  const {
    register,
    handleSubmit,
    formState: {errors},
  } = useForm();

  const onSubmit = async (data) => {
    try {
      const response = await httpRequest({
        method: 'POST',
        service: 'player',
        body: JSON.stringify(data)
      });
      window.sessionStorage.setItem('logged', JSON.stringify({
        user_id: response.id,
        username: response.name,
        ingame: response.ingame,
      }));

      history.push('/main');
    } catch (error) {
      console.log(error);
    }
  };

  return(
    <div className={styles.InicioForm}>
      <h3>INGRESE EL NOMBRE DE SU USUARIO</h3>
      <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
        <input 
          {...register('username', {
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
          })
          }
        />
        <div>
          {errors.username && <p className="text-danger">{errors.username.message}</p>}
        </div>
        <input type="submit" value="Ingresar" className={styles.Buttons}/>
      </form>
  </div>
  )
};

export default InicioForm;