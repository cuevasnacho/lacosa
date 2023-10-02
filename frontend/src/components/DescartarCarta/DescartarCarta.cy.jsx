import React from 'react'
import DescartarCarta from './DescartarCarta'
import ManoJugador from '../ManoJugador/ManoJugador'
import lacosa from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/lacosa.png'
import cuerdas_podridas from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/panico/cuerdas_podridas.png'


describe('<DescartarCarta />', () => {
  const mano = <ManoJugador cartas={[lacosa, cuerdas_podridas]} />
  let descarte = cuerdas_podridas;
  
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<DescartarCarta ComponenteMano={mano} nombreCarta={descarte}/>)
  })
})