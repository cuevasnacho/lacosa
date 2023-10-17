import styles from './MazoDescarte.module.css';

function MazoDescarte ({mazoDescarteState}) {
  const mazoState = `${styles.mazoDescarte} ${styles[`mazoDescarteState${mazoDescarteState}`]}`;

  return (
    <button
      className={mazoState}
      type='button'
    />
  );
}

export default MazoDescarte;