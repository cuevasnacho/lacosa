import styles from './Popup.module.css';

const Popup = ({title, text, closePopup}) => {
  return (
    <div className={styles.popupcontainer}>
      <button className={styles.closeRules} onClick={closePopup}>X</button>
      <div className={styles.popupbody}>
        <h1>{title}</h1>
        <p>{text}</p>
      </div>
    </div>
  )
};

export default Popup;