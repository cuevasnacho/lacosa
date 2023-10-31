import styles from './LogPartida.module.css';
import { useState } from 'react';

export default function LogPartida({messages}) {
  const [opened, setOpened] = useState(false);
     messages.map((value) =>{
       console.log(value.msj)
     })
    const toggleOpened = () => {
        setOpened(!opened);
    }
  return (
    <>
    <div className={styles.container}>
    { opened ? (
        <>
        <button type='button' className={styles.close_button} onClick={toggleOpened}>X</button>
        <div className={styles.chat_container}>
           <div className={styles.chat}>
            {messages.map((value, index) => {
                return (
                <div key={index} className={styles.my_message_container}>
                  <div className={styles.my_message}>
                    <p className={styles.message}>{value.msj}</p>
                  </div>
              </div>
            )
            })}
           </div>
        </div>
        </>
    ) : (
        <button type='button' className={styles.chat_hidden} onClick={toggleOpened}>Historial de Jugadas</button>
      )}
    </div>
    </>
  )
}

