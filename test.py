<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Santa's Delivery Dash</title>
<style>
  body {
    margin: 0;
    background: #000;
    font-family: sans-serif;
  }
  #scoreBoard {
    text-align: center;
    font-size: 24px;
    color: #fff;
    margin-top: 10px;
  }
  #gameArea {
    position: relative;
    width: 1200px;
    height: 1200px;
    margin: 20px auto;
    background: #000;
    border: 2px solid #fff;
    overflow: hidden;
  }
  #santa {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 100px;
  }
  .gift, .obstacle, .powerup {
    position: absolute;
    width: 70px;
    height: 70px;
  }
  .gift img, .obstacle img, .powerup img {
    display: block;
    width: auto;
    height: auto;
    max-width: 70px;
    max-height: 70px;
}
</style>
</head>
<body>

<div id="scoreBoard">Score: 0</div>
<div id="gameArea">
  <img id="santa" src="{{ url_for('static', filename='images/games/christmas/santa.png') }}" alt="santa">
</div>

<script>
const gameArea = document.getElementById('gameArea');
const santa = document.getElementById('santa');

let score = 0;
let speed = 2;
let santaX = (gameArea.offsetWidth - 100)/2;
let objects = [];

const giftImages = [
    "{{ url_for('static', filename='images/games/christmas/tata.png') }}",
    "{{ url_for('static', filename='images/games/christmas/cooky.png') }}",
    "{{ url_for('static', filename='images/games/christmas/green_gift.png') }}",
    "{{ url_for('static', filename='images/games/christmas/purple_gift.png') }}"
];
const obstacleImages = [
    "{{ url_for('static', filename='images/games/christmas/snowflake.png') }}",
    "{{ url_for('static', filename='images/games/christmas/snowman.png') }}"
];
const powerupImage = "{{ url_for('static', filename='images/games/christmas/star.png') }}";

function getGameDimensions() {
    return { width: gameArea.offsetWidth, height: gameArea.offsetHeight };
}

function createObject(type) {
    const { width } = getGameDimensions();
    const obj = document.createElement('div');
    obj.classList.add(type);
    obj.style.left = Math.random() * (width - 70) + 'px';
    obj.style.top = '-70px';
    const img = document.createElement('img');

    if(type === 'gift') img.src = giftImages[Math.floor(Math.random() * giftImages.length)];
    else if(type === 'obstacle') img.src = obstacleImages[Math.floor(Math.random() * obstacleImages.length)];
    else if(type === 'powerup') img.src = powerupImage;

    obj.appendChild(img);
    gameArea.appendChild(obj);
    objects.push({element: obj, type: type});
}

function moveObjects() {
    const { width, height } = getGameDimensions();
    for (let i = objects.length - 1; i >= 0; i--) {
        const obj = objects[i];
        let top = parseFloat(obj.element.style.top) + speed;
        obj.element.style.top = top + 'px';

        const santaRect = santa.getBoundingClientRect();
        const objRect = obj.element.getBoundingClientRect();

        if (!(santaRect.right < objRect.left ||
              santaRect.left > objRect.right ||
              santaRect.bottom < objRect.top ||
              santaRect.top > objRect.bottom)) {

            if(obj.type === 'gift') score += 10;
            else if(obj.type === 'powerup') speed = 5;
            else if(obj.type === 'obstacle') score = Math.max(0, score - 20);

            gameArea.removeChild(obj.element);
            objects.splice(i,1);
        } else if(top > height) {
            gameArea.removeChild(obj.element);
            objects.splice(i,1);
        }
    }

    document.getElementById('scoreBoard').textContent = "Score: " + score;
}

function gameLoop() {
    if(Math.random() < 0.02) createObject('gift');
    if(Math.random() < 0.01) createObject('obstacle');
    if(Math.random() < 0.005) createObject('powerup');

    moveObjects();
    requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', e => {
    const { width } = getGameDimensions();
    if(e.key === 'ArrowLeft') santaX -= 20;
    if(e.key === 'ArrowRight') santaX += 20;
    santaX = Math.max(0, Math.min(width - 70, santaX));
    santa.style.left = santaX + 'px';
});

gameLoop();
</script>

</body>
</html>
