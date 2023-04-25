if (localStorage.getItem("token") === "authen"){
    window.location.href = "../page/chatboard.html";
}
else if (localStorage.getItem("token") == null) {
    window.location.href = "../page/registry.html";
}