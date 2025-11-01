document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('asistencia-table-body');
    const noRecordsMessage = document.getElementById('no-records-message');

    // Función para simular la obtención de datos de asistencia
    const fetchAsistenciaData = () => {
        // **TODO: Reemplaza este bloque con una llamada real a tu API de Flask**
        // Ejemplo con fetch():
        // fetch('/api/asistencia/registros')
        //     .then(response => response.json())
        //     .then(data => {
        //         renderTable(data.registros);
        //     })
        //     .catch(error => {
        //         console.error('Error al obtener los registros:', error);
        //         renderTable([]); // Muestra tabla vacía en caso de error
        //     });

        // Datos de ejemplo para simulación
        const simulatedData = [
            { fecha: '2023-10-25', hora_entrada: '09:00 AM', hora_salida: '06:00 PM', estado: 'A tiempo' },
            { fecha: '2023-10-24', hora_entrada: '09:15 AM', hora_salida: '06:00 PM', estado: 'Tardanza' },
            { fecha: '2023-10-23', hora_entrada: '09:00 AM', hora_salida: '06:00 PM', estado: 'A tiempo' },
            { fecha: '2023-10-20', hora_entrada: '09:00 AM', hora_salida: '06:00 PM', estado: 'A tiempo' },
            { fecha: '2023-10-19', hora_entrada: '09:05 AM', hora_salida: '06:00 PM', estado: 'A tiempo' }
        ];

        renderTable(simulatedData);
    };

    // Función para renderizar los datos en la tabla
    const renderTable = (records) => {
        tableBody.innerHTML = ''; // Limpiar registros existentes
        if (records.length === 0) {
            noRecordsMessage.classList.remove('d-none');
        } else {
            noRecordsMessage.classList.add('d-none');
            records.forEach(record => {
                const row = document.createElement('tr');
                let statusClass = '';
                if (record.estado === 'Tardanza') {
                    statusClass = 'table-warning';
                }

                row.innerHTML = `
                    <td>${record.fecha}</td>
                    <td>${record.hora_entrada}</td>
                    <td>${record.hora_salida || 'N/A'}</td>
                    <td class="${statusClass}">${record.estado}</td>
                `;
                tableBody.appendChild(row);
            });
        }
    };

    // Llamar a la función para cargar los datos al iniciar la página
    fetchAsistenciaData();
});