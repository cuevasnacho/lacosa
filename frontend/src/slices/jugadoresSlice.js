import { createSlice } from '@reduxjs/toolkit'

export const jugadoresSlice = createSlice({
    name: 'jugadores',
    initialState: {
        jugadores: [],
    },
    reducers: {
        setJugadores: (state, action) => {
            state.jugadores = action.payload
        }
    }
})
export const getJugadores = (state) => state.jugadores.jugadores;
export const {setJugadores} = jugadoresSlice.actions;
export default jugadoresSlice.reducer;