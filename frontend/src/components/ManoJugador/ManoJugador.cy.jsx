import React from 'react'
import ManoJugador from './ManoJugador'
import lacosa from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/lacosa.png'
import cuerdas_podridas from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/panico/cuerdas_podridas.png'

const test_cartas = [lacosa, cuerdas_podridas, lacosa, cuerdas_podridas];

describe('<ManoJugador />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<ManoJugador cartas={test_cartas}/>)
  })
})