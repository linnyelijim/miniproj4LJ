function createElemWithText(elemType = "p", textContent = "") {
    const myElem = document.createElement(elemType);
    myElem.textContent = textContent;

    return myElem;
}
const getGames = async (id) => {
    try {
        const response = await fetch(`https://boardgamegeek.com/xmlapi2/hot?id=${id}`);
        return await response.json();
    } catch (e) {
        console.log(e);
    }
}
const createGames = async (boardgames) => {
    let fragment = document.createDocumentFragment();

    for(let i = 0; i < boardgames.length; i++) {
        let game = boardgames[i];
        let module = document.createElement('module');

        let h2 = createElemWithText('h2', game.name);
        let p = createElemWithText('p', game.item['rank']);
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
