<template>
  <div id="app">
    <nav>
      <router-link to="/">Pagos</router-link> |
      <router-link to="/create">Nuevo Pago</router-link> |
      <router-link to="/providers">Proveedores</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 20px;
}

nav {
  padding: 10px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>