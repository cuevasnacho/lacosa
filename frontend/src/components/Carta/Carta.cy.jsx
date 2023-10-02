import React from 'react'
import Carta from './Carta'
import Diccionario from './Diccionario'

describe('<Carta />', () => {
  const carta = Diccionario['lacosa'];

  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<Carta carta={carta}/>)
  })
})