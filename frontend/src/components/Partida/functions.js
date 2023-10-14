function mod(i, n) {
    return ((i % n) + n) % n;
}

function normalizePosition (jugador, pos, n) {
    const curr_pos = jugador['position'];
    jugador['position'] = mod(curr_pos - pos, n);
    return jugador;
}

function sortPlayers(jugadores, pos) {
    const normalizedPlayers = jugadores.map(jugador => normalizePosition({ ...jugador }, pos, jugadores.length+1));
    normalizedPlayers.sort((a,b) => a.position - b.position);
    return normalizedPlayers;
}

export { sortPlayers };