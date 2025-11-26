document.addEventListener("DOMContentLoaded", () => {
    const buscarInput = document.getElementById("buscarInput");
    const estadoFiltro = document.getElementById("estadoFiltro");
    const fechaFiltro = document.getElementById("fechaFiltro");
    const filas = document.querySelectorAll("table tbody tr");

    function aplicarFiltros() {
        const txtBuscar = buscarInput.value.toLowerCase();
        const estado = estadoFiltro.value;
        const fecha = fechaFiltro.value;

        filas.forEach(fila => {
            const titulo = fila.children[2]?.innerText.toLowerCase() || "";
            const estadoFila = fila.children[3]?.innerText.trim();
            const fechaFila = fila.children[4]?.innerText.split(" ")[0]; // dd/mm/yyyy

            // convertir fecha a yyyy-mm-dd
            const partes = fechaFila.split("/");
            const fechaConvertida = `${partes[2]}-${partes[1]}-${partes[0]}`;

            let mostrar = true;

            if (txtBuscar && !titulo.includes(txtBuscar)) mostrar = false;
            if (estado && estadoFila !== estado) mostrar = false;
            if (fecha && fecha !== fechaConvertida) mostrar = false;

            fila.style.display = mostrar ? "" : "none";
        });
    }

    buscarInput.addEventListener("input", aplicarFiltros);
    estadoFiltro.addEventListener("change", aplicarFiltros);
    fechaFiltro.addEventListener("change", aplicarFiltros);
});
