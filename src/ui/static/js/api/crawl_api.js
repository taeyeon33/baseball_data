import { request } from "./request.js";

export function crawlGames(jsonData) {
    return request("/api/admin/crawl/games", {
        method: "POST",
        body: jsonData
    });
}

export function getCrawlStatus(jobId) {
    return request(`/api/admin/crawl/status?job_id=${jobId}`, {
        method: "GET"
    });
}