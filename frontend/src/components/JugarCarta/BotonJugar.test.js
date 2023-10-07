import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import BotonJugar from './BotonJugar';


test("Aparece el boton de jugar",()=>{
    const component =render(<BotonJugar/>
    );
    component.getByText("Jugar");
})