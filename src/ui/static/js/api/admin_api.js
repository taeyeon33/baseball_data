async function request(url, options = {}) {
    const fetchOptions = {
        method: options.method || "GET",
        headers: {},
    }

    if (options.body !== undefined) {
        fetchOptions.headers["Content-Type"] = "application/json";
        fetchOptions.body = JSON.stringify(options.body);
    }

    const res = await fetch(url, fetchOptions);

    if (!res.ok) {
        const text = await res.text();
        alert(`${res.status} ${text}`);
        throw new Error(`${res.status} ${text}`);
    }

    return res.json();
}

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