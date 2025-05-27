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
            ${tokens.map(([word, pos]) => <tr><td>${word}</td><td>${pos}</td></tr>).join('')}
        </table>
    `;
    document.getElementById("tokenTable").innerHTML = tableHTML;
}

function drawAST(ast) {
    const canvas = document.getElementById("astCanvas");

    // Set high-res canvas dimensions
    canvas.width = 1800;
    canvas.height = 1200;

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const radius = 40;
    const spacing = 180;
    const verticalGap = 150;
    const animationDelay = 600; // ms between drawing each node

    const queue = []; // Queue of nodes to draw with position and parent info

    // Precompute positions and store in queue
    function enqueueNode(node, x, y, level, parentX = null, parentY = null) {
        queue.push({ node, x, y, level, parentX, parentY });

        if (node.children && node.children.length > 0) {
            const totalWidth = spacing * (node.children.length - 1);
            let childX = x - totalWidth / 2;
            const childY = y + verticalGap;

            for (let child of node.children) {
                enqueueNode(child, childX, childY, level + 1, x, y);
                childX += spacing;
            }
        }
    }

    function drawSingleNode({ node, x, y, parentX, parentY }) {
        // Draw line from parent to current node
        if (parentX !== null && parentY !== null) {
            ctx.beginPath();
            ctx.moveTo(parentX, parentY + radius);
            ctx.lineTo(x, y - radius);
            ctx.stroke();
        }

        // Draw node circle
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        ctx.fillStyle = "lightblue";
        ctx.fill();
        ctx.stroke();

        // Draw node label
        ctx.fillStyle = "black";
        ctx.font = "20px Arial";
        ctx.textAlign = "center";
        ctx.fillText(node.value, x, y + 6);
    }

    // Begin queueing and animate
    enqueueNode(ast, canvas.width / 2, 80, 0);

    let i = 0;
    function animate() {
        if (i < queue.length) {
            drawSingleNode(queue[i]);
            i++;
            setTimeout(animate, animationDelay);
        }
    }

    animate();
}
