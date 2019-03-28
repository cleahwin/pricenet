function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function getQuantity(nameFruit) {
    // get quantity of fruit from server
    return httpGet("http://localhost:8080/" + nameFruit + "/get-quantity");
}

function getPrice(nameFruit) {
    // get price of fruit from server
    return httpGet("http://localhost:8080/" + nameFruit + "/get-price");
}

function getRecommendedPrice(nameFruit) {
    // get recommended price of fruit from server
    return httpGet("http://localhost:8080/" + nameFruit + "/get-recommended-price");
}

function getLight(nameFruit) {
    // get light of fruit from server
    return httpGet("http://localhost:8080/" + nameFruit + "/get-light");
}

function getAvgCostEstimate(nameFruit) {
    // get approximated cost of fruit from server
    return httpGet("http://localhost:8080/" + nameFruit + "/get-avg-cost-estimate");
}

function getHistory(nameFruit) {
    // get history of fruit from server
    return httpGet("http://localhost:8080/" + nameFruit + "/get-history");
}

function recordDelivery(nameFruit, quantity, costPerItem) {
    // send recorded delivery to server
    return httpGet("http://localhost:8080/" + nameFruit + "/record-delivery/" + quantity + "/" + costPerItem);
    alert("delivery of " + quantity + " " + nameFruit + "s at " + costPerItem);
}

function recordSale(nameFruit, quantity) {
    // send recorded sale to server
    return httpGet("http://localhost:8080/" + nameFruit + "/record-sale/" + quantity);
    alert("sale of " + quantity + " " + nameFruit + "s")
}

function setPrice(nameFruit, price) {
    // send new price to server
    return httpGet("http://localhost:8080/" + nameFruit + "/set-price/" + price);
    alert("price of " + nameFruit + " changed to " + price);
}

function updatePrice(nameFruit) {
    return httpGet("http://localhost:8080/" + nameFruit + "/update-price/");
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

    quantity.innerHTML = "Quantity: " + getQuantity(selectedFruit);
    price.innerHTML = "Price:" + getPrice(selectedFruit);
    recommendedPrice.innerHTML ="Reccomended Price: " + "$" + getRecommendedPrice(selectedFruit);
    light.innerHTML = "Light: " + getLight(selectedFruit);
    avgCostEstimate.innerHTML = "Average Cost Estimate: " + getAvgCostEstimate(selectedFruit);

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
