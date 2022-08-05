const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');
const counter = 0;

const addButton = document.getElementById('createInput');
addButton.addEventListener('click', addInput, false);


function addInput(evt) {
  evt.preventDefault();
  // Get the element where the inputs will be added to
  var container = document.getElementById("input-container");
  container.classList.add("mt-3")
  // Create an <input> element, set its type and name attributes
  var row = document.createElement("div");
  row.classList.add("test-row", "mt-2", "d-flex", "justify-content-between", "align-items-center");
  container.appendChild(row);
  var input = document.createElement("select");
  input.id = "input-"+counter;
  input.classList.add('form-select', 'select-syllable');
  input.style = "width: 100px;"
  input.options[input.options.length] = new Option('Select', 'null');
  input.options[input.options.length] = new Option('Has', 'has');
  input.options[input.options.length] = new Option('After', 'after');
  input.options[input.options.length] = new Option('Set', 'set');
  input.options[input.options.length] = new Option('Trigger', 'trigger');
  input.addEventListener("change", setOption(row), false);
  row.appendChild(input);
};

const removeButton = document.getElementById('removeInput');
removeButton.addEventListener('click', removeInput, false);

function removeInput(evt) {
  evt.preventDefault();
  var container = document.getElementById("input-container");
  if(!container.hasChildNodes()) {
    return;
  } else {
    container.removeChild(container.lastChild);
  }
}


function setOption(row) {
  function clearRow() {
    const otherElements = [...row.querySelectorAll("*:not(select.select-syllable, option)")];
    console.log(otherElements);
    otherElements.forEach((el) => el.remove());
  }
  return function(evt) {
    clearRow();
    const selectedValue = evt.target.value;
    switch (selectedValue) {

      case "has":
        const hasInput = document.createElement("input");
        hasInput.className = "form-control";
        hasInput.style = "width: 12rem; height: 2rem;"
        row.appendChild(hasInput);
        const hasText = document.createElement("p");
        hasText.innerText = "in";
        hasText.style.margin = 0
        row.appendChild(hasText);
        const hasSelect = document.createElement("select");
        hasSelect.id = "input-" + counter;
        hasSelect.classList.add('form-select');
        hasSelect.style.width = "136px"
        hasSelect.options[hasSelect.options.length] = new Option('Whole page', 'wholepage');
        hasSelect.options[hasSelect.options.length] = new Option('Custom', 'custom');
        row.appendChild(hasSelect);
        break;

      case "after":
        const afterInput = document.createElement("input");
        afterInput.classList.add("form-input")
        row.appendChild(afterInput);
        const afterText = document.createElement("p");
        afterText.innerText = "in";
        afterText.style.margin = 0
        row.appendChild(afterText);
        const afterSelect = document.createElement("select");
        afterSelect.id = "input-"+counter;
        afterSelect.classList.add('form-select');
        afterSelect.style.width = "136px"
        afterSelect.options[afterSelect.options.length] = new Option('Whole page', 'wholepage');
        afterSelect.options[afterSelect.options.length] = new Option('Custom', 'custom');
        row.appendChild(afterSelect);
        break;

      case "set":
        const setInput = document.createElement("input");
        row.appendChild(setInput);
        const setText = document.createElement("p");
        setText.innerText = "in";
        setText.style.margin = 0
        row.appendChild(setText);
        const setSelect = document.createElement("select");
        setSelect.id = "input-"+counter;
        setSelect.classList.add('form-select');
        setSelect.style.width = "136px"
        setSelect.options[setSelect.options.length] = new Option('Whole page', 'wholepage');
        setSelect.options[setSelect.options.length] = new Option('Custom', 'custom');
        row.appendChild(setSelect);
        break;

      case "trigger":
        const triggerInput = document.createElement("input");
        row.appendChild(triggerInput);
        const triggerText = document.createElement("p");
        triggerText.innerText = "on";
        triggerText.style.margin = 0
        row.appendChild(triggerText);
        const triggerSelect = document.createElement("select");
        triggerSelect.id = "input-"+counter;
        triggerSelect.classList.add('form-select');
        triggerSelect.style.width = "136px"
        triggerSelect.options[triggerSelect.options.length] = new Option('Click', 'click');
        triggerSelect.options[triggerSelect.options.length] = new Option('Focus', 'focus');
        row.appendChild(triggerSelect);
        break;
    }
  }
}



