import { configureStore } from '@reduxjs/toolkit'
import manoJugadorReducer from './slices/manoJugadorSlice'
import jugadoresReducer from './slices/jugadoresSlice'
import turnoReducer from './slices/turnoSlice'

export default configureStore({
  reducer: {
    manoJugador: manoJugadorReducer,
    jugadores: jugadoresReducer,
    turno: turnoReducer
  }
})

