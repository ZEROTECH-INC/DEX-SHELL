// ui_renderer.js
// Light helper functions used by QML's JavaScript context (imported via Qt.createQmlObject or directly in QML)

function formatPercent(value) {
    return (Math.round(value * 100) / 100) + "%";
}

function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
}

// simple animation helper
function pulse(t, speed) {
    return 0.5 + 0.5 * Math.sin(t * speed);
}