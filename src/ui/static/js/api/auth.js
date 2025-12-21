export async function login(password) {
    const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
    });

    const data = await res.json();
    return { res, data };
}

export async function logout() {
    const res = await fetch("/api/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    return { res, data };
}