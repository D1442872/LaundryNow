console.log("LaundryNow preview loaded");

document.querySelectorAll(".card").forEach(function(card) {
    card.addEventListener("mouseenter", function() {
        card.style.transform = "translateY(-4px)";
        card.style.transition = "0.2s";
    });

    card.addEventListener("mouseleave", function() {
        card.style.transform = "translateY(0)";
    });
});
