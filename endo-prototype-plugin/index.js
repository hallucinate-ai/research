

async function exportlayer(image) {
  const storage = window.require("uxp").storage;
  const file = await storage.localFileSystem.getFileForSaving("temp.png");
  await file.write(image);

}
 

function showLayerNames() {
    const app = window.require("photoshop").app;
    const allLayers = app.activeDocument.layers;
    const allLayerNames = allLayers.map(layer => layer.name);
    const alllayerids = allLayers.map(layer => layer.id);
    html = "";
    layerbuttons = "";
    allLayers.forEach(h => layerbuttons += "</div><p><sp-button class=\"layers\" id=\"" + h.name + "\">" + h.name +"</sp-button></p></div>" );
    html += layerbuttons
    console.warn(html);
    document.getElementById("layers").innerHTML = html;
    el = document.getElementById("layers");
    el.getElementsByTagName("sp-button").forEach(function (button) {
            button.addEventListener("click", function () {
                console.warn("clicked " + button.id);
                selectLayer(button.id);
            });
      console.warn(el.innerHTML);
    });
}
showLayerNames()

console.error("foo error");
console.warn("foo log");
document.getElementById("btnPopulate").addEventListener("click", showLayerNames);

function selectLayer(layerName) {
    const app = window.require("photoshop").app;
    const allLayers = app.activeDocument.layers;
    findlayer = allLayers.find(layer => layer.name === layerName);
    exportlayer();
}

