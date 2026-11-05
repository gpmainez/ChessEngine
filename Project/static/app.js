var board = null;
var selectedMode = 'standard';
var selectedColor = 'white';
var selectedDifficulty = 3;
var gameOver = false;

function setStatus(msg) {
    document.getElementById('statusMsg').textContent = msg;
}

function selectMode(mode) {
    selectedMode = mode;
    document.getElementById('btnStandard').classList.toggle('active', mode === 'standard');
    document.getElementById('btnFisher').classList.toggle('active', mode === 'fisher');
}

function selectDifficulty(diff) {
    selectedDifficulty = diff;
    document.getElementById('btnDiff0').classList.toggle('active', diff === 0);
    document.getElementById('btnDiff1').classList.toggle('active', diff === 1);
    document.getElementById('btnDiff3').classList.toggle('active', diff === 3);
    document.getElementById('btnDiff5').classList.toggle('active', diff === 5);
    document.getElementById('btnDiffBoth').classList.toggle('active', diff === 'both');
    updateSettings();
}

function selectColor(color) {
    selectedColor = color;
    document.getElementById('btnWhite').classList.toggle('active', color === 'white');
    document.getElementById('btnBlack').classList.toggle('active', color === 'black');
    document.getElementById('btnRandom').classList.toggle('active', color === 'random');
    updateSettings();
}

function triggerGameStartBanner() {
    var banner = document.getElementById('gameStartBanner');
    banner.style.display = 'flex';
    banner.style.opacity = '1';
    setTimeout(function() {
        banner.style.opacity = '0';
        setTimeout(function() {
            banner.style.display = 'none';
        }, 400);
    }, 1000);
}

function startNewGame() {
    var color = selectedColor;
    if (selectedDifficulty === 'both') {
        color = 'both';
    }
    fetch('/api/new_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: selectedMode, player_color: color, difficulty: selectedDifficulty === 'both' ? 3 : selectedDifficulty })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            board.position(data.fen);
            if (data.player_color === 'black') {
                board.orientation('black');
            } else {
                board.orientation('white');
            }
            gameOver = false;
            document.getElementById('gameOverBanner').style.display = 'none';
            var colName = data.player_color === 'white' ? 'białe' : (data.player_color === 'black' ? 'czarne' : 'Bez AI');
            setStatus('Nowa gra: ' + (selectedMode === 'fisher' ? 'Chess960' : 'standardowe') + ' (' + colName + ')');
            triggerGameStartBanner();
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

    var color = selectedColor;
    if (selectedDifficulty === 'both') {
        color = 'both';
    }

    fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            source: source,
            target: target,
            difficulty: selectedDifficulty === 'both' ? 3 : selectedDifficulty,
            player_color: color
        })
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
                if (d.player_color === 'black') {
                    board.orientation('black');
                    selectColor('black');
                } else if (d.player_color === 'white') {
                    board.orientation('white');
                    selectColor('white');
                } else {
                    board.orientation('white');
                    selectColor('white');
                }
                if (d.player_color === 'both') {
                    selectDifficulty('both');
                } else if (d.difficulty !== undefined) {
                    selectDifficulty(d.difficulty);
                }
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


function updateSettings() {
    var color = selectedColor;
    if (selectedDifficulty === 'both') {
        color = 'both';
    }
    fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            difficulty: selectedDifficulty === 'both' ? 3 : selectedDifficulty,
            player_color: color
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            if (data.ai_moved) {
                board.position(data.fen);
                if (data.game_over) {
                    handleGameOver(data.game_over);
                }
            }
        }
    });
}


function endGame() {
    selectedMode = 'standard';
    selectedColor = 'white';
    selectedDifficulty = 3;
    gameOver = false;

    document.getElementById('btnStandard').classList.add('active');
    document.getElementById('btnFisher').classList.remove('active');

    selectDifficulty(3);
    selectColor('white');

    document.getElementById('gameOverBanner').style.display = 'none';

    fetch('/api/new_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: 'standard', player_color: 'white', difficulty: 3 })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            board.position('start');
            board.orientation('white');
            setStatus('Gra zakończona. Powrócono do ustawień początkowych.');
        } else {
            setStatus('Blad: ' + data.message);
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