import React from 'react'
import Jugador from './Jugador'

describe('<Jugador />', () => {
  it('renders', () => {
    const params = {
      username: "Juaen",
      esTurno: false
    }
    // see: https://on.cypress.io/mounting-react
    cy.mount(<Jugador username={params.username} esTurno={params.esTurno}/>)
  })
})