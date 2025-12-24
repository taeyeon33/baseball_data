import { fetchAllTables, fetchAllPlayers } from "../api/admin_api.js";
import { logout } from "../api/auth.js";

let tableList = [];

class Admin {
    constructor() {
        this.tableList = [];

        this.nowTab = "players";
        this.tableMenuList = [
            "players", "player_names", "player_team_history", "player_positions",
            "leagues", "seasons", "stadiums", "positions", "details", "detail_translations",
            "games", "scores"
        ]

        this.dataModalList = [];

        this.modalState = "";

        this.init();
    }

    async init() {
        let tables = await fetchAllTables();
        if (typeof tables == "string") tables = JSON.parse(tables);
        this.tableList = tables;
        console.log(this.tableList);

        this.logoutEvent();
        
        this.renderTab();
        this.modalEvent();
        // this.loadFilterModal();
    }

    renderTab() {
        const { tableMenuList } = this;

        const navTabs = document.querySelector("#navTabs");
        navTabs.innerHTML = "";

        tableMenuList.forEach(menu => {
            // const table = tableList[name];
            this.tabItemDom(menu);
        });

        this.loadPlayers();
        this.loadDataModal("players");
    }

    tabItemDom(menu) {
        const navTabs = document.querySelector("#navTabs");

        const li = document.createElement("li");
        li.classList.add("nav-item");
        const button = document.createElement("button");
        button.classList.add("nav-link", "px-3");
        if (menu == "players") button.classList.add("active");
        let text = menu;
        if (menu.indexOf("_") != -1) text = `${menu.slice(0, 1)}_${menu.split("_")[1]}`;
        button.innerHTML = text;
        li.appendChild(button);
        navTabs.appendChild(li);

        this.tabEvent(button, menu);
    }

    tabEvent(button, menu) {
        const tableTitle = document.querySelector("#currentTableTitle");
        const modalTitle = document.querySelector("#modalTitle");
        
        button.addEventListener("click", e => {
            const tabBtnList = document.querySelectorAll("#navTabs .nav-link");
            tabBtnList.forEach(item => { item.classList.remove("active"); });
            e.target.classList.add("active");
            this.nowTab = menu;
            tableTitle.innerHTML = e.target.innerHTML;
            modalTitle.innerHTML = e.target.innerHTML;
            this.loadDataModal(menu);
            this.renderTable();
        });
    }

    loadDataModal(menu) {
        const { tableList } = this;
        console.log(this.nowTab);
        console.log(this.tableList[menu]);

        const data = tableList[menu];

        const modalForm = document.querySelector("#modalForm .row");
        modalForm.innerHTML = "";

        data.forEach(col => {
            // if (col.name.indexOf("id") != -1) return;
            const div = document.createElement("div");
            div.classList.add("col-md-4");
            const label = document.createElement("label");
            label.classList.add("form-label", "text-body-secondary", "small");
            label.setAttribute("for", col.name);
            label.innerHTML = col.name;
            const input = document.createElement("input");
            input.classList.add("form-control");
            input.id = col.name;
            if (col.type == "TEXT") input.type = "TEXT";
            else if (col.type == "INTEGER") input.type = "number";

            div.appendChild(label);
            div.appendChild(input);
            modalForm.appendChild(div);
        });
    }

    modalEvent() {
        const dataModal = document.querySelector("#dataModal");
        const dataInsertBtn = document.querySelector("#dataInsertBtn");
        const closeBtn = document.querySelector("#closeBtn");
        const cancelBtn = document.querySelector("#cancelBtn");
        const updateBtn = document.querySelector("#updateBtn");

        dataInsertBtn.addEventListener("click", e => {
            dataModal.style.display = "flex";
            this.modalState = "insert";
        });

        closeBtn.addEventListener("click", e => {
            dataModal.style.display = "none";
        });

        cancelBtn.addEventListener("click", e => {
            e.preventDefault();
            const inputs = document.querySelectorAll("#modalForm input");
            inputs.forEach(input => { input.value = ""; });
            dataModal.style.display = "none";
        });

        updateBtn.addEventListener("click", e => {
            e.preventDefault();
            if (this.modalState === "insert") this.insertData();
            else if (this.modalState === "update") this.updateData();
        });
    }

    // 테이블 로딩
    async loadPlayers() {
        const players = await fetchAllPlayers();
        this.renderTable(players);
    }

    renderTable(dataList) {
        console.log("render table", dataList);
    }

    // 로그아웃 이벤트
    logoutEvent() {
        const logoutBtn = document.querySelector("#logoutBtn");
        logoutBtn.addEventListener("click", async e => {
            e.preventDefault();

            let res, data;
            try {
                ({ res, data } = await logout());
            } catch (e) {
                alert("네트워크 오류");
                return;
            }

            if (res.status !== 200) {
                alert(data.message || "서버 오류");
                return;
            }

            location.href = "/"
        });
    }
}

const admin = new Admin();

// async function loadTables() {
//     let data = await fetchAllTables();
//     if (typeof data == "string") data = JSON.parse(data);
//     tableList = data;
// }

// console.log(tableList);

// async function loadPlayers() {
//     const players = await fetchAllPlayers();
//     renderTable(players);
// }

// loadTables();
// loadPlayers();

// const tableThead = document.querySelector("#tableThead");
// const tableTbody = document.querySelector("#tableTbody");

// function renderTabs(tableList) {
//     if (typeof tableList == "string") tableList = JSON.parse(tableList);
//     console.log(tableList);
// }

// function renderTable(dataList) {
//     console.log(dataList);
// }

// const currentTableTitle = document.querySelector("#currentTableTitle");
// const dataInsertBtn = document.querySelector("#dataInsertBtn");

// const dataModal = document.querySelector("#dataModal");
// const modalTitle = document.querySelector("#modalTitle");
// const closeBtn = document.querySelector("#closeBtn");
// const modalForm = document.querySelector("#modalForm");
// const cancelBtn = document.querySelector("#cancelBtn");
// const updateBtn = document.querySelector("#updateBtn");

// dataInsertBtn.addEventListener("click", e => {
//     dataModal.style.display = "flex";
//     modalTitle.innerHTML = "선수 추가";
// });

// closeBtn.addEventListener("click", e => {
//     dataModal.style.display = "none";
// });

// cancelBtn.addEventListener("click", e => {
//     const inputs = document.querySelectorAll("#modalForm input");
//     inputs.forEach(input => { input.value = ""; });
//     dataModal.style.display = "none";
// });

// updateBtn.addEventListener("click", e => {
//     e.preventDefault();
// });


// const logoutBtn = document.querySelector("#logoutBtn");
// logoutBtn.addEventListener("click", async e => {
//     e.preventDefault();

//     let res, data;
//     try {
//         ({ res, data } = await logout());
//     } catch (e) {
//         alert("네트워크 오류");
//         return;
//     }

//     if (res.status !== 200) {
//         alert(data.message || "서버 오류");
//         return;
//     }

//     location.href = "/"
// });