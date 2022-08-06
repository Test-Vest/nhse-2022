const menu = document.querySelector("#mobile-menu");
const menuLinks = document.querySelector(".navbar__menu");

const addButton = document.getElementById("createInput");
addButton.addEventListener("click", addInput, false);

function newTextInput(placeholder = "something...") {
  const input = document.createElement("input");
  input.classList.add("form-control", "mx-2");
  input.style.maxWidth = "180px";
  input.placeholder = placeholder;

  return input;
}

function newPrepositionText(preposition) {
  const text = document.createElement("p");
  text.innerText = preposition;
  text.style.margin = 0;

  return text;
}

function newSelect(optionsData, onSelectChange) {
  const select = document.createElement("select");
  select.classList.add("form-select", "mx-2");
  select.style.minWidth = "136px";
  select.style.maxWidth = "172px";

  optionsData.forEach((optionData) => {
    const option = document.createElement("option");
    option.text = optionData[0];
    option.value = optionData[1];

    select.appendChild(option);
  });

  onSelectChange && select.addEventListener("change", onSelectChange);

  return select;
}

function newElementSelect(wholePageOptionDisabled = false) {
  const onSelectChange = (event) => {
    const button = document.createElement("button");
    const buttonClassName = "element-select";
    button.classList.add("btn", "btn-primary", buttonClassName);
    button.textContent = "select one";

    const row = event.target.parentElement;
    const elementSelectButton = row.getElementsByClassName(buttonClassName)[0];
    console.log(row, elementSelectButton);
    if (elementSelectButton) {
      elementSelectButton.remove();
    }

    row.appendChild(button);
  };

  return newSelect(
    [
      ...(!wholePageOptionDisabled ? [["whole page", "wholepage"]] : []),
      ["custom element", "custom"],
    ],
    onSelectChange
  );
}

function addInput(evt) {
  evt.preventDefault();
  // Get the element where the inputs will be added to
  var container = document.getElementById("input-container");
  container.classList.add("mt-3");
  // Create an <input> element, set its type and name attributes
  var row = document.createElement("div");
  row.classList.add(
    "test-row",
    "mt-2",
    "d-flex",
    "justify-content-between",
    "align-items-center"
  );

  container.appendChild(row);
  var input = document.createElement("select");
  input.classList.add("form-select", "select-syllable");
  input.style = "width: 100px;";
  input.options[input.options.length] = new Option("Select", "null");
  input.options[input.options.length] = new Option("Has", "has");
  input.options[input.options.length] = new Option("Set", "set");
  input.options[input.options.length] = new Option("Trigger", "trigger");
  input.addEventListener("change", setOption(row), false);
  row.appendChild(input);
}

const removeButton = document.getElementById("removeInput");
removeButton.addEventListener("click", removeInput, false);

function removeInput(evt) {
  evt.preventDefault();
  var container = document.getElementById("input-container");
  if (!container.hasChildNodes()) {
    return;
  } else {
    container.removeChild(container.lastChild);
  }
}

function setOption(row) {
  function clearRow() {
    const otherElements = [
      ...row.querySelectorAll("*:not(select.select-syllable, option)"),
    ];
    otherElements.forEach((el) => el.remove());
  }

  return function (evt) {
    clearRow();

    const selectedValue = evt.target.value;
    switch (selectedValue) {
      case "has":
        row.appendChild(newTextInput());
        row.appendChild(newPrepositionText("in"));
        row.appendChild(newElementSelect());
        break;

      case "set":
        row.appendChild(newTextInput());
        row.appendChild(newPrepositionText("in"));
        row.appendChild(newElementSelect());
        break;

      case "trigger":
        row.appendChild(
          newSelect([
            ["click", "click"],
            ["focus", "focus"],
          ])
        );
        row.appendChild(newPrepositionText("on"));
        row.appendChild(newElementSelect(true));
        break;
    }
  };
}
