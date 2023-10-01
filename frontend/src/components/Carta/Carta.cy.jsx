import React from 'react'
import Carta from './Carta'
import analisis from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/analisis.png'

describe('<Carta />', () => {
  const carta_analisis = {
    id: 1,
    template: 'string',
    tipo: 0,
    ubicacion: 'mano',
    imagen: analisis,
  };

  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<Carta carta={carta_analisis}/>)
  })
})