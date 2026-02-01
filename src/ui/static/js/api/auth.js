export async function login(password) {
    const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
    });

    const data = await res.json();
    return { res, data };
}

export async function logout() {
    const res = await fetch("/api/admin/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    return { res, data };
}