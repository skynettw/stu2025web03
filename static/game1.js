// 簡化打磚塊遊戲（你可換成完整版本）
// 遊戲結束後呼叫 submitScore(score)

let canvas = document.getElementById("gameCanvas");
let ctx = canvas.getContext("2d");

let score = 0;
let y = 200;
let dy = -2;

function draw() {
    ctx.clearRect(0, 0, 400, 400);
    ctx.beginPath();
    ctx.arc(200, y, 10, 0, Math.PI * 2);
    ctx.fill();

    y += dy;
    if (y <= 10) {
        dy = 2;
        score++;
    }
    if (y >= 390) {
        alert("遊戲結束！你的分數：" + score);
        submitScore(score);
        return;
    }

    requestAnimationFrame(draw);
}

draw();
