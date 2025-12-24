const points = document.querySelectorAll(".point");

points.forEach(point => {
    point.addEventListener("click", () => {
        const region = point.dataset.region;
        window.location.href = `region.html?region=${encodeURIComponent(region)}`;
    });
});