// ===============================
// Referencias a elementos del DOM
// ===============================
const tableBody = document.getElementById('portfolioTableBody');
const portfolioForm = document.getElementById('portfolioForm');
const createPortfolioBtn = document.getElementById('createPortfolioBtn');
const modalTitle = document.getElementById('modalTitle');
const usuarioSelect = document.getElementById('usuarioSelect');

// ===============================
// Modal de Bootstrap
// ===============================
const portfolioModal = new bootstrap.Modal(document.getElementById('portfolioModal'));

// ===============================
// Variables de estado
// ===============================
let isEditing = false;
let currentPortfolioId = null;

// ===============================
// API Base
// ===============================
const API_URL = "http://localhost:5000/api";

// ===============================
// Función para mostrar alertas
// ===============================
function showAlert(message, type = "success") {
  const alertContainer = document.getElementById("alertContainer");

  // Limpiar alertas anteriores
  alertContainer.innerHTML = "";

  // Crear alerta Bootstrap
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
  alertDiv.role = "alert";
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  alertContainer.appendChild(alertDiv);

  // Ocultar automáticamente después de 4s
  setTimeout(() => {
    if (alertDiv) {
      alertDiv.classList.remove("show");
      setTimeout(() => alertDiv.remove(), 500);
    }
  }, 4000);
}

// ===============================
// Renderizar tabla
// ===============================
function renderTable(carteras) {
  tableBody.innerHTML = '';
  carteras.forEach(cartera => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${cartera.NombreUsuario}</td>
      <td>${cartera.NombreContacto}</td>
      <td>${cartera.TelefonoContacto}</td>
      <td>${cartera.CorreoContacto}</td>
      <td>${cartera.FechaAsignacion}</td>
      <td>
        <div class="d-flex gap-2">
          <button onclick="viewOrders(${cartera.IdCartera})" class="btn btn-sm btn-outline-primary">Ver Pedidos</button>
          <button onclick="editPortfolio(${cartera.IdCartera})" class="btn btn-sm btn-outline-warning">Editar</button>
          <button onclick="deletePortfolio(${cartera.IdCartera})" class="btn btn-sm btn-outline-danger">Eliminar</button>
        </div>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

// ===============================
// Abrir modal (Crear o Editar)
// ===============================
function openModal(edit = false, cartera = null) {
  isEditing = edit;
  modalTitle.textContent = edit ? 'Editar Cartera' : 'Crear Cartera';
  
  portfolioForm.reset();

  if (edit && cartera) {
    currentPortfolioId = cartera.IdCartera;
    usuarioSelect.value = cartera.IdUsuario;
    document.getElementById('nombreContacto').value = cartera.NombreContacto;
    document.getElementById('telefonoContacto').value = cartera.TelefonoContacto;
    document.getElementById('correoContacto').value = cartera.CorreoContacto;

    // Ajustar formato de fecha para datetime-local
    const fecha = cartera.FechaAsignacion 
      ? cartera.FechaAsignacion.replace(" ", "T").slice(0, 16) 
      : "";
    document.getElementById('fechaAsignacion').value = fecha;
  } else {
    currentPortfolioId = null;
  }

  portfolioModal.show();
}

function closeModal() {
  isEditing = false;
  currentPortfolioId = null;
  portfolioModal.hide();
}

// ===============================
// Guardar (Crear o Editar)
// ===============================
portfolioForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("IdUsuario", usuarioSelect.value);
  formData.append("NombreContacto", document.getElementById('nombreContacto').value);
  formData.append("TelefonoContacto", document.getElementById('telefonoContacto').value);
  formData.append("CorreoContacto", document.getElementById('correoContacto').value);
  formData.append("FechaAsignacion", document.getElementById('fechaAsignacion').value);

  let url = `${API_URL}/carteras`;
  let method = "POST";

  if (isEditing && currentPortfolioId) {
    url = `${API_URL}/carteras/${currentPortfolioId}`;
    method = "PUT";
  }

  try {
    const resp = await fetch(url, { method, body: formData });
    const data = await resp.json();
    showAlert(data.mensaje || data.error, resp.ok ? "success" : "danger");

    if (resp.ok) {
      closeModal();
      cargarCarteras();
    }
  } catch (error) {
    console.error("Error guardando cartera:", error);
    showAlert("Error al guardar la cartera.", "danger");
  }
});

// ===============================
// Ver pedidos
// ===============================
window.viewOrders = function (id) {
  window.location.href = `/pedido?idCartera=${id}`;
};

// ===============================
// Editar cartera
// ===============================
window.editPortfolio = async function (id) {
  try {
    const resp = await fetch(`${API_URL}/carteras`);
    const carteras = await resp.json();
    const cartera = carteras.find(c => c.IdCartera === id);

    if (cartera) {
      openModal(true, cartera);
    }
  } catch (error) {
    console.error("Error cargando cartera:", error);
    showAlert("No se pudo cargar la cartera.", "danger");
  }
};

// ===============================
// Eliminar cartera
// ===============================
window.deletePortfolio = async function (id) {
  if (confirm("¿Estás seguro de eliminar esta cartera?")) {
    try {
      const resp = await fetch(`${API_URL}/carteras/${id}`, { method: "DELETE" });
      const data = await resp.json();
      showAlert(data.mensaje || data.error, resp.ok ? "success" : "danger");

      if (resp.ok) {
        cargarCarteras();
      }
    } catch (error) {
      console.error("Error eliminando cartera:", error);
      showAlert("Error al eliminar la cartera.", "danger");
    }
  }
};

// ===============================
// Cargar usuarios en el <select>
// ===============================
async function cargarUsuarios() {
  try {
    console.log("📡 Solicitando usuarios...");
    const resp = await fetch(`${API_URL}/usuarios`);
    const usuarios = await resp.json();
    console.log("✅ Usuarios recibidos:", usuarios);

    usuarioSelect.innerHTML = `<option value="">Seleccione un usuario...</option>`;
    usuarios.forEach(u => {
      const opt = document.createElement('option');
      opt.value = u.IdUsuario;
      opt.textContent = u.NombreCompleto;
      usuarioSelect.appendChild(opt);
    });
  } catch (error) {
    console.error("Error cargando usuarios:", error);
    showAlert("No se pudieron cargar los usuarios.", "danger");
  }
}

// ===============================
// Cargar carteras desde API
// ===============================
async function cargarCarteras() {
  try {
    console.log("📡 Solicitando carteras...");
    const resp = await fetch(`${API_URL}/carteras`);
    const carteras = await resp.json();
    console.log("✅ Carteras recibidas:", carteras);
    renderTable(carteras);
  } catch (error) {
    console.error("Error cargando carteras:", error);
    showAlert("No se pudieron cargar las carteras.", "danger");
  }
}

// ===============================
// Eventos
// ===============================
createPortfolioBtn.addEventListener('click', () => openModal());

// ===============================
// Inicializar
// ===============================
cargarUsuarios();
cargarCarteras();