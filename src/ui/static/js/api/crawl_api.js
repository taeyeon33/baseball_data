import { request } from "./request.js";

export function crawlGames(jsonData) {
    return request("/api/admin/crawl/games", {
        method: "POST",
        body: jsonData
    });
}