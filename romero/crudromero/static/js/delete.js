function delete_elem(id) {
    if (confirm('Está seguro de que desea eliminar a este paciente?')) {
        fetch(`http://127.0.0.1:8000/eliminar/${id}`, { method: 'DELETE' });
        document.getElementById(id).className += 'd-none';
    }
}