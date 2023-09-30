import React from "react";
/*

carta = {
    id: 1,
    template: "string",
    tipo: True, -> Panico = True - Alejate = False
    imagen: "ruta/a/imagen.jpg"
}

*/
function Carta({carta}) {
    return (
        <div className="carta">
            <div>
                <img src={carta.imagen} />
            </div>
        </div>
    );
}

export default Carta;