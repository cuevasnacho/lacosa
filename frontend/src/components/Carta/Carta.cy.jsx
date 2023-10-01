import React from 'react'
import Carta from './Carta'
import analisis from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/analisis.png'

describe('<Carta />', () => {

  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<Carta carta={analisis}/>)
  })
})