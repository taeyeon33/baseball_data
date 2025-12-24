export async function fetchAllTables() {
    const res = await fetch("/api/admin/tables");
    if (!res.ok) throw new Error("failed");
    return res.json();
}

export async function fetchAllPlayers() {
    const res = await fetch("/api/admin/players");
    if (!res.ok) throw new Error("failed");
    return res.json();
}