document.addEventListener('DOMContentLoaded', () => {
    const agregarUsuario = document.getElementById('agregar-usuario');
    const btnGuardar = document.getElementById('btn-guardar');
    const usuariosContainer = document.getElementById('usuarios-container');

    // Cargar usuarios al iniciar
    cargarUsuarios();

    // Mostrar/ocultar formulario al hacer hover
    agregarUsuario.addEventListener('mouseenter', () => {
        agregarUsuario.querySelector('.formulario-flotante').style.display = 'block';
    });

    agregarUsuario.addEventListener('mouseleave', () => {
        agregarUsuario.querySelector('.formulario-flotante').style.display = 'none';
    });

    // Guardar nuevo usuario
    btnGuardar.addEventListener('click', async () => {
        const nombre = document.getElementById('nombre').value.trim();
        const correo = document.getElementById('correo').value.trim();

        if (!nombre || !correo) {
            alert('Por favor completa todos los campos');
            return;
        }

        try {
            const response = await fetch('/api/usuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nombre, correo }),
            });

            if (!response.ok) throw new Error('Error al guardar');

            // Limpiar formulario y recargar usuarios
            document.getElementById('nombre').value = '';
            document.getElementById('correo').value = '';
            cargarUsuarios();
        } catch (error) {
            alert(error.message);
        }
    });

    // Función para cargar usuarios
    async function cargarUsuarios() {
        try {
            const response = await fetch('/api/usuarios');
            const usuarios = await response.json();
            mostrarUsuarios(usuarios);
        } catch (error) {
            console.error('Error al cargar usuarios:', error);
        }
    }

    // Función para mostrar usuarios en los placeholders
    function mostrarUsuarios(usuarios) {
        usuariosContainer.innerHTML = '';
        usuarios.forEach(usuario => {
            const divUsuario = document.createElement('div');
            divUsuario.className = 'dato';
            divUsuario.innerHTML = `
                <p>${usuario.nombre}</p>
                <p>${usuario.correo}</p>
            `;
            usuariosContainer.appendChild(divUsuario);
        });
    }
});
