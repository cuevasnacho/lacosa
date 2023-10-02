import React from 'react'
import ManoJugador from './ManoJugador'


const test_cartas = [lacosa, cuerdas_podridas, lacosa, cuerdas_podridas];

describe('<ManoJugador />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<ManoJugador cartas={test_cartas}/>)
  })
})