import { logout } from "../api/auth.js";

console.log(import.meta.url);
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