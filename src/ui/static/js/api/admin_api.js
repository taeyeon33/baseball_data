import { request } from "./request.js";

export async function fetchAllTables() {
    return request("/api/admin/tables", { method: "POST" });
}

export async function fetchDataList(jsonData) {
    return request("/api/admin/datalist", {
        method: "POST",
        body: jsonData
    });
}

export async function fetchUpdateData(jsonData, type) {
    if (type == "insert") {
        return request("/api/admin/insert", {
            method: "POST",
            body: jsonData
        });
    } else {
        return request("/api/admin/update", {
            method: "POST",
            body: jsonData
        });
    }
}

export async function fetchDeleteData(jsonData) {
    return request("/api/admin/delete", {
        method: "POST",
        body: jsonData
    });
}