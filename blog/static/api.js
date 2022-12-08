const getGames = async (id = 266192) => {
    try {
        const xmlResponse = await fetch(`https://boardgamegeek.com/xmlapi2/thing?id=${id}`);
        const xml = await xmlResponse.text();
        const parser = new DOMParser();
        const xmlDOM = parser.parseFromString(xml, "application/xml");
        const games = xmlDOM.querySelectorAll("item");
        const gameArray = Array.from(games).map(game => {
            const name = game.querySelector("name").getAttribute("value");
            const id = game.getAttribute("id");
            const description = game.querySelector("description").textContent;
            const yearPublished = game.querySelector("yearpublished").getAttribute("value");
            const minPlayers = game.querySelector("minplayers").getAttribute("value");
            const maxPlayers = game.querySelector("maxplayers").getAttribute("value");
            const minPlayTime = game.querySelector("minplaytime").getAttribute("value");
            const maxPlayTime = game.querySelector("maxplaytime").getAttribute("value");
            console.log('name - ', name)
            console.log('id - ', id)
            console.log('description - ', description)
            console.log('yearPublished - ', yearPublished)
            console.log('minPlayers - ', minPlayers)
            console.log('maxPlayers - ', maxPlayers)
            console.log('minPlayTime - ', minPlayTime)
            console.log('maxPlayTime - ', maxPlayTime)
            // const stats = game.querySelector("stats").getAttribute("stats");
            // use and return whatever you want
        })
        return gameArray;
    } catch (e) {
        console.log(e);
    }
}

const createElemWithText = (elemType = "p", textContent = "") => {
    const myElem = document.createElement(elemType);
    myElem.textContent = textContent;

    return myElem;
}

const createGames = async (games) => {
    let fragment = document.createDocumentFragment();

    for (let i = 0; i < games.length; i++) {
        let game = games[i];
        let tableRow = document.createElement('tr');

        let id = createElemWithText('td', game.id);
        let name = createElemWithText('td', game.name);
        // let stats = createElemWithText('td', game.stats);

        tableRow.append(name, id);
        fragment.append(tableRow)
    }
    return fragment;
}

const listGames = async (games) => {
    const gameInfo = document.querySelector("#game-table");
    let element = (games) ? await createGames(games) : document.querySelector("#gameInfo p")
    gameInfo.append(element);
    return element;
}

const hydrateUI = async () => {
    const games = await getGames()
    await listGames(games)
}

hydrateUI()
