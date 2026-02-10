import { login } from "../api/auth_api.js"

const form = document.querySelector("#loginForm");

form.addEventListener("submit", async e => {
    e.preventDefault();

    const password = form.password.value;

    let res, data;
    try {
        ({ res, data } = await login(password));
    } catch (e) {
        alert("네트워크 오류");
        return;
    }

    if (res.status === 401) {
        alert("비밀번호가 틀렸습니다.");
        form.password.value = "";
        form.password.focus();
        return;
    }

    if (res.status !== 200) {
        alert(data.message || "서버 오류");
        return;
    }

    location.href = "/admin";
});