// taking the input 
function getInputNumber() {
    const dig1 = parseFloat(document.getElementById('dig1').value);
    const dig2 = parseFloat(document.getElementById('dig2').value);  
    return {dig1, dig2};
}

function displayResult(result) {
    document.getElementById('result').textContent = "Result " + result;
}

//creating function for each operation 
function add() {
    const {dig1, dig2} = getInputNumber();
    const result = dig1 + dig2;
    displayResult(result);
}

function subtract() {
    const {dig1, dig2} = getInputNumber();
    const result = dig1 - dig2;
    displayResult(result);
}

function multiply() {
    const {dig1, dig2} = getInputNumber();
    const result = dig1 * dig2;
    displayResult(result);
}

function divide() {
    const {dig1, dig2} = getInputNumber();
    if (dig1 === 0) {
        displayResult("Cannot divide by Zero");
    } else {
        const result =  dig1 / dig2;
        displayResult(result);
    }
}