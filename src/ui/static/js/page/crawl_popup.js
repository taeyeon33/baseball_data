const log = console.log;

const theme = window.opener ? window.opener.document.documentElement.getAttribute("data-bs-theme") : "dark";
document.documentElement.setAttribute("data-bs-theme", theme);

async function startPolling(jobId) {
    const progressBar = document.querySelector("#progressBar");
    const gameCount = document.querySelector("#gameCount");
    const statusText = document.querySelector("#statusText");

    const interval = setInterval(async () => {
        try {
            const res = await fetch(`/api/admin/crawl/job_status/${jobId}`);
            const data = await res.json();
            
            const { percent, count, message, completed } = data;
            
            progressBar.style.width = `${percent}%`;
            gameCount.innerText = count;
            statusText.innerText = message;

            if (percent >= 100) {
                progressBar.classList.remove("progress-bar-animated");
                statusText.classList.remove("text-body-secondary");
                statusText.classList.add("text-success", "fw-bold");
                clearInterval(interval);
            }
        } catch(err) {
            statusText.innerText = "진행률 가져오기 실패: " + err.message;
            clearInterval(interval);
        }
    }, 1000);
};

window.addEventListener("message", e => {
    if (!e.data) return;

    if (e.data.type === "THEME_UPDATE") {
        document.documentElement.setAttribute("data-bs-theme", e.data.theme);
    }

    if (e.data.type === "JOB_ID") {
        const jobId = e.data.jobId;
        startPolling(jobId);
    }
});

window.onload = () => {
    window.opener.postMessage({ type: "POPUP_READY" }, "*");
};