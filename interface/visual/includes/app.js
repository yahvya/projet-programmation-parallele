"use strict";
const filesZone = document.querySelector(".files-list-container");
const filesContainer = filesZone.querySelector(".files");
const downloadZone = document.querySelector(".download-zone");
const filesToDownloadList = downloadZone.querySelector(".files");
const filesMessage = downloadZone.querySelector(".message");
const downloadButton = filesZone.querySelector(".btn");
const requestConfig = {
    "files-list-get-link": "http://127.0.0.1:6060/get-files",
    "get-files-to-download-link": "http://127.0.0.1:6060/files-to-download"
};
fetch(requestConfig["files-list-get-link"], { method: "POST" })
    .then(response => response.json())
    .then(data => {
    data.files.forEach((file) => {
        const card = document.createElement("div");
        card.classList.add("card", "col-sm-3", "p-2");
        card.innerHTML = `
              <img src="./ressources/file-icon.png" class="card-img-top m-auto">
              <div class="card-body">
                <p class="card-text text-center">${file.path}</p>
                <input class="form-check-input m-auto d-block p-3" type="checkbox" name="files[]" value="${file.path}">
              </div>
            `;
        filesContainer.append(card);
        downloadButton.classList.remove("d-none");
        downloadButton.classList.add("d-block");
    });
    filesZone.classList.remove("placeholder");
})
    .catch(err => filesMessage.textContent = "Echec de récupération de la liste des fichiers, veuillez recharger la page");
filesZone.addEventListener("submit", (submitEvent) => {
    Array.from(filesToDownloadList.children).forEach(child => child.remove());
    downloadZone.classList.add("placeholder");
    filesMessage.classList.add("d-none");
    submitEvent.preventDefault();
    const options = {
        method: "POST",
        body: new FormData(filesZone)
    };
    fetch(requestConfig["get-files-to-download-link"], options)
        .then(response => response.json())
        .then(data => {
        const files = data.files;
        for (const filepath in files) {
            const blob = new Blob([files[filepath]], { type: "text/plain" });
            const downloadLink = URL.createObjectURL(blob);
            const downloadButton = document.createElement("a");
            downloadButton.classList.add("btn", "btn-primary", "d-block", "m-auto", "mb-3");
            downloadButton.href = downloadLink;
            downloadButton.download = filepath;
            downloadButton.textContent = `Télécharger : ${filepath}`;
            filesToDownloadList.append(downloadButton);
        }
        downloadZone.classList.remove("placeholder");
    })
        .catch(err => {
        downloadZone.classList.remove("placeholder");
        filesMessage.classList.remove("d-none");
        filesMessage.textContent = "Echec de récupération des fichiers à télécharger";
    });
});
