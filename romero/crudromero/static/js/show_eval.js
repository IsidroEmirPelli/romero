function show_evaluation( eval, fecha, hora, intervencion, motivo_consulta, tratamiento_psicofarm){
    h5 = document.querySelector('#exampleModalLabel');
    h5.textContent = `Visita - ${fecha} ${hora}`;

    body = document.querySelector('#modal-body-show');
    body.innerHTML = `
    <form style="background-color: white">
        <label for="tratamiento_psicofarm_show">Tratamiento psicofarmacológico</label>
        <textarea
            class="form-control mb-2"
            name="tratamiento_psicofarm_show"
            id="tratamiento_psicofarm_show"
            rows="2"
            disabled
        >${ tratamiento_psicofarm }</textarea>
        <label for="intervencion_show">Intervención</label>
        <input
            id="intervencion_show"
            type="text"
            class="form-control col-md-3 mb-2"
            name="intervencion"
            value="${ intervencion }"
            disabled
        />
        <label for="motivo_consulta">Motivo de consulta</label>
        <input
            id="motivo_consulta_show"
            type="text"
            class="form-control col-md-3 mb-2" 
            name="motivo_consulta"
            required
            disabled
            value="${ motivo_consulta }"
        />
        <label for="evaluacion">Evaluación al día de la fecha</label>
        <textarea 
            id="evaluacion_show"
            class="form-control mb-2"
            name="evaluacion" 
            rows="3" 
            disabled>${ eval }</textarea>
        </form>
    `
}
