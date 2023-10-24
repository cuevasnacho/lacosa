import React from "react";
import { render } from "@testing-library/react";
import Carta from "../components/Carta/Carta";

const props = {
  carta: { cartaNombre: "analisis", tipo: 0, id: 4 },
  esTurno: true,
  actualizar: jest.fn(),
  mano: [],
  socket: jest.fn(),
  jugadores: [
    { username: "user1", esTurno: true, eliminado: false },
    { username: "user2", esTurno: false, eliminado: false },
    { username: "user3", esTurno: false, eliminado: false },
    { username: "user4", esTurno: false, eliminado: false },
  ],
};

it("renders without crashing", function () {
  render(<Carta {...props}/>);
});
