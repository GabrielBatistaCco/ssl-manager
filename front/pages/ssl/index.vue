<template>
  <v-container>
      <v-row>
        <v-col cols="12">
          <h1 style="color: #1aa5f">Certificados SSL</h1>
        </v-col>
        <v-col cols="6">
          <v-text-field v-model="search" label="Buscar"/>
        </v-col>
        <v-col cols="2">
          <v-icon color="blue" class="mdi-plus mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated " @click="persist()">
            mdi-plus
          </v-icon>
        </v-col>
      </v-row>
      <v-data-table
        :headers="headers"
        :items="certificates" 
        :search="search"
        items-per-page-text="Itens por página"
        show-current-page="true"
        theme="dark"
        >
        <template v-slot:item.actions="{ item }">
          <v-icon small color="yellow" class="mr-2" @click="persist(item)">
            mdi-pencil
          </v-icon> 
          <v-icon small color="red" class="mr-2" @click="destroy(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
  </v-container>
  
</template>
 
<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
export default {
  layout: "default",
  name: "defaultCertificatesPage",
  data() {
    return {
      search: "",
      certificates: [],
      headers: [
        { title: "ID", key: "id" },
        { title: "Domínio", key: "domain" },
        { title: "Url ssls", key: "ssls_url" },
        { title: "", key: "actions" },
      ],
    }; 
  },
  created() {
    this.getCertificates(); 
  },
  methods: {
    async getCertificates() {
      try {
        this.certificates = (await axios.get(`${import.meta.env.VITE_API_URL}/certificates/`)).data;
      } catch (error) {
        toast(`Ocorreu um erro ao carregar a pagina, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme:  'dark'
        });
      }
    },
    
    async destroy(certificate) {
      try {
        if (confirm(`Deseja deletar ${certificate.domain}?`)) {
          await axios.delete(`${import.meta.env.VITE_API_URL}/certificates/${certificate.id}`);
          toast(`Registro deletado com sucesso`, {
            autoClose: 1000,
            position: 'bottom-right',
            theme:  'dark'
          });
          return this.getCertificates();
        }
      } catch (error) {
        console.log(error)
        toast(`Ocorreu um erro ao deletar o registro id ${certificate.id}, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme:  'dark'
        });
      }
    },
    async persist(certificate) {
      try {
        if (certificate) {
          return this.$router.push({
            name: "ssl-id", 
            params: { id: certificate.id },
          });
        }
        
        return this.$router.push({
          name: "ssl-id",
          params: { id: false }, 
        });

      } catch (error) {
        toast(`Ocorreu um erro, contate o administrador`, { 
          autoClose: 1000,
          position: 'bottom-right',
          theme:  'dark'
        });
      }
    },
  },
};
</script>