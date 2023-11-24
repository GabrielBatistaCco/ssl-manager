<template>
  <div class="default-layout">
    <slot name="header">
      <header class="pb-16 mb-16">
        <template>
          <v-card max-width="448" class="mx-auto">
            <v-layout>
              <v-app-bar color="#00aeef">
                <template v-slot:prepend>
                  <v-app-bar-nav-icon></v-app-bar-nav-icon>
                </template>
                <template v-slot:default>
                  <LogoIxc class="w-100"></LogoIxc>
                </template>
              </v-app-bar>
            </v-layout>
          </v-card>
        </template>
      </header>
      <div>
    </div>
    </slot>
    <slot />
  </div>
</template>
<script>
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
export default {

  created() {
   
  },
  methods: {
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
</style>