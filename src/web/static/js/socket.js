
function updateFields(data) {
    for (let quantityName in data) {
        const valueField = document.querySelector(`#${quantityName} .value`);

        if (data[quantityName].value === null || valueField === null) { continue; }

        valueField.textContent = data[quantityName].value.toLocaleString();
    }
}


window.onload = function () {
    let websocket = new WebSocket(`ws://localhost:${websocketPort}`);

    websocket.onmessage = function (event) {
        console.log("Got message");
        let messageData = JSON.parse(event.data);
        updateFields(messageData)
    };
};
