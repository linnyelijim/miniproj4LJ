function createElemWithText(elemType = "p", textContent = "") {
    const myElem = document.createElement(elemType);
    myElem.textContent = textContent;

    return myElem;
}
const getGames = async (id) => {
    try {
        const response = await fetch(`https://boardgamegeek.com/xmlapi2/thing?id=${Id}`);
        return await response.json();
    } catch (e) {
        console.log(e);
    }
}
const createGames = async (games) => {
    let fragment = document.createDocumentFragment();

    for(let i = 0; i < games.length; i++) {
        let game = games[i];
        let module = document.createElement('module');

        let h2 = createElemWithText('h2', game.name);
        let p = createElemWithText('p', game.stats);
        let p2 = createElemWithText('p', `Game ID: ${game.id}`);

        module.append(h2,p,p2);
        fragment.append(module);
    }
    return fragment;
}
const listGames = async (games) => {
    const gameInfo = document.querySelector("#gameInfo");
    let element = (games) ? await createGames(games) : document.querySelector("#gameInfo p")
    gameInfo.append(element);
    return element;
}
