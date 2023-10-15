function sortPlayers(jugadores) {
    const sortedPlayers = jugadores.sort((a,b) => a.position - b.position);
    return sortedPlayers;
}

export { sortPlayers };
