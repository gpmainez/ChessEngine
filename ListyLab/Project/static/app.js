var board = null;
var selectedMode = 'standard';
var selectedColor = 'white';
var gameOver = false;

function setStatus(msg) {
    document.getElementById('statusMsg').textContent = msg;
}

function selectMode(mode) {
    selectedMode = mode;
    document.getElementById('btnStandard').classList.toggle('active', mode === 'standard');
    document.getElementById('btnFisher').classList.toggle('active', mode === 'fisher');
}

function selectColor(color) {
    selectedColor = color;
    document.getElementById('btnWhite').classList.toggle('active', color === 'white');
    document.getElementById('btnBlack').classList.toggle('active', color === 'black');
    document.getElementById('btnRandom').classList.toggle('active', color === 'random');
}

function startNewGame() {
    fetch('/api/new_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: selectedMode, player_color: selectedColor })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            board.position(data.fen);
            gameOver = false;
            document.getElementById('gameOverBanner').style.display = 'none';
            var colName = data.player_color === 'white' ? 'białe' : 'czarne';
            setStatus('Nowa gra: ' + (selectedMode === 'fisher' ? 'Chess960' : 'standardowe') + ' (' + colName + ')');
        } else {
            setStatus('Blad: ' + data.message);
        }
    });
}

function showModePanel() {
    document.getElementById('gameOverBanner').style.display = 'none';
    gameOver = false;
}

function handleGameOver(state) {
    if (!state) return;
    gameOver = true;
    var msg = state === 'CHECKMATE' ? 'SZACH MAT!' : 'REMIS (pat)';
    document.getElementById('gameOverMsg').textContent = msg;
    document.getElementById('gameOverBanner').style.display = 'flex';
}

function onDrop(source, target, piece, newPos, oldPos, orientation) {
    if (source === target || gameOver) return;

    fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: source, target: target })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            board.position(data.fen);
            if (data.game_over) {
                handleGameOver(data.game_over);
            }
        } else {
            board.position(oldPos);
        }
    })
    .catch(error => {
        console.error('Blad polaczenia:', error);
        board.position(oldPos);
    });
}

function saveGame() {
    fetch('/api/save', { method: 'POST' })
        .then(r => r.json())
        .then(d => setStatus(d.status === 'success' ? 'Zapisano gre.' : 'Blad zapisu.'));
}

function loadGame() {
    fetch('/api/load', { method: 'POST' })
        .then(r => r.json())
        .then(d => {
            if (d.status === 'success') {
                board.position(d.fen);
                gameOver = false;
                document.getElementById('gameOverBanner').style.display = 'none';
                if (d.game_over) {
                    handleGameOver(d.game_over);
                }
                setStatus('Wczytano gre.');
            } else {
                setStatus('Blad wczytania: ' + d.message);
            }
        });
}

var config = {
    draggable: true,
    position: 'start',
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
    onDrop: onDrop
};

board = Chessboard('myBoard', config);