function nueva_visita(id) {
    if (confirm('Esta seguro que desea añadir una nueva visita?')) {
        fetch(`http://127.0.0.1:8000/visita/${id}/`, { method: 'POST' });
        alert('Visita agregada');
    }
}