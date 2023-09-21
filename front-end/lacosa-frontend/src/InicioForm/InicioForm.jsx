import { useState } from 'react';
import styles from './InicioForm.module.css';

const InicioForm = ({
  onCreateUser
}) => {
  const [data, setData] = useState({
    user: '',
    id: 0
  });

  return(
    <div className={styles.InicioForm}>
      <h3>INGRESE EL NOMBRE DE SU USUARIO</h3>
      <form className={styles.form}>
        <input 
          type="text"
          placeholder="Usuario"
          value={data.user}
          onChange={(e) => setData({ ...data, user: e.target.value })}
        />
      </form>
      <div className={styles.Buttons}>
        <button onClick={() => onCreateUser(data)}>Ingresar</button>
      </div>
  </div>
  )
};

export default InicioForm;