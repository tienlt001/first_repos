document.addEventListener('DOMContentLoaded', () => {
  const boardEl = document.getElementById('board');
  const statusEl = document.getElementById('status');
  const aiEnabledEl = document.getElementById('ai_enabled');
  const aiPlayerEl = document.getElementById('ai_player');
  const newBtn = document.getElementById('new');

  async function newGame() {
    await fetch('/new', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ai_enabled: aiEnabledEl.checked, ai_player: aiPlayerEl.value})
    });
    await updateBoard();
    statusEl.textContent = '';
  }

  async function updateBoard() {
    const res = await fetch('/state');
    const data = await res.json();
    const cells = data.cells;
    document.querySelectorAll('.cell').forEach((el) => {
      el.textContent = cells[el.dataset.index];
    });
    if (data.winner) {
      statusEl.textContent = `${data.winner} wins!`;
    } else if (data.draw) {
      statusEl.textContent = `Draw!`;
    } else {
      statusEl.textContent = `Current: ${data.current}`;
    }
  }

  boardEl.addEventListener('click', async (ev) => {
    const btn = ev.target.closest('.cell');
    if (!btn) return;
    const idx = parseInt(btn.dataset.index);
    const res = await fetch('/move', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({index: idx})
    });
    const data = await res.json();
    if (!data.success) {
      statusEl.textContent = data.error || 'Invalid move';
      return;
    }
    if (data.cells) {
      document.querySelectorAll('.cell').forEach((el)=> el.textContent = data.cells[el.dataset.index]);
    }
    if (data.winner) {
      statusEl.textContent = `${data.winner} wins!`;
    } else if (data.draw) {
      statusEl.textContent = 'Draw!';
    } else {
      statusEl.textContent = `Current: ${data.current || ''}`;
    }
  });

  newBtn.addEventListener('click', newGame);
  newGame();
  setInterval(updateBoard, 1000);
});
