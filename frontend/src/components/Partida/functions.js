function sortPlayers(jugadores) {
    const sortedPlayers = jugadores.sort((a,b) => a.position - b.position);
    console.log(jugadores);
    console.log(sortedPlayers);
    return sortedPlayers;
}

export { sortPlayers };
