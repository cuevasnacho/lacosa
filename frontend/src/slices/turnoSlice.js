import { createSlice } from '@reduxjs/toolkit'

export const turnoSlice = createSlice({
    name: 'turno',
    initialState: {
        turno: null,
    },
    reducers: {
        setTurno: (state, action) => {
            state.turno = action.payload
        }
    }
})

export const getTurno = (state) => state.turno.turno;
export const {setTurno} = turnoSlice.actions;
export default turnoSlice.reducer;