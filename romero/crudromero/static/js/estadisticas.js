

// const torta_internados = document.getElementById('torta-internados');
// const torta_pacientes_total_internados = document.getElementById('torta-pacientes-total-internados');
// const torta_pacientes_por_derivacion = document.getElementById('torta-pacientes-por-derivacion');
// const torta_por_region_sanitaria = document.getElementById('torta-por-region-sanitaria');
// const torta_por_barrio = document.getElementById('torta-por-barrio');
// const get_days_data = document.getElementById('get-days-data');

function randomsColors (size){
    const colors = [];
    while (colors.length != size) {
        let color = '#'+Math.floor(Math.random()*16777215).toString(16);
        if (!colors.includes(color)) {
            colors.push(color); 
        }
    }
    return colors; 
}



function makeCharts(json, id) {
    const data = JSON.parse(json);
    const colors = randomsColors(data.labels.length);
    const elem = document.getElementById(id);
    const PieChart = new Chart(elem, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.data,
                hoverOffset: 4,
                backgroundColor: colors,
                borderColor: '#ded8d8',
            }],
        },
    });
}

function makeCharts2(json, id) {
    const data = JSON.parse(json);
    const colors = randomsColors(data.labels.length);
    const elem = document.getElementById(id);
    const BarChart = new Chart(elem, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Pacientes por día',
                data: data.data,
                hoverOffset: 4,
                backgroundColor: colors,
                borderColor: 'black',
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                }
            }
        }
    });
}


function makeChartBarrio(json, id) {
    const data = JSON.parse(json);
    const colors = randomsColors(data.labels.length);
    const elem = document.getElementById(id);
    const PieChart = new Chart(elem, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.data,
                hoverOffset: 4,
                backgroundColor: colors,
                borderColor: '#ded8d8',
            }],
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                }
            }
        }
    });
}