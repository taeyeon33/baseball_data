import { crawlGames, getCrawlStatus } from "../api/crawl_api.js"

class Flatpickr {
    constructor() {
        this.crawlBtn = document.querySelector("#crawlBtn");
        this.crawlDateInput = document.querySelector("#crawlDate");
        this.fp = null;

        this.theme = document.documentElement.getAttribute("data-bs-theme");

        window.crawlPopup = null;

        this.init();
        this.themeChange();
    }

    init() {
        const { crawlDateInput } = this;
        this.fp = flatpickr(crawlDateInput, {
            mode: "range",
            locale: "ko",
            dateFormat: "Y-m-d",
            defaultDate: [new Date(), new Date()]
        });

        this.crawlEvent();
    }

    crawlEvent() {
        const { crawlBtn, crawlDateInput, fp } = this;
        crawlBtn.addEventListener("click", async e => {
            const selectedDates = fp.selectedDates;
            if (selectedDates.length === 0) return alert("크롤링할 날짜를 선택해주세요.");

            const startDate = this.formatDate(selectedDates[0]);
            const endDate = this.formatDate(selectedDates[1] || selectedDates[0]);
            
            // 팝업 창 열기
            const width = 600;
            const height = 400;
            const left = (window.screen.width / 2) - (width / 2);
            const top = (window.screen.height / 2) - (height / 2);

            window.crawlPopup = window.open(
                "/admin/crawl_popup",
                "CrawlProgress",
                `width=${width},height=${height},top=${top},left=${left},menubar=no,toolbar=no,location=no,status=no,resizable=no,scrollbars=no`
            );
            
            if (!window.crawlPopup) return alert("팝업 차단이 설정되어 있습니다. 팝업 차단을 해제해주세요.");

            try {
                const response = await crawlGames({"start_date": startDate, "end_date": endDate});
                const jobId = response.job_id;

                if (!jobId) return alert("Job 생성 실패");

                window.addEventListener("message", function handler(e) {
                    if (e.data?.type === "POPUP_READY") {
                        window.crawlPopup.postMessage({ type: "JOB_ID", jobId }, "*");
                        window.removeEventListener("message", handler);
                    }
                });
            } catch (err) {
                alert("크롤링 시작 실패: " + err.message);
            }
        });
    }

    themeChange() {
        const themeBtn = document.querySelector("#themeBtn");
        themeBtn.addEventListener("click", e => {
            if (this.theme == "dark") this.theme = "light";
            else if (this.theme == "light") this.theme = "dark";
            localStorage.setItem("theme", this.theme);

            if (window.crawlPopup && !window.crawlPopup.closed) {
                window.crawlPopup.document.documentElement.setAttribute("data-bs-theme", this.theme);
            }
        });
    }

    formatDate(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, "0");
        const d = String(date.getDate()).padStart(2, "0");
        return `${y}-${m}-${d}`;
    }
}

window.onload = () => {
    const flatpickr = new Flatpickr();
};