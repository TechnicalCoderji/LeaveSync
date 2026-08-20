
    const profileMenu = document.getElementById("profileMenu");
    const profileTrigger = document.getElementById("profileTrigger");
    profileTrigger.addEventListener("click", function (event) {
        event.stopPropagation();
        profileMenu.classList.toggle("open");
        const isOpen = profileMenu.classList.contains("open");
        profileTrigger.setAttribute(
            "aria-expanded",
            isOpen
        );
    });

    document.addEventListener("click", function (event) {
        if (!profileMenu.contains(event.target)) {
            profileMenu.classList.remove("open");
            profileTrigger.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            profileMenu.classList.remove("open");
            profileTrigger.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    });
