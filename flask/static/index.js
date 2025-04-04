"use strict";

const board = document.querySelector("#gameboard");
const territoryName = document.querySelector("#territory-name");
const troopCount = document.querySelector("#troop-count");

let selectedTerritory = "";
let updatedTroopCount = "";
let showUpdatedTroopCount = false;

let currentPlayer = 0;
let playerColors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#888888"];

// TODO: Output JSON to screen

// Object to store the troop data
const territoryArray = [
    "Alaska",
    "Northwest Territories",
    "Greenland",
    "Alberta",
    "Ontario",
    "Quebec",
    "Western United States",
    "Eastern United States",
    "Mexico",
    "Venezuala",
    "Peru",
    "Argentina",
    "Brazil",
    "Iceland",
    "Great Britain",
    "Scandanavia",
    "Western Europe",
    "Northern Europe",
    "Southern Europe",
    "Ukraine",
    "North Africa",
    "Egypt",
    "East Africa",
    "Congo",
    "South Africa",
    "Madagascar",
    "Middle East",
    "Ural",
    "Siberia",
    "Yakutsk",
    "Irkutsk",
    "Kamchatka",
    "Afghanistan",
    "Mongolia",
    "China",
    "Japan",
    "India",
    "South East Asia",
    "Indonesia",
    "New Guinea",
    "Western Australia",
    "Eastern Australia"
]

const territoryIDs = [
    "alaska",
    "northwest_territory",
    "greenland",
    "alberta",
    "onterio",
    "quebec",
    "western_united_states",
    "eastern_united_states",
    "mexico",
    "venezuala",
    "peru",
    "argentina",
    "brazil",
    "iceland",
    "great_britain",
    "scandinavia",
    "western_europe",
    "northern_europe",
    "southern_europe",
    "ukraine",
    "north_africa",
    "egypt",
    "east_africa",
    "congo",
    "south_africa",
    "madagascar",
    "middle_east",
    "ural",
    "siberia",
    "yakutsk",
    "irkutsk",
    "kamchatka",
    "afghanistan",
    "mongolia",
    "china",
    "japan",
    "india",
    "siam",
    "indonisia",
    "new_guinea",
    "western_australia",
    "eastern_australia"
]

// Generate <text> elements to show troop counts
for (let i = 0; i < territoryIDs.length; i++) {
    const territory = document.querySelector("#" + territoryIDs[i]);

    // Find center of territory
    const bBox = territory.getBBox();
    const centerX = bBox.x + bBox.width / 2;
    const centerY = bBox.y + bBox.height / 2;

    const textElement = document.createElementNS("http://www.w3.org/2000/svg", "text");

    textElement.setAttribute("x", centerX);
    textElement.setAttribute("y", centerY);
    textElement.setAttribute("text-anchor", "middle");

    textElement.textContent = 0;

    textElement.id = territoryIDs[i] + "-troops";
    textElement.classList.add("small");

    document.querySelector("#gameboard").appendChild(textElement);
}

let jsonData = {}
const idToDisplay = {}
for (let i = 0; i < territoryArray.length; i++) {
    // jsonData[territoryIDs[i]] = { owner: 0, troops: 1, displayName: territoryArray[i] }
    jsonData[territoryArray[i]] = { owner: 0, troops: 1 };
    idToDisplay[territoryIDs[i]] = territoryArray[i];
}

board.addEventListener("click", (event) => {
    if (territoryArray.includes(selectedTerritory)) {
        jsonData[selectedTerritory].owner += 1;
        if (jsonData[selectedTerritory].owner % 5 == 0) {
            jsonData[selectedTerritory].owner = 0;
        }
    }
    // const svgTest = document.createElement("svg",);
    // svgTest.innerHTML = selectedTerritory
    updateMap();
});

board.addEventListener("mouseover", (event) => {
    if (territoryIDs.includes(event.target.id)) {
        selectedTerritory = idToDisplay[event.target.id];
        console.log(selectedTerritory)
        updatedTroopCount = "";
        showUpdatedTroopCount = false;
        updateMap();
    }
});

window.addEventListener("keyup", (event) => {
    console.log(event.key)
    if (!isNaN(event.key) && territoryArray.includes(selectedTerritory)) {
        console.log(true)
        updatedTroopCount += event.key;
        showUpdatedTroopCount = true;
    }
    if (event.key == "Backspace" && updatedTroopCount.length > 0) {
        updatedTroopCount = updatedTroopCount.substring(0, updatedTroopCount.length - 1);
    }
    if (event.key == "Enter" && updatedTroopCount.length > 0) {
        jsonData[selectedTerritory].troops = parseFloat(updatedTroopCount)
        showUpdatedTroopCount = false;
    }
    updateMap();
})

// document.querySelector("#json-textarea-in-btn").addEventListener("click", (event) => {
//     /*{"Alaska":{"owner":0,"troops":10},"Northwest Territories":{"owner":0,"troops":1},"Greenland":{"owner":0,"troops":1},"Alberta":{"owner":0,"troops":1},"Ontario":{"owner":0,"troops":1},"Quebec":{"owner":0,"troops":1},"Western United States":{"owner":0,"troops":1},"Eastern United States":{"owner":0,"troops":1},"Mexico":{"owner":0,"troops":1},"Venezuala":{"owner":1,"troops":1},"Peru":{"owner":1,"troops":1},"Argentina":{"owner":1,"troops":1},"Brazil":{"owner":1,"troops":10},"Iceland":{"owner":3,"troops":1},"Great Britain":{"owner":3,"troops":1},"Scandanavia":{"owner":3,"troops":1},"Western Europe":{"owner":3,"troops":1},"Northern Europe":{"owner":3,"troops":1},"Southern Europe":{"owner":3,"troops":1},"Ukraine":{"owner":3,"troops":1},"North Africa":{"owner":2,"troops":10},"Egypt":{"owner":2,"troops":1},"East Africa":{"owner":2,"troops":1},"Congo":{"owner":2,"troops":1},"South Africa":{"owner":2,"troops":1},"Madagascar":{"owner":2,"troops":1},"Middle East":{"owner":4,"troops":10},"Ural":{"owner":4,"troops":1},"Siberia":{"owner":4,"troops":1},"Yakutsk":{"owner":4,"troops":1},"Irkutsk":{"owner":4,"troops":1},"Kamchatka":{"owner":4,"troops":1},"Afghanistan":{"owner":4,"troops":1},"Mongolia":{"owner":4,"troops":1},"China":{"owner":4,"troops":1},"Japan":{"owner":4,"troops":1},"India":{"owner":4,"troops":1},"South East Asia":{"owner":4,"troops":1},"Indonesia":{"owner":1,"troops":10},"New Guinea":{"owner":1,"troops":1},"Western Australia":{"owner":1,"troops":1},"Eastern Australia":{"owner":1,"troops":1}}*/
//     jsonData = JSON.parse(document.querySelector("#json-textarea-in").value);
//     updateMap();
// })

document.querySelector("#json-textarea-send-request").addEventListener("click", (event) => {
    console.log(document.URL);
    fetch(document.URL + "/", {
        method: "POST",
        body: JSON.stringify(jsonData),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then((response) => response.json()).then((json) => {
        console.log(json);
        jsonData = json;
        updateMap();
    });
});

function updateMap() {
    for (let i = 0; i < territoryIDs.length; i++) {
        const territory = document.querySelector("#" + territoryIDs[i]);
        const territoryLabel = document.querySelector("#" + territoryIDs[i] + "-troops");
        // Set color based on owner
        // console.log(i, territoryArray[i], jsonData)
        territory.setAttribute("fill", playerColors[jsonData[territoryArray[i]].owner])

        territoryLabel.textContent = jsonData[territoryArray[i]].troops;
    }

    // Update troop number selection
    if (territoryArray.includes(selectedTerritory)) {

        territoryName.innerText = selectedTerritory;

        if (showUpdatedTroopCount) {
            troopCount.innerText = updatedTroopCount;
            troopCount.classList.add(".updated-troop-count");
        } else {
            troopCount.innerText = jsonData[selectedTerritory].troops;
            troopCount.classList.remove(".updated-troop-count");
        }
    }

    // Update json display
    document.querySelector("#json-textarea").value = JSON.stringify(jsonData);
}

updateMap();