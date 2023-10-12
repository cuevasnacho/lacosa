import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import Finalizar from './Finalizar';
import { BrowserRouter as Router} from 'react-router-dom';


test("Mostrar 4 jugadores no repetidos con exito",()=>{
    const jugadoresDB={
        "jugadores":[
            {
                nombre_jugador:"LionelMessi",
                equipo:"Humano"
            },
            {
                nombre_jugador:"elbicho",
                equipo:"Humano"
            },
            {
                nombre_jugador:"elcelebro",
                equipo:"Humano"
            },
            {
                nombre_jugador:"bichiFuerte",
                equipo:"Humano"
            }
        ],
        "ganador":"Humanos"
    }
    const component = render(<Router>
        <Finalizar jugadoresDB={jugadoresDB}/>
    </Router>);
    component.getByText("Victoria para los Humanos")
    component.getByText("LionelMessi")
    component.getByText("elbicho")
    component.getByText("elcelebro")
    component.getByText("bichiFuerte")
    component.getAllByText("Humano")
})