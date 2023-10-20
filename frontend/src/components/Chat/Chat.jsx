import styles from './Chat.module.css';
import { useState } from 'react';

const Chat = ({ws, messages}) => {
  const [message, setMessage] = useState([]);
  const [opened, setOpened] = useState(false);

  const user_id = parseInt(window.sessionStorage.getItem('user_id'));
  const username = window.sessionStorage.getItem('username');

  const sendMessage = () => {
    const message_parse = {action: 'message', data: {id: user_id, username: username, mensaje: message}};
    ws.send(JSON.stringify(message_parse));
    setMessage([]);
  };

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
              if (value.id === user_id) {
                return (
                  <div key={index} className={styles.my_message_container}>
                    <div className={styles.my_message}>
                      <p className={styles.client}>{value.username}</p>
                      <p className={styles.message}>{value.mensaje}</p>
                    </div>
                  </div>
                );
              } else {
                return (
                  <div key={index} className={styles.another_message_container}>
                    <div className={styles.another_message}>
                      <p className={styles.client}>{value.username}</p>
                      <p className={styles.message}>{value.mensaje}</p>
                    </div>
                  </div>
                );
              }
            })}
          </div>
          <div className={styles.input_chat_container}>
            <input
              className={styles.input_chat}
              type="text"
              placeholder="Escriba su mensaje..."
              onChange={(e) => setMessage(e.target.value)}
              value={message}
            ></input>
            <button className={styles.submit_chat} onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
        </>
      ) : (
        <button type='button' className={styles.chat_hidden} onClick={toggleOpened}>Chat</button>
      )}
      </div>
    </>
  );
}

export default Chat;

/* 
<div className={styles.input_chat_container}>
            <input
              className={styles.input_chat}
              type="text"
              placeholder="Chat message ..."
            />
            <button className={styles.submit_chat}>
              Send
            </button>
          </div>
          */