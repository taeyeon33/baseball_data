import { fetchAllTables, fetchDataList, fetchUpdateData, fetchDeleteData } from "../api/admin_api.js";
import { logout } from "../api/auth.js";

class Admin {
    constructor() {
        this.tableList = [];

        this.nowTab = "players";
        this.tableMenuList = [
            "players", "player_names", "player_team_history", "player_positions",
            "leagues", "seasons", "stadiums", "positions", "details", "detail_translations",
            "games", "scores"
        ]

        this.dataModal = document.querySelector("#dataModal");
        this.modalState = "";

        this.init();
    }

    async init() {
        let tables = await fetchAllTables();
        if (typeof tables == "string") tables = JSON.parse(tables);
        this.tableList = tables;

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
            this.tabItemDom(menu);
        });

        this.loadTable();
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
            this.loadTable();
        });
    }

    loadDataModal(menu) {
        const { tableList } = this;

        const data = tableList[menu];

        const modalForm = document.querySelector("#modalForm .row");
        modalForm.innerHTML = "";

        data.forEach(col => {
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
            else if (col.type == "date") input.type = "date";
            if (col.notnull) {
                input.placeholder = "필수";
                input.required = true;
            }

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
            this.updateData();
        });
    }

    // 데이터 추가, 변경, 삭제
    async updateData() {
        const jsonData = { "table": this.nowTab };

        const inputs = document.querySelectorAll("#modalForm input");
        inputs.forEach(input => {
            const key = input.id;
            jsonData[key] = input.value.trim();
        });

        const update = await fetchUpdateData(jsonData, this.modalState);
        if (typeof update.message !== "number") {
            alert(update.message);
            return;
        }

        inputs.forEach(input => { input.value = ""; });
        dataModal.style.display = "none";
        this.loadTable();
    }

    async deleteData(data) {
        data["table"] = this.nowTab;

        if (confirm("정말 삭제하시겠습니까?")) {
            const del = await fetchDeleteData(data);
            if (del.message !== 1) alert(del.message);

            this.loadTable();
        }
    }

    // 테이블 로딩
    async loadTable() {
        const jsonData = { "table": this.nowTab };
        const dataList = await fetchDataList(jsonData);
        this.renderTable(dataList);
    }

    renderTable(dataList) {
        const tableThead = document.querySelector("#tableThead");
        tableThead.innerHTML = "";

        this.tableList[this.nowTab].forEach(col => {
            if (col.name === "first_name") col.name = "name";
            if (col.name === "last_name") return;
            if (this.nowTab === "player_names") {
                if (col.name.split("_")[1] === "first") col.name = col.name.split("_")[0] + "_name";
                if (col.name.split("_")[1] === "last") return;
            }
            const th = document.createElement("th");
            th.innerHTML = col.name;
            tableThead.appendChild(th);
        });

        const th = document.createElement("th");
        th.innerHTML = "관리";
        tableThead.appendChild(th);

        const tableTbody = document.querySelector("#tableTbody");
        tableTbody.innerHTML = "";

        if (dataList[0] == undefined) {
            const tr = document.createElement("tr");
            tr.innerHTML = `<td colspan="100">데이터가 존재하지 않습니다.</td>`;
            tableTbody.appendChild(tr);
            return;
        }

        const columns = tableThead.querySelectorAll("th");
        dataList.forEach(data => {
            const tr = document.createElement("tr");
            for (let i = 0; i < columns.length - 1; i++) {
                const td = document.createElement("td");
                const col = columns[i].innerHTML;
                let innerData = data[col];
                if (col === "name") innerData = `${data["last_name"]} ${data["first_name"]}`;
                if (col.indexOf("_name") != -1) innerData = `${data[col.split("_")[0] + "_last_name"]}・${data[col.split("_")[0] + "_first_name"]}`;
                td.innerHTML = innerData;
                tr.appendChild(td);
            }

            const td = document.createElement("td");
            const div = document.createElement("div");
            div.classList.add("d-flex", "justify-content-center", "gap-1");

            const updateBtn = document.createElement("button");
            updateBtn.classList.add("btn", "btn-sm", "btn-outline-primary", "border-0", "p-1");
            updateBtn.innerHTML = `<i class="bi bi-pencil-square"></i>`;

            const deleteBtn = document.createElement("button");
            deleteBtn.classList.add("btn", "btn-sm", "btn-outline-danger", "border-0", "p-1");
            deleteBtn.innerHTML = `<i class="bi bi-trash3-fill"></i>`;

            this.managementBtnEvent(updateBtn, deleteBtn, data);

            div.append(updateBtn, deleteBtn);
            td.appendChild(div);
            tr.appendChild(td);

            tableTbody.appendChild(tr);
        });
    }

    managementBtnEvent(updateBtn, deleteBtn, data) {
        const { dataModal } = this;

        updateBtn.addEventListener("click", e => {
            this.modalState = "update";
            const inputs = document.querySelectorAll("#modalForm input");
            inputs.forEach(input => { input.value = data[input.id]; });

            dataModal.style.display = "flex";
        });

        deleteBtn.addEventListener("click", async e => {
            this.deleteData(data);
        });
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