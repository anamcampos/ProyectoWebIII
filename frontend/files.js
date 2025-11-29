async function loadFiles() {
  const container = document.getElementById("files-container");
  container.innerHTML = "Cargando...";

  try {
    const response = await fetch("/static/data/files.json");
    const data = await response.json();

    container.innerHTML = "";

    data.forEach(file => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>${file.file_name}</h3>
        <p><strong>Checksum:</strong> ${file.sha256}</p>
        <p><strong>Versión:</strong> ${file.version}</p>
      `;
      container.appendChild(div);
    });

  } catch (err) {
    container.innerHTML = "Error cargando archivos.";
  }
}