async function loadResults() {
  const container = document.getElementById("results-container");
  container.innerHTML = "Cargando...";

  try {
    const response = await fetch("/api/items");
    const data = await response.json();

    container.innerHTML = "";

    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>${item.title}</h3>
        <p><strong>Precio:</strong> ${item.price}</p>
        <a href="${item.url}" target="_blank">Ver libro</a>
      `;
      container.appendChild(div);
    });

  } catch (err) {
    container.innerHTML = "Error cargando resultados.";
  }
}

loadResults();