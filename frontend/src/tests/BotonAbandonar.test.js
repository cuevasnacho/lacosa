import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import BotonAbandonar from './BotonAbandonar';

test("Mostrar el boton",()=>{
    const component=render(<BotonAbandonar/>);
    component.findByText("Abandonar");
})