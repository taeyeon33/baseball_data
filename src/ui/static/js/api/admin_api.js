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
        throw new Error(`${res.status} ${text}`);
    }

    return res.json();
}

export async function fetchAllTables() {
    return request("/api/admin/tables", { method: "POST" });
}

export async function fetchAllPlayers() {
    return request("/api/admin/players", { method: "POST" });
}

export async function fetchInsertData(jsonData) {
    return request("/api/admin/insert", {
        method: "POST",
        body: jsonData
    });
}