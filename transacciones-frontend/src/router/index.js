import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import TransaccionesView from '../views/Transacciones.vue';

const routes = [
    { path: '/', component: HomeView },
    { path: '/transacciones', component: TransaccionesView }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;