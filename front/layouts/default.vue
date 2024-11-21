<template>
  <title>SSL Manager</title>
  <div class="default-layout">
    <slot name="header">
      <header class="pb-16 mb-5">
        <template>
          <v-card max-width="448" class="mx-auto max-index">
            <v-layout>
              <v-app-bar color="#00aeef">
                <template v-slot:prepend>
                  <v-app-bar-nav-icon></v-app-bar-nav-icon>
                </template>
                <template v-slot:default>
                  <router-link to="/" class="mr-auto d-flex justify-center align-center">
                    <LogoIxc class="w-100"></LogoIxc>
                  </router-link>
                </template>
              </v-app-bar>
            </v-layout>
          </v-card>
        </template>
      </header>
      <div>
    </div>
    </slot>
    <slot v-if="loadedLayout"/>
  </div>
</template>
<script>
export default {
  data() {
    return{
      loadedLayout: false
    }
  },
  beforeMount() {
    document.title = 'SSL Manager'; 
  },
  mounted() {
    this.loadedLayout = true
  }
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
