function getQuantity(nameFruit) {
    // TODO get quantity of fruit from server
    return 50;
}

function getPrice(nameFruit) {
    // TODO get price of fruit from server
    return 5;
}

function getRecommendedPrice(nameFruit) {
    // TODO get recommended price of fruit from server
    return 6;
}

function getLight(nameFruit) {
    // TODO get light of fruit from server
    return 2;
}

function getAvgCostEstimate(nameFruit) {
    // TODO get price of fruit from server
    return 5;
}

function getHistory(nameFruit) {
    // TODO get history of fruit from server
    return "price changed to 5\ndelivery of 50";
}

function recordDelivery(nameFruit, quantity, costPerItem) {
    // TODO send recorded delivery to server
    alert("delivery of " + quantity + " " + nameFruit + "s at " + costPerItem);
}

function recordSale(nameFruit, quantity) {
    // TODO send recorded sale to server
    alert("sale of " + quantity + " " + nameFruit + "s")
}

function setPrice(nameFruit, price) {
    // TODO send new price to server
    alert("price of " + nameFruit + " changed to " + price);
}

function updatePrice(nameFruit) {
    // TODO send to server
    alert("updated price of " + nameFruit);
}

function loadFruit() {
    var selectFruitBox = document.getElementById("fruits");
    var selectedFruit = selectFruitBox.value;

    var title = document.getElementById("title");
    title.innerHTML = selectedFruit;

    var quantity = document.getElementById("quantity");
    var price = document.getElementById("price");
    var recommendedPrice = document.getElementById("recommendedPrice");
    var light = document.getElementById("light");
    var avgCostEstimate = document.getElementById("avgCostEstimate");

    quantity.innerHTML = getQuantity(selectedFruit);
    price.innerHTML = getPrice(selectedFruit);
    recommendedPrice.innerHTML = getRecommendedPrice(selectedFruit);
    light.innerHTML = getLight(selectedFruit);
    avgCostEstimate.innerHTML = getAvgCostEstimate(selectedFruit);

    var history = document.getElementById("history");
    history.innerHTML = getHistory(selectedFruit).replace(/\n/g, "<br>");
}

function executeCode() {
    var editor = document.getElementById("editor");
    var code = editor.value
    var tokens = code.replace( /\n/g, " " ).split( " " ).filter(function(e){return e});;
    
    for (var i = 0; i < tokens.length; i++) {
        var token = tokens[i];

        if (token == "delivery") {
            var quantity = tokens[i + 2];
            var name = tokens[i + 3];
            var price = tokens[i + 5];

            recordDelivery(name, quantity, price);
        }
        if (token == "sale") {
            var nameFruit = tokens[i + 3];
            var quantity = tokens[i + 2];

            recordSale(nameFruit, quantity);
        }
        if (token == "update") {
            var nameFruit = tokens[i + 3];

            updatePrice(nameFruit);
        }
        if (token == "set")  {
            var nameFruit = tokens[i + 3];
            var quantity = tokens[i + 5];

            setPrice(nameFruit, quantity);

        }
    }
}
