function sortPlayers(jugadores, pos) {
    const sortedPlayers = jugadores.sort((a,b) => a.position - b.position);
    return sortedPlayers;
}

export { sortPlayers };
