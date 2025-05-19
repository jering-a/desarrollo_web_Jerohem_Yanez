document.addEventListener("DOMContentLoaded", function() {
    const actividades = [
      {
        titulo: "Concierto en Plaza Italia",
        inicio: "2025-04-10 15:00",
        termino: "2025-04-10 17:00",
        comuna: "Santiago",
        sector: "Plaza Italia",
        tema: "Música",
        organizador: "Ana Pérez",
        fotos: ["../images/musica320.jpeg", "../images/musicaaa320.jpg"] // Fotos en tamaño 320
      },
      {
        titulo: "Zumba en el parque",
        inicio: "2025-04-11 11:00",
        termino: "2025-04-11 13:00",
        comuna: "Ñuñoa",
        sector: "Parque Pucará",
        tema: "Deporte",
        organizador: "Juan Díaz",
        fotos: ["../images/futbol320.jpg"] // Agrega las fotos aquí
      },
      {
        titulo: "Charlas científicas juveniles",
        inicio: "2025-04-12 16:00",
        termino: "2025-04-12 19:00",
        comuna: "Puente Alto",
        sector: "Centro Cultural",
        tema: "Ciencias",
        organizador: "Marcela Soto",
        fotos: ["../images/ciencia320.jpg", "../images/cienciaa320.png", "../images/ciencian320.jpg"]
      },
      {
        titulo: "Feria de sabores",
        inicio: "2025-04-13 10:00",
        termino: "2025-04-13 12:00",
        comuna: "La Florida",
        sector: "Av. Vicuña Mackenna",
        tema: "Comida",
        organizador: "Pedro Gómez",
        fotos: ["../images/comida320.jpeg"]
      },
      {
        titulo: "Clases de salsa al atardecer",
        inicio: "2025-04-14 18:00",
        termino: "2025-04-14 20:00",
        comuna: "Providencia",
        sector: "Terraza Mall Costanera",
        tema: "Baile",
        organizador: "Claudia Rojas",
        fotos: ["../images/danza320.jpeg", "../images/baile320.jpeg"]
      }
    ];
  
    const tablaActividades = document.getElementById("tablaActividades");
    const detalle = document.getElementById("detalle");
    const modal = document.getElementById("modal");
    const modalImg = document.getElementById("modalImg");
    const contenedorFotos = document.getElementById("detalleFotos");
    const volverListadoBtn = document.getElementById("volverListado");
    const cerrarModalBtn = document.getElementById("cerrarModal");
  
    // Event listener para las filas de la tabla
    function agregarEventosFilas() {
      const filas = tablaActividades.querySelectorAll("tbody tr");
      filas.forEach((fila, index) => {
        fila.addEventListener("click", function() {
          mostrarDetalle(index);
        });
      });
    }
  
    // Event listener para las fotos en el detalle
    function agregarEventosFotos() {
      contenedorFotos.addEventListener("click", function(event) {
        if (event.target.tagName === "IMG") {
          ampliarImagen(event.target.src); // Al hacer clic, muestra la imagen en tamaño completo
        }
      });
    }
  
    // Event listener para volver al listado
    function agregarEventoVolverListado() {
      volverListadoBtn.addEventListener("click", volverListado);
    }
  
    // Event listener para cerrar el modal
    function agregarEventoCerrarModal() {
      cerrarModalBtn.addEventListener("click", cerrarModal);
    }
  
    // Mostrar detalle de actividad
    function mostrarDetalle(index) {
      const act = actividades[index];
  
      // Cambiar la vista a detalle
      document.getElementById("tablaActividades").classList.add("hidden");
      detalle.classList.remove("hidden");
  
      // Rellenar los detalles de la actividad
      document.getElementById("tituloActividad").textContent = act.titulo;
      document.getElementById("detalleInicio").textContent = act.inicio;
      document.getElementById("detalleTermino").textContent = act.termino;
      document.getElementById("detalleComuna").textContent = act.comuna;
      document.getElementById("detalleSector").textContent = act.sector;
      document.getElementById("detalleTema").textContent = act.tema;
      document.getElementById("detalleOrganizador").textContent = act.organizador;
  
      // Mostrar las fotos en miniatura (320x240)
      contenedorFotos.innerHTML = "";
      act.fotos.forEach(src => {
        const img = document.createElement("img");
        img.src = src; // Usamos la foto en miniatura
        img.alt = "foto actividad";
        img.style.width = "320px"; // Establecemos el tamaño en miniatura
        img.style.height = "240px";
        contenedorFotos.appendChild(img);
      });
  
      // Agregar eventos a las fotos
      agregarEventosFotos();
    }
  
    // Volver al listado de actividades
    function volverListado() {
      document.getElementById("tablaActividades").classList.remove("hidden");
      detalle.classList.add("hidden");
    }
  
    // Ampliar la imagen (se muestra en tamaño 800x600)
    function ampliarImagen(src) {
      modalImg.src = src.replace("320", "800"); // Reemplaza "320" por "800" para la imagen en tamaño grande
      modal.style.display = "flex";
    }
  
    // Cerrar el modal
    function cerrarModal() {
      modal.style.display = "none";
    }
  
    // Inicializar los event listeners
    agregarEventosFilas();
    agregarEventoVolverListado();
    agregarEventoCerrarModal();
  });

  