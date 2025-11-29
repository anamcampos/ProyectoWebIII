async function loadEvents() {
  const container = document.getElementById("calendar-container");
  container.innerHTML = "Cargando...";

  try {
    const response = await fetch("/static/data/events.json");
    const events = await response.json();

    container.innerHTML = "";

    events.forEach(ev => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <strong>${ev.event_type.toUpperCase()}</strong><br>
        Item ID: ${ev.item_id}<br>
        <small>${ev.created_at}</small><br>
        <pre>${JSON.stringify(ev.details, null, 2)}</pre>
      `;
      container.appendChild(div);
    });

  } catch (err) {
    container.innerHTML = "Error cargando eventos.";
  }
}

loadEvents();