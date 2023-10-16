import { render } from '@testing-library/react';
import '@testing-library/jest-dom';



test("Aparece el boton de jugar",()=>{
    const component =render(<JugarCarta/>
    );
    component.getByText("Jugar");
})