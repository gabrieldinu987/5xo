/*
    Dimensiunea tablei.
*/

const BOARD_SIZE = 50;


/*
    Containerul în care vom desena tabla.
*/

const boardContainer = document.getElementById("board-container");


/*
    Creează tabla de joc.
*/

function createBoard() {

    /*
        Ștergem conținutul existent.
    */

    boardContainer.innerHTML = "";


    /*
        Creăm toate cele 2500 de celule.
    */

    for (let row = 0; row < BOARD_SIZE; row++) {

        for (let col = 0; col < BOARD_SIZE; col++) {

            const cell = document.createElement("div");

            cell.className = "cell";

            /*
                Salvăm coordonatele.
            */

            cell.dataset.row = row;

            cell.dataset.col = col;

            /*
                Adăugăm celula în tablă.
            */

            boardContainer.appendChild(cell);

        }

    }

}


/*
    Pornirea aplicației.
*/

createBoard();

console.log("5XO loaded.");