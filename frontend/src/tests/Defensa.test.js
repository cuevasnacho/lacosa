import { render, fireEvent, screen, waitFor } from "@testing-library/react";
import Defensa from "../components/Defensa/Defensa";
import get_hand from '../components/Partida/functions'

jest.mock('../services/HttpService.js', () => ({
    httpRequest: jest.fn(),
  }));

jest.mock('../components/Partida/functions', () => ({
    get_hand: jest.fn()
}));

const mockWebSocket = {
    send: jest.fn(),
};

describe("Defensa", () => {
    let dataSocket = {'card_to_defend' : ["nada_de_barbacoas", "aterrador"], 'attacker_id' : 1, 'attack_card_name' : "lanzallamas",'motive': "defensa",
    'attack_card_id': 2};
    const manoJugador = [{cartaNombre: "nada_de_barbacoas", id: 10, tipo: 0}];

    test('Renderiza', () => { 
        render(
            <Defensa 
            dataSocket={dataSocket} 
            manoJugador={manoJugador} 
            setManoJugador={null}
            socket={mockWebSocket}
            setStage={null}
            setJugadas={null}/>
        )
     })

    test('El tamaño de la lista es el mismo que el arreglo de cartas que nos envian', () => { 
        render(
            <Defensa 
            dataSocket={dataSocket} 
            manoJugador={manoJugador} 
            setManoJugador={null}
            socket={null}
            setStage={null}
            setJugadas={null}/>
        )
        const lista_cartas = screen.getAllByTestId("nombreCarta");
        expect(lista_cartas).toHaveLength(dataSocket.card_to_defend.length);
     })

})