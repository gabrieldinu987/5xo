const BOARD_SIZE = 50;

const board = document.getElementById("board-container");

function createBoard() {

    board.innerHTML = "";

    for (let row = 0; row < BOARD_SIZE; row++) {

        for (let col = 0; col < BOARD_SIZE; col++) {

            const cell = document.createElement("div");

            cell.className = "cell";

            cell.dataset.row = row;

            cell.dataset.col = col;

            board.appendChild(cell);

        }

    }

}

createBoard();