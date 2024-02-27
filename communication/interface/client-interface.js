const fileSelectionForm = document.querySelector(".file-selector-zone");
const fileListContainer = document.querySelector(".file-list");
const includeLogChecker = document.querySelector(".include-log");


// récupération de la liste des fichiers et affichage
loadFilesList()
    .then(filesList => {
        // affichage des fichiers reçus
        filesList.forEach((fileDatas,index) => {
            // affichage du fichier
            const fileContainer = document.createElement("label");
            const image = document.createElement("img");
            const title = document.createElement("p");
            const input = document.createElement("input");

            image.alt = "Icone du fichier";
            image.src = "./resources/file-icon.png";

            title.textContent = fileDatas.path;
            title.classList.add("small-title");

            input.id = `files${index}`;
            input.type = "checkbox";
            input.name = "files";
            input.value = fileDatas.name;

            fileContainer.setAttribute("for",`files${index}`);
            fileContainer.classList.add("file");
            fileContainer.append(image,title,input);

            // ajout dans le conteneur
            fileListContainer.append(fileContainer);
        });

        fileListContainer.classList.remove("loading");
    })
    .catch(error => alert(`${error} - Veuillez recharger la page :(`));

// évènement de validation des fichiers à récupérer
fileSelectionForm.addEventListener("submit",(submitEvent) => {
    submitEvent.preventDefault();

    const form = new FormData(fileSelectionForm);
});

/**
 * charge la liste des fichiers
 * @returns {Promise<Array>} promesse avec en argument la liste des fichiers récupéré
 */
function loadFilesList() {
    return new Promise((resolve, reject) => {
        const form = new FormData();

        form.append("include-log",includeLogChecker.checked);

        const options = {
            method: "POST",
            body: form
        };

        fetch("http://127.0.0.1:8000/get-files-list", options)
            .then(response => response.json())
            .then(filesList => resolve(filesList))
            .catch(error => reject("Une erreur s'est produite lors de la récupération des fichiers"));
    });
}