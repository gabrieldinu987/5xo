/*
==================================================
5XO
Frontend JavaScript
==================================================
*/


/*
==================================================
1. CONSTANTE
==================================================
*/

const BOARD_SIZE = 50;


/*
==================================================
2. GAME STATE
==================================================
*/

const game = {

    board: [],

    currentPlayer: "X",

    winner: null,

    gameOver: false,

    moveCount: 0,

    lastMove: null

};


/*
==================================================
3. ELEMENTE HTML
==================================================
*/

const boardContainer =
    document.getElementById("board-container");

const currentPlayerLabel =
    document.getElementById("current-player");

const gameStatus =
    document.getElementById("game-status");

const resetButton =
    document.getElementById("reset-button");


/*
==================================================
4. FUNCȚII DE CONSTRUIRE - creaza tabla de joc
==================================================
*/

function createBoard() {

    boardContainer.innerHTML = "";

    for (let row = 0; row < BOARD_SIZE; row++) {

        for (let col = 0; col < BOARD_SIZE; col++) {

            const cell = document.createElement("div");

            cell.className = "cell";

            cell.dataset.row = row;

            cell.dataset.col = col;

            cell.addEventListener("click", function () {
                sendMove(row, col);
            });

            boardContainer.appendChild(cell);

        }

    }

}


/*
==================================================
5. FUNCȚII API - incarca starea
==================================================
*/

async function loadGameState() {

    try {

        const response = await fetch("/state");

        if (!response.ok) {

            throw new Error("Cannot load game state.");

        }

        const state = await response.json();

        game.board = state.board;

        game.currentPlayer = state.current_player;

        game.gameOver = state.game_over;

        game.winner = state.winner;

        console.log(game);

    }

    catch (error) {

        console.error(error);

    }

}

async function sendMove(row, col) {

    try {

        const response = await fetch("/move", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                row: row,
                col: col

            })

        });

        if (!response.ok) {

            const error = await response.json();

            alert(error.message);

            return;

        }

        const state = await response.json();

        game.board = state.board;
        game.currentPlayer = state.current_player;
        game.gameOver = state.game_over;
        game.winner = state.winner;

        updateGameInfo();

        renderBoard();

    }

    catch (error) {

        console.error(error);

    }

}

/*
==================================================
6. FUNCȚII UI 
==================================================
*/

// Verifica starea jocului (daca este catigat sau este egalitate)
function updateGameInfo() {

    currentPlayerLabel.textContent =
        game.currentPlayer;

    if (game.gameOver) {

        if (game.winner !== null) {

            gameStatus.textContent =
                "Player " +
                game.winner +
                " wins!";

        }

        else {

            gameStatus.textContent =
                "Draw";

        }

    }

    else {

        gameStatus.textContent =
            "Game Started";

    }

}

// Afiseaza tabla de joc
function renderBoard() {

    for (let row = 0; row < BOARD_SIZE; row++) {

        for (let col = 0; col < BOARD_SIZE; col++) {

            const value = game.board[row][col];

            const cell = document.querySelector(
                `.cell[data-row="${row}"][data-col="${col}"]`
            );

            if (!cell) {
                continue;
            }

            cell.textContent = value ?? "";

        }

    }

}


/*
==================================================
7. EVENIMENTE
==================================================
*/

/*
    Vor fi implementate mai târziu.
*/


/*
==================================================
8. INITIALIZARE
==================================================
*/

async function initializeGame() {

    createBoard();

    await loadGameState();

    updateGameInfo();

    renderBoard();

}


initializeGame();