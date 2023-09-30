import React from "react";

/*

carta = {
    id: 1,
    template: "string"
    tipo: 0,
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