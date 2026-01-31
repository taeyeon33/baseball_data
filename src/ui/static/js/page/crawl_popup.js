const log = console.log;

const theme = window.opener ? window.opener.document.documentElement.getAttribute("data-bs-theme") : "dark";
document.documentElement.setAttribute("data-bs-theme", theme);

window.addEventListener("message", e => {
    if (e.data && e.data.type === "THEME_UPDATE") {
        document.documentElement.setAttribute("data-bs-theme", e.data.theme);
    }
});


export async function updateProgress(percent, count, message) {
    const progressBar = document.querySelector("#progressBar");
    const gameCount = document.querySelector("#gameCount");
    const statusText = document.querySelector("#statusText");

    progressBar.style.width = `${percent}%`;
    gameCount.innerText = count;
    statusText.innerText = message;

    if (percent >= 100) {
        progressBar.classList.remove("progress-bar-animated");
        statusText.classList.remove("text-body-secondary");
        statusText.classList.add("text-success", "fw-bold");
    }
}