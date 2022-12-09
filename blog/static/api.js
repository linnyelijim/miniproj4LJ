const getGames = async (id) => {
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
            //const minPlayers = game.querySelector("minplayers").getAttribute("value");
            const maxPlayers = game.querySelector("maxplayers").getAttribute("value");
            //const minPlayTime = game.querySelector("minplaytime").getAttribute("value");
            //const maxPlayTime = game.querySelector("maxplaytime").getAttribute("value");

            return {name, id, description, yearPublished, maxPlayers}
        });
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
        let description = createElemWithText('td', game.description);
        let published = createElemWithText('td', game.yearPublished);
        let players = createElemWithText('td', game.maxPlayers);

        tableRow.append(name, id, description, published, players);
        fragment.append(tableRow);
    }
    return fragment;
}

const listGames = async (games) => {
    const gameInfo = document.querySelector("#game-table");
    let element = (games) ? await createGames(games) : document.querySelector("#gameInfo p")
    gameInfo.append(element);
    return element;
}
/** const getId = async (id) => {
    const xmlResponse = await fetch(`https://boardgamegeek.com/xmlapi2/thing?id=${id}`);
    const xml = await xmlResponse.text();
    const parser = new DOMParser();
    const xmlDOM = parser.parseFromString(xml, "application/xml");
    const allGames = [266192, 156129, 1927, 13]
    let section = xmlDOM.getElementById("gameCards");
    let classes = xmlDOM.getElementsByClassName("card");
    let classList = [];
    for (let i = 0; i < classes.length; i++) {
        classList.push(classes[i]);
    }


    for (let i = 0; i < allGames.length; i++) {
        if (classList[i].id === allGames[i]) {
            let game = await getGames(allGames[i]);
            await listGames(game);
        }
    }
}
 */

const hydrateUI = async () => {
    const allGames = [266192, 156129, 1927, 13];
    for (let i = 0; i < allGames.length; i++) {
        let game = await getGames(allGames[i]);
        await listGames(game);
    }
}

hydrateUI();

