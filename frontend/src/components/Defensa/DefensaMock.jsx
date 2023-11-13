import Defensa from "./Defensa";

export function DefensaMock() {
    //data = 
    const dataSocket = {'card_to_defend' : ["nada_de_barbacoas"], 'attacker_id' : 1, 'attack_card_name' : "lanzallamas",'motive': "defensa",
    'attack_card_id': 2};
    const manoJugador = [{cartaNombre: "nada_de_barbacoas", id: 10, tipo: 0}];

    return(
        <Defensa 
        dataSocket={dataSocket} 
        manoJugador={manoJugador} 
        setManoJugador={null}
        socket={null}
        setStage={null}
        setJugadas={null}/>
    )
}