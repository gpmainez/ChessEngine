var board = null;

function onDrop(source, target, piece, newPos, oldPos, orientation) {
    if (source === target) return;

    fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: source, target: target })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            board.position(data.fen);
        } else {
            console.warn("Niedozwolony ruch! Cofam bierkę.");
            board.position(oldPos);
        }
    })
    .catch(error => {
        console.error('Błąd połączenia z serwerem:', error);
        board.position(oldPos);
    });
}

var config = {
    draggable: true,
    position: 'start',
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
    onDrop: onDrop
};

board = Chessboard('myBoard', config);