const log = console.log;

// 컬러 템플릿
const html = document.documentElement;
const prefersColor = window.matchMedia("(prefers-color-scheme: dark)").matches;
let nowTheme = "dark";

if (!prefersColor) {
    html.setAttribute("data-bs-theme", "dark");
    nowTheme = "dark";
} else {
    html.setAttribute("data-bs-theme", "light");
    nowTheme = "light";
}

const themeBtn = document.querySelector("#themeBtn");
themeBtn.addEventListener("click", e => {
    if (nowTheme == "dark") {
        html.setAttribute("data-bs-theme", "light");
        nowTheme = "light";
    } else if (nowTheme == "light") {
        html.setAttribute("data-bs-theme", "dark");
        nowTheme = "dark";
    }
});

// header 버튼
const indexBtn = document.querySelector("#indexBtn");
if (indexBtn) {
    indexBtn.addEventListener("click", e => {
        location.href = "/";
    });
}

const adminBtn = document.querySelector("#adminBtn");
if (adminBtn) {
    adminBtn.addEventListener("click", e => {
        location.href = "/admin";
    });
}

// index.html 탭 버튼
const tabs = [
    {
        btn: document.querySelector("#battingBtn"),
        table: document.querySelector("#battingTable"),
    },
    {
        btn: document.querySelector("#pitchingBtn"),
        table: document.querySelector("#pitchingTable"),
    },
];

tabs.forEach((tab, idx) => {
    if (tab.btn == null) return;
    tab.btn.addEventListener("click", e => {
        if (tab.btn.classList.contains("active")) return;
        activeTab(idx);
    });
});

function activeTab(activeIdx) {
    tabs.forEach((tab, idx) => {
        const isActive = idx === activeIdx;
        tab.btn.classList.toggle("active", isActive);
        tab.table.classList.toggle("active", isActive);
    });
}