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
        { title: "Ativação", key: "activation_ssl" },
        { title: "Validade", key: "expiration_ssl" },
        { title: "Produto", key: "product_name" },
        { title: "Emissor", key: "issuer" },
        { title: "Status", key: "status_ssl" },
        { title: "", key: "actions" },
      ],
      product_name_options: [
        {
          "value": "ixc_provedor",
          "text": "IXC Provedor"
        },
        {
          "value": "central_assinante",
          "text": "Central do Assinante"
        },
        {
          "value": "site",
          "text": "Site"
        },
        {
          "value": "ixc_franquia",
          "text": "IXC Franquia"
        },
        {
          "value": "speedtest",
          "text": "Speed Test"
        },
        {
          "value": "opa_suite",
          "text": "Opa! Suite"
        },
        {
          "value": "acs",
          "text": "IXC Acs"
        }
      ]
    }; 
  },
  created() {
    this.getCertificates(); 
  },
  methods: {
    async getCertificates() {
      try {
        this.certificates = [];
        let certificates = (await axios.get(`${import.meta.env.VITE_API_URL}/certificates/`)).data;
        certificates.forEach(element => {
            let activation_ssl = this.formatDate(element.activation_ssl);
            let expiration_ssl = this.formatDate(element.expiration_ssl);
            element.activation_ssl = activation_ssl ? activation_ssl : '-';
            element.expiration_ssl = expiration_ssl ? expiration_ssl : '-';
            element.issuer = element.issuer && element.issuer != null ? element.issuer : '-';
            console.log(element.product_name)
            element.product_name = this.product_name_options.find( option => 
              option.value === element.product_name
            ).text;

            switch(element.status_ssl) {
              case 'Active':
                element.status_ssl = 'Ativo';
              break;
              case 'Expired':
                element.status_ssl = 'Expirado';
              break;
              case 'Abandoned': 
                element.status_ssl = 'Abandonado'
              break;
              case 'Last day':
                element.status_ssl = 'Ultimo dia';
              break;
              case 'Available':
                element.status_ssl = 'Disponível'
              break;
              case 'Inconsistent':
                element.status_ssl = 'Inconsistente';
              break;
              case 'Inactive':
              default:
                element.status_ssl = 'Inativo';
              break;
            }

            this.certificates.push(element)
        });
      } catch (error) {
        toast(`Ocorreu um erro ao carregar a pagina, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme:  'dark'
        });
      }
    },

    formatDate(date) {
      if(!date) return  '';
      date = new Date(date); 
      if(isNaN(new Date(date).getTime())) return '';
      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      let dateFormtat = `${day < 10 ? '0' : ''}${day}/${month < 10 ? '0' : ''}${month}/${year}`;
      return dateFormtat;
    },

    async destroy(certificate) {
      try {
        if (confirm(`Deseja deletar ${certificate.domain}?`)) {
          await axios.delete(`${import.meta.env.VITE_API_URL}/certificates/${certificate.id}/`);
          toast(`Registro deletado com sucesso`, {
            autoClose: 1000,
            position: 'bottom-right',
            theme:  'dark'
          });
          return this.getCertificates();
        }
      } catch (error) {
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