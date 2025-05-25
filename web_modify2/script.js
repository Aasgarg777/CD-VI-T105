async function analyze() {
    const sentence = document.getElementById("sentenceInput").value;
    const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence: sentence })
    });
    const data = await response.json();
    drawTokenTable(data.tokens);
    drawAST(data.ast);
}

function drawTokenTable(tokens) {
    const tableHTML = `
        <table>
            <tr><th>Word</th><th>POS</th></tr>
            ${tokens.map(([word, pos]) => `<tr><td>${word}</td><td>${pos}</td></tr>`).join('')}
        </table>
    `;
    document.getElementById("tokenTable").innerHTML = tableHTML;
}

function drawAST(ast) {
    const canvas = document.getElementById("astCanvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    function drawNode(node, x, y, level) {
        ctx.beginPath();
        ctx.arc(x, y, 30, 0, 2 * Math.PI);
        ctx.fillStyle = "lightblue";
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText(node.value, x, y + 5);

        if (!node.children) return;

        const spacing = 120;
        const childY = y + 100;
        const totalWidth = spacing * (node.children.length - 1);
        let childX = x - totalWidth / 2;

        for (let child of node.children) {
            ctx.beginPath();
            ctx.moveTo(x, y + 30);
            ctx.lineTo(childX, childY - 30);
            ctx.stroke();
            drawNode(child, childX, childY, level + 1);
            childX += spacing;
        }
    }

    drawNode(ast, canvas.width / 2, 60, 0);
}
