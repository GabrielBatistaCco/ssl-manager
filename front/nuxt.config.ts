// https://nuxt.com/docs/api/configuration/nuxt-config
const temaCustomizado = {
  dark: true,
  colors: {
    background: '#660000',
    surface: '#FFFFFF',
    primary: '#6200EE',
    secondary: '#03DAC6',
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
  },
};

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@invictus.codes/nuxt-vuetify',
    '@nuxt/devtools',
  ],
  vuetify: {
    /* vuetify options */
    vuetifyOptions: {
      theme: {
        defaultTheme: 'temaCustomizado',
        themes: {
          temaCustomizado,
        },
      },
    },

    moduleOptions: {
      /* nuxt-vuetify module options */
      treeshaking: true || false,
      useIconCDN: true || false,

      /* vite-plugin-vuetify options */
      styles: true || 'none' || 'expose' || 'sass' || { configFile: String },
      autoImport: true || false,
      useVuetifyLabs: true || false,
    },
  },
})
