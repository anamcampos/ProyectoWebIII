async function loadItems(){
  const res = await fetch('/api/items');
  if (!res.ok) {
    document.getElementById('items').innerText = "Error cargando items";
    return;
  }
  const items = await res.json();
  const container = document.getElementById('items');
  container.innerHTML = '';
  if (items.length === 0) {
    container.innerText = "No hay items en la DB (ejecuta el scraper primero).";
    return;
  }
  for (const it of items) {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `<strong>${it.title}</strong><div>${it.price}</div><a href="${it.url}" target="_blank">Ver</a>`;
    container.appendChild(div);
  }
}

loadItems();
