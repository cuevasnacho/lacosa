import UnirsePartida from "../components/UnirsePartida/UnirsePartida";
import { render, waitFor} from '@testing-library/react';
import '@testing-library/jest-dom';
import TablaFila from "../components/UnirsePartida/TablaFila";

beforeEach(() => {
  global.fetch = jest.fn(() => {
    return Promise.resolve({
      ok: true,
    })
  });
});

describe('Unirse a Partida', () =>{

  jest.mock('../components/UnirsePartida/TablaFila', () => jest.fn());

  test('Renderiza el componente', async () => {
    
    render(<UnirsePartida />);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
    });
    
  });

});