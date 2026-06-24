import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Game",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 Snake Game")
st.markdown("Use **WASD** or **Arrow Keys** to move. "
            "Eat 🍎 to grow. Don't hit the walls!")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.markdown("🟢 **Green** = Snake")
col2.markdown("🔴 **Red** = Food")
col3.markdown("⬛ **Black** = Wall")

# Full Snake game in HTML/JS
snake_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    background: #0d1117;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Courier New', monospace;
    color: #58a6ff;
    margin: 0;
    padding: 10px;
  }
  #score-board {
    display: flex;
    gap: 40px;
    margin-bottom: 10px;
    font-size: 1rem;
    font-weight: bold;
  }
  .score-item span {
    color: #2ecc71;
    font-size: 1.3rem;
  }
  #canvas {
    border: 3px solid #30363d;
    border-radius: 8px;
    box-shadow: 0 0 30px rgba(46,204,113,0.2);
    display: block;
  }
  #controls {
    margin-top: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }
  .ctrl-row {
    display: flex;
    gap: 6px;
  }
  .ctrl-btn {
    width: 44px;
    height: 44px;
    background: #161b22;
    border: 2px solid #30363d;
    border-radius: 8px;
    color: #58a6ff;
    font-size: 1.1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
    transition: background 0.1s;
  }
  .ctrl-btn:active, .ctrl-btn.active {
    background: #2ecc71;
    color: #000;
    border-color: #2ecc71;
  }
  #message {
    margin-top: 10px;
    font-size: 1rem;
    color: #f39c12;
    height: 24px;
    text-align: center;
  }
  #start-btn {
    margin-top: 8px;
    padding: 10px 32px;
    background: #2ecc71;
    color: #000;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    letter-spacing: 1px;
  }
  #start-btn:hover {
    background: #27ae60;
  }
  #difficulty {
    margin-top: 8px;
    display: flex;
    gap: 8px;
  }
  .diff-btn {
    padding: 6px 18px;
    background: #161b22;
    border: 2px solid #30363d;
    border-radius: 6px;
    color: #58a6ff;
    cursor: pointer;
    font-family: monospace;
    font-size: 0.85rem;
  }
  .diff-btn.selected {
    background: #1f6feb;
    border-color: #58a6ff;
    color: white;
  }
</style>
</head>
<body>

<div id="score-board">
  <div class="score-item">Score: <span id="score">0</span></div>
  <div class="score-item">High Score: <span id="high-score">0</span></div>
  <div class="score-item">Length: <span id="length">1</span></div>
</div>

<canvas id="canvas" width="400" height="400"></canvas>

<div id="message">Press START to play!</div>

<div id="difficulty">
  <button class="diff-btn selected" onclick="setDiff(150,'Easy',this)">Easy</button>
  <button class="diff-btn" onclick="setDiff(100,'Medium',this)">Medium</button>
  <button class="diff-btn" onclick="setDiff(60,'Hard',this)">Hard</button>
  <button class="diff-btn" onclick="setDiff(35,'Pro',this)">Pro</button>
</div>

<button id="start-btn" onclick="startGame()">▶ START</button>

<div id="controls">
  <div class="ctrl-row">
    <button class="ctrl-btn" id="btn-up" onclick="setDir(0,-1)">▲</button>
  </div>
  <div class="ctrl-row">
    <button class="ctrl-btn" id="btn-left" onclick="setDir(-1,0)">◄</button>
    <button class="ctrl-btn" id="btn-down" onclick="setDir(0,1)">▼</button>
    <button class="ctrl-btn" id="btn-right" onclick="setDir(1,0)">►</button>
  </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx    = canvas.getContext('2d');
const GRID   = 20;
const COLS   = canvas.width  / GRID;
const ROWS   = canvas.height / GRID;

let snake, dir, nextDir, food, score,
    highScore, gameLoop, speed, running;

highScore = 0;
speed     = 150;

function setDiff(s, label, btn) {
  speed = s;
  document.querySelectorAll('.diff-btn')
    .forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
}

function setDir(dx, dy) {
  if (dx === 1  && dir.x !== -1) nextDir = {x:1,  y:0};
  if (dx === -1 && dir.x !== 1)  nextDir = {x:-1, y:0};
  if (dy === 1  && dir.y !== -1) nextDir = {x:0,  y:1};
  if (dy === -1 && dir.y !== 1)  nextDir = {x:0,  y:-1};

  // Button highlight
  ['up','down','left','right'].forEach(d =>
    document.getElementById('btn-'+d)
      .classList.remove('active'));
  if (dx===1)  document.getElementById('btn-right').classList.add('active');
  if (dx===-1) document.getElementById('btn-left').classList.add('active');
  if (dy===1)  document.getElementById('btn-down').classList.add('active');
  if (dy===-1) document.getElementById('btn-up').classList.add('active');
}

function randomFood() {
  let pos;
  do {
    pos = {
      x: Math.floor(Math.random() * COLS),
      y: Math.floor(Math.random() * ROWS)
    };
  } while (snake.some(s => s.x===pos.x && s.y===pos.y));
  return pos;
}

function startGame() {
  clearInterval(gameLoop);
  snake   = [{x:10, y:10}];
  dir     = {x:1, y:0};
  nextDir = {x:1, y:0};
  score   = 0;
  running = true;
  food    = randomFood();
  updateUI();
  document.getElementById('message').textContent =
    'Use arrows or WASD!';
  gameLoop = setInterval(tick, speed);
}

function tick() {
  dir = {...nextDir};
  const head = {
    x: snake[0].x + dir.x,
    y: snake[0].y + dir.y
  };

  // Wall collision
  if (head.x < 0 || head.x >= COLS ||
      head.y < 0 || head.y >= ROWS) {
    return gameOver();
  }
  // Self collision
  if (snake.some(s => s.x===head.x && s.y===head.y)) {
    return gameOver();
  }

  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    score += 10;
    if (score > highScore) highScore = score;
    food = randomFood();
  } else {
    snake.pop();
  }

  updateUI();
  draw();
}

function gameOver() {
  clearInterval(gameLoop);
  running = false;
  document.getElementById('message').textContent =
    `💀 Game Over! Score: ${score} — Press START to retry`;
  drawGameOver();
}

function updateUI() {
  document.getElementById('score').textContent = score;
  document.getElementById('high-score').textContent = highScore;
  document.getElementById('length').textContent = snake.length;
}

function draw() {
  // Background
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Grid dots
  ctx.fillStyle = '#161b22';
  for (let x = 0; x < COLS; x++) {
    for (let y = 0; y < ROWS; y++) {
      ctx.fillRect(x*GRID+9, y*GRID+9, 2, 2);
    }
  }

  // Food
  ctx.fillStyle = '#e74c3c';
  ctx.shadowColor = '#e74c3c';
  ctx.shadowBlur  = 12;
  ctx.beginPath();
  ctx.arc(
    food.x*GRID + GRID/2,
    food.y*GRID + GRID/2,
    GRID/2 - 2, 0, Math.PI*2
  );
  ctx.fill();
  ctx.shadowBlur = 0;

  // Snake body
  snake.forEach((seg, i) => {
    const ratio = 1 - (i / snake.length) * 0.6;
    ctx.fillStyle = i === 0
      ? '#2ecc71'
      : `rgba(46, ${Math.floor(180*ratio)}, ${Math.floor(80*ratio)}, 0.9)`;
    ctx.shadowColor = i === 0 ? '#2ecc71' : 'transparent';
    ctx.shadowBlur  = i === 0 ? 8 : 0;

    const padding = i === 0 ? 1 : 2;
    ctx.beginPath();
    ctx.roundRect(
      seg.x*GRID + padding,
      seg.y*GRID + padding,
      GRID - padding*2,
      GRID - padding*2,
      i === 0 ? 5 : 3
    );
    ctx.fill();
    ctx.shadowBlur = 0;
  });

  // Eyes on head
  if (snake.length > 0) {
    const h = snake[0];
    ctx.fillStyle = '#000';
    let ex1, ey1, ex2, ey2;
    if (dir.x === 1) {
      ex1=h.x*GRID+14; ey1=h.y*GRID+5;
      ex2=h.x*GRID+14; ey2=h.y*GRID+13;
    } else if (dir.x === -1) {
      ex1=h.x*GRID+4;  ey1=h.y*GRID+5;
      ex2=h.x*GRID+4;  ey2=h.y*GRID+13;
    } else if (dir.y === 1) {
      ex1=h.x*GRID+5;  ey1=h.y*GRID+14;
      ex2=h.x*GRID+13; ey2=h.y*GRID+14;
    } else {
      ex1=h.x*GRID+5;  ey1=h.y*GRID+4;
      ex2=h.x*GRID+13; ey2=h.y*GRID+4;
    }
    ctx.beginPath(); ctx.arc(ex1,ey1,2,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(ex2,ey2,2,0,Math.PI*2); ctx.fill();
  }
}

function drawGameOver() {
  ctx.fillStyle = 'rgba(0,0,0,0.6)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#e74c3c';
  ctx.font = 'bold 36px Courier New';
  ctx.textAlign = 'center';
  ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2 - 20);
  ctx.fillStyle = '#58a6ff';
  ctx.font = '20px Courier New';
  ctx.fillText(`Score: ${score}`, canvas.width/2, canvas.height/2 + 20);
  ctx.fillStyle = '#2ecc71';
  ctx.font = '14px Courier New';
  ctx.fillText('Press START to play again',
    canvas.width/2, canvas.height/2 + 55);
}

// Initial draw
ctx.fillStyle = '#0d1117';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = '#2ecc71';
ctx.font = 'bold 28px Courier New';
ctx.textAlign = 'center';
ctx.fillText('🐍 SNAKE', canvas.width/2, canvas.height/2 - 20);
ctx.fillStyle = '#58a6ff';
ctx.font = '16px Courier New';
ctx.fillText('Press START to begin',
  canvas.width/2, canvas.height/2 + 20);

// Keyboard controls
document.addEventListener('keydown', e => {
  if (!running) return;
  if (e.key==='ArrowUp'    || e.key==='w' || e.key==='W')
    setDir(0,-1);
  if (e.key==='ArrowDown'  || e.key==='s' || e.key==='S')
    setDir(0,1);
  if (e.key==='ArrowLeft'  || e.key==='a' || e.key==='A')
    setDir(-1,0);
  if (e.key==='ArrowRight' || e.key==='d' || e.key==='D')
    setDir(1,0);
  e.preventDefault();
});
</script>
</body>
</html>
"""

components.html(snake_html, height=680)

st.markdown("---")
st.markdown("""
### 🎮 How to Play
- Press **START** to begin
- **Arrow keys** or **WASD** to move
- Eat the 🔴 red food to grow and score points
- Don't hit the walls or yourself!

### 🏆 Scoring
| Action | Points |
|---|---|
| Eat food | +10 |
| Each food eaten | Snake grows by 1 |

### ⚡ Difficulty
| Level | Speed |
|---|---|
| Easy | 150ms per tick |
| Medium | 100ms per tick |
| Hard | 60ms per tick |
| Pro | 35ms per tick |
""")

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "Snake Game | "
    "HTML5 Canvas + JavaScript in Streamlit"
)