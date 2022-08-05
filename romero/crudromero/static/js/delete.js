function delete_elem(id) {
    fetch(`http://127.0.0.1:8000/eliminar/${id}`, { method: 'DELETE' });
}