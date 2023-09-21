import { useState } from 'react';
import styles from './Inicio.module.css';
import InicioForm from '../InicioForm/InicioForm';
import Popup from '../Popup/Popup';

const onCreateUser = (data) => {
  if(data.user == '') {
    return (
      alert("Please enter a username!")
    );
  }
  else {
    return (
      alert(`${data.user}`)
    );
  }
}

const Inicio = () => {
  const [open, setOpen] = useState(false);
  
  return (
    <>
      <div className={styles.page}>
        <div className={styles.sqcenter}>
          <button onClick={() => setOpen(true)}>Reglas</button>
          {open ? <Popup title="Reglas" text=" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut at libero at enim euismod feugiat. Cras pretium, urna eu viverra faucibus, ipsum urna eleifend sem, non ultricies mi tortor et felis. Vivamus auctor ex eget faucibus tristique. Nulla sollicitudin leo urna, eget varius lorem vulputate eu. Nulla facilisi. Phasellus tincidunt non velit et iaculis. Vivamus eget dui id lectus ultricies bibendum. Suspendisse pharetra vehicula consectetur. Ut nulla nulla, viverra eu turpis eget, fermentum euismod lacus. Quisque dapibus nisl ut sem pharetra ultrices. Aliquam erat metus, mollis quis fringilla eu, sagittis vitae nisl.

Cras at dolor id ipsum euismod bibendum quis nec ex. Morbi fermentum magna ac eleifend iaculis. Proin orci velit, congue in bibendum in, imperdiet sit amet mauris. Phasellus nec vehicula leo. Curabitur dolor ante, mollis vitae ultrices eu, scelerisque eget justo. Vestibulum sed vehicula mauris. Sed et magna hendrerit, volutpat neque ac, pellentesque purus. Sed a consequat lectus. Sed sed pretium nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Curabitur viverra in orci nec congue. In at risus est. Phasellus ut vehicula felis. Nunc id ultrices tortor. Pellentesque in massa auctor, tincidunt orci in, convallis neque.

Nunc pellentesque gravida dapibus. Proin porta feugiat ligula quis scelerisque. Duis ante sem, scelerisque non feugiat vitae, vulputate ut ante. Donec suscipit magna in vulputate maximus. Sed consequat nibh mi, vel pellentesque erat vestibulum ut. Cras fringilla quam vitae fermentum pharetra. Suspendisse potenti. Morbi faucibus rutrum tortor ut mollis. Donec ut bibendum magna. Cras ultrices tristique mauris, non lobortis sem laoreet ultricies. Aenean lacinia massa quis volutpat commodo. Maecenas vulputate velit eu dictum mattis. Nam nec ipsum nec massa pulvinar pharetra. Duis convallis turpis sapien, nec tincidunt lectus facilisis sit amet. Sed nec luctus sapien, eu hendrerit lorem.

Aliquam a justo odio. Integer egestas finibus ullamcorper. Phasellus faucibus orci eu urna accumsan scelerisque. Fusce a fringilla odio. Duis viverra nec neque et placerat. Curabitur volutpat mattis velit non iaculis. Fusce quis lacus sit amet ante tempor laoreet. Nullam id luctus orci. In eget ex posuere diam suscipit sodales at quis erat. Praesent imperdiet mauris in mi imperdiet porta. Integer nunc ante, hendrerit sit amet dui nec, mollis sagittis urna. In hac habitasse platea dictumst. " closePopup={() => setOpen(false)}/> : null}
          <InicioForm onCreateUser={onCreateUser} />
        </div>
      </div> 
    </>
  )
};

export default Inicio;