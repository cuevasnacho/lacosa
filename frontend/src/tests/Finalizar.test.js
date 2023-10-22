import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter as Router} from 'react-router-dom';
import Finalizar from '../components/FinalizarPartida/Finalizar';

test("Mostrando boton y titulo",()=>{
 const component=render(<Router>
    <Finalizar/>
  </Router>);
  component.findByText('Volver Inicio');
})

