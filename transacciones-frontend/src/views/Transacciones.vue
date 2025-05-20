<template>
    <div class="container">
        <h2>Transacciones</h2>
        <div class="transacciones-list">
            <div v-for="transaccion in transacciones" :key="transaccion.id" class="transaccion-card">
                <h3>{{ transaccion.tipo }}</h3>
                <p><strong>Monto:</strong> ${{ transaccion.monto }}</p>
                <p><strong>Descripción:</strong> {{ transaccion.descripcion || 'Sin descripción' }}</p>
                <p><strong>Referencia:</strong> {{ transaccion.referencia || 'Sin referencia' }}</p>
                <p><strong>Fecha:</strong> {{ new Date(transaccion.fecha).toLocaleString() }}</p>
            </div>
        </div>
        <router-link to="/" class="volver-link">Volver al Inicio</router-link>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "TransaccionesView",
    data() {
        return {
            transacciones: []
        };
    },
    mounted() {
        this.obtenerTransacciones();
    },
    methods: {
        async obtenerTransacciones() {
            try {
                const response = await axios.get("http://localhost:8000/transacciones/");
                this.transacciones = response.data;
            } catch (error) {
                console.error("Error al obtener las transacciones:", error);
            }
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

h2 {
    color: #2ecc71;
    text-align: center;
    margin-bottom: 20px;
    font-size: 2.5em;
}

.transacciones-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}

.transaccion-card {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 20px;
    width: 300px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.transaccion-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.transaccion-card h3 {
    color: #3498db;
    margin-bottom: 10px;
    font-size: 1.8em;
}

.transaccion-card p {
    color: #555;
    margin-bottom: 8px;
    font-size: 1.1em;
}

.volver-link {
    display: block;
    margin: 20px auto;
    text-align: center;
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.2em;
    transition: color 0.3s;
}

.volver-link:hover {
    color: #2ecc71;
}
</style>