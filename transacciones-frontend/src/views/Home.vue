<template>
    <div class="home-container">
        <div class="welcome-card">
            <h1>Transacciones</h1>
            <router-link to="/transacciones" class="btn-acceso">
                Ver Transacciones
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: "HomeView"
};
</script>

<style scoped>
.home-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #ffffff, #f1f4f9);
    padding: 20px;
}

.welcome-card {
    background-color: #ffffff;
    padding: 50px 40px;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    text-align: center;
    max-width: 600px;
    width: 100%;
    transition: transform 0.3s;
}

.welcome-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
}

h1 {
    font-size: 2.8em;
    color: #2c3e50;
    margin-bottom: 15px;
    font-weight: bold;
}


.btn-acceso {
    background-color: #2ecc71;
    color: #ffffff;
    padding: 15px 40px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 1.2em;
    font-weight: bold;
    transition: background-color 0.3s, transform 0.2s;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.btn-acceso:hover {
    background-color: #27ae60;
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}
</style>