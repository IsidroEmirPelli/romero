function show_evaluation(eval, fecha, hora){
    h5 = document.querySelector('#exampleModalLabel');
    h5.textContent = `Evaluación - ${fecha} ${hora}`;
    p = document.querySelector('#content');
    p.textContent = eval;
}