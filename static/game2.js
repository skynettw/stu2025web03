let canvas = document.getElementById("gameCanvas");
let ctx = canvas.getContext("2d");

let x = 200;
let y = 200;
let score = 0;
let dx = 10;
let dy = 0;

document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp") { dx = 0; dy = -10; }
    if (e.key === "ArrowDown") { dx = 0; dy = 10; }
    if (e.key === "ArrowLeft") { dx = -10; dy = 0; }
    if (e.key === "ArrowRight") { dx = 10; dy = 0; }
});

function gameLoop() {
    ctx.clearRect(0, 0, 400, 400);
    ctx.fillRect(x, y, 10, 10);

    x += dx;
    y += dy;
    score++;

    if (x < 0 || x > 390 || y < 0 || y > 390) {
        alert("遊戲結束！你的分數：" + score);
        submitScore(score);
        return;
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();
