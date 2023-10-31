import { createSlice } from '@reduxjs/toolkit'

export const manoJugadorSlice = createSlice({
    name: 'manoJugador',
    initialState: {
        manoJugador: [],
    },
    reducers: {
        setMano: (state, action) => {
            state.manoJugador = action.payload
        }
    }
})

export const getMano = (state) => state.manoJugador.manoJugador;
export const {setMano} = manoJugadorSlice.actions;
export default manoJugadorSlice.reducer;