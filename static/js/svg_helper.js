var SVG_NAMESPACE = "http://www.w3.org/2000/svg";

function createCircle(options) {
    var circle = document.createElementNS(SVG_NAMESPACE, "circle");
    circle.setAttribute("cx", options.radius);
    circle.setAttribute("cy", options.radius);
    circle.setAttribute("r", options.radius);
    circle.setAttribute("fill", options.fill);;
    circle.setAttribute("transform", "translate(" + options.translate.x + ", " + options.translate.y + ")");
    return circle;
}