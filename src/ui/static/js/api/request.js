export async function request(url, options = {}) {
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