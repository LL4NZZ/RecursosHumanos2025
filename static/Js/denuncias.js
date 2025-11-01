// Variable para almacenar todas las denuncias
let denuncias = [];
const KEY_DENUNCIAS = 'denuncias_app';

// Referencias a elementos del DOM
const pendientesColumna = document.getElementById('pendientes');
const aprobadasColumna = document.getElementById('aprobadas');
const rechazadasColumna = document.getElementById('rechazadas');
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modalTitle');
const formDenuncia = document.getElementById('formDenuncia');
const editIndexInput = document.getElementById('editIndex');
const tituloInput = document.getElementById('titulo');
const descripcionInput = document.getElementById('descripcion');
const fechaInput = document.getElementById('fecha');
const filtroFechaInput = document.getElementById('filtroFecha');

// Cargar denuncias del almacenamiento local al inicio
document.addEventListener('DOMContentLoaded', () => {
    const data = localStorage.getItem(KEY_DENUNCIAS);
    if (data) {
        denuncias = JSON.parse(data);
        renderizarDenuncias(denuncias);
    }
});

// Función para guardar las denuncias en el almacenamiento local
const guardarDenuncias = () => {
    localStorage.setItem(KEY_DENUNCIAS, JSON.stringify(denuncias));
};

// Función para renderizar una denuncia como una tarjeta
const crearTarjetaDenuncia = (denuncia, index) => {
    const card = document.createElement('div');
    card.className = 'denuncia-card';
    card.draggable = true;
    card.dataset.index = index;

    card.innerHTML = `
        <h4>${denuncia.titulo}</h4>
        <p>${denuncia.descripcion}</p>
        <small>Fecha: ${denuncia.fecha}</small>
        <div class="card-acciones">
            <button class="btn-editar" onclick="editarDenuncia(${index})">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn-eliminar" onclick="eliminarDenuncia(${index})">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;

    return card;
};

// Función para renderizar todas las denuncias en las columnas correspondientes
const renderizarDenuncias = (listaDenuncias) => {
    // Limpiar columnas
    pendientesColumna.innerHTML = '<h2>Pendientes</h2>';
    aprobadasColumna.innerHTML = '<h2>Aprobadas</h2>';
    rechazadasColumna.innerHTML = '<h2>Rechazadas</h2>';

    // Agregar las tarjetas a las columnas correctas
    listaDenuncias.forEach((denuncia, index) => {
        const tarjeta = crearTarjetaDenuncia(denuncia, index);
        if (denuncia.estado === 'pendiente') {
            pendientesColumna.appendChild(tarjeta);
        } else if (denuncia.estado === 'aprobada') {
            aprobadasColumna.appendChild(tarjeta);
        } else if (denuncia.estado === 'rechazada') {
            rechazadasColumna.appendChild(tarjeta);
        }
    });

    // Agregar manejadores de eventos de arrastrar y soltar a las tarjetas
    agregarEventosArrastrarYSoltar();
};

// Manejar el envío del formulario para agregar/editar
formDenuncia.addEventListener('submit', (e) => {
    e.preventDefault();
    const titulo = tituloInput.value;
    const descripcion = descripcionInput.value;
    const fecha = fechaInput.value;
    const editIndex = editIndexInput.value;

    if (editIndex === '') {
        // Modo Agregar
        const nuevaDenuncia = {
            titulo,
            descripcion,
            fecha,
            estado: 'pendiente'
        };
        denuncias.push(nuevaDenuncia);
    } else {
        // Modo Editar
        denuncias[editIndex].titulo = titulo;
        denuncias[editIndex].descripcion = descripcion;
        denuncias[editIndex].fecha = fecha;
    }

    guardarDenuncias();
    renderizarDenuncias(denuncias);
    cerrarModal();
});

// Función para abrir el modal
const abrirModal = (index = '') => {
    if (index === '') {
        modalTitle.textContent = 'Nueva Denuncia';
        formDenuncia.reset();
        editIndexInput.value = '';
    }
    modal.style.display = 'flex';
};

// Función para editar una denuncia
const editarDenuncia = (index) => {
    const denuncia = denuncias[index];
    modalTitle.textContent = 'Editar Denuncia';
    tituloInput.value = denuncia.titulo;
    descripcionInput.value = denuncia.descripcion;
    fechaInput.value = denuncia.fecha;
    editIndexInput.value = index;
    abrirModal(index);
};

// Función para eliminar una denuncia
const eliminarDenuncia = (index) => {
    if (confirm('¿Estás seguro de que quieres eliminar esta denuncia?')) {
        denuncias.splice(index, 1);
        guardarDenuncias();
        renderizarDenuncias(denuncias);
    }
};

// Función para cerrar el modal
const cerrarModal = () => {
    modal.style.display = 'none';
};

// Lógica de filtrado por fecha
const filtrarDenuncias = () => {
    const fecha = filtroFechaInput.value;
    if (fecha) {
        const denunciasFiltradas = denuncias.filter(d => d.fecha === fecha);
        renderizarDenuncias(denunciasFiltradas);
    } else {
        mostrarTodas();
    }
};

// Función para mostrar todas las denuncias
const mostrarTodas = () => {
    filtroFechaInput.value = '';
    renderizarDenuncias(denuncias);
};

// Lógica de arrastrar y soltar
let draggedItem = null;

const agregarEventosArrastrarYSoltar = () => {
    const cards = document.querySelectorAll('.denuncia-card');
    cards.forEach(card => {
        card.addEventListener('dragstart', () => {
            draggedItem = card;
            setTimeout(() => card.classList.add('dragging'), 0);
        });
        card.addEventListener('dragend', () => {
            draggedItem.classList.remove('dragging');
            draggedItem = null;
        });
    });

    const columnas = document.querySelectorAll('.columna');
    columnas.forEach(columna => {
        columna.addEventListener('dragover', (e) => {
            e.preventDefault();
        });
        columna.addEventListener('drop', (e) => {
            e.preventDefault();
            if (draggedItem) {
                const targetColumna = e.target.closest('.columna');
                if (targetColumna && targetColumna !== draggedItem.parentNode) {
                    targetColumna.appendChild(draggedItem);
                    actualizarEstado(draggedItem.dataset.index, targetColumna.id);
                }
            }
        });
    });
};

// Función para actualizar el estado de la denuncia después de arrastrar y soltar
const actualizarEstado = (index, columnaId) => {
    const denuncia = denuncias[index];
    if (columnaId === 'pendientes') {
        denuncia.estado = 'pendiente';
    } else if (columnaId === 'aprobadas') {
        denuncia.estado = 'aprobada';
    } else if (columnaId === 'rechazadas') {
        denuncia.estado = 'rechazada';
    }
    guardarDenuncias();
};