<template>
    <title>SSL Manager</title>
    <div class="default-layout">
      <slot name="header">
        <header class="pb-16 mb-5">
          <!-- Removido o bloco da barra de navegação -->
        </header>
        <div>
      </div>
      </slot>
      <slot />
    </div>
  </template>
  
  <script>
  export default {
    beforeMount() {
      document.title = 'SSL Manager'; 
    },
  }
  </script>
  
  <style>
  .v-icon {
    position: static !important;
  }
  
  th:hover .v-icon{
    opacity: 1 !important;
  }
  
  .max-index{
    z-index: 100 !important;
  }
  
  /* scrollbar */
  ::-webkit-scrollbar {
      width: 4px; 
  }
  
  ::-webkit-scrollbar-thumb {
      background-color: #90a4ae;
      border-radius: 25px; 
  }
  
  ::-webkit-scrollbar-track {
      background-color: #cfd8dc;
  }
  
  * {
      scrollbar-color: #90a4ae #cfd8dc; 
      scrollbar-width: thin; 
  }
  
  h1 {
    font-size: clamp(25px,4vw,35px);
  }
  </style>
  
