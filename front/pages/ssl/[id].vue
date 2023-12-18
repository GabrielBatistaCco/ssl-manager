<template>
  <v-container>
    <v-row no-gutters class="py-10 justify-center">
      <v-col cols="6">
        <h1 v-if="!certificate.id" class="text-center pb-5">Cadastro de certificados</h1>
        <h1 v-if="certificate.id" class="text-center pb-5">Edição de certificados</h1>
      </v-col>
      <v-col cols="8">
        <v-form v-model="valid">
          <v-row no-gutters>
            <v-col v-if="certificate.id" cols="12">
              <v-text-field v-model="certificate.id" v-value="certificate.id" disabled=""  label="ID" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="certificate.domain" v-value="certificate.domain" 
                label="Domínio *" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="certificate.ssls_url" v-value="certificate.ssls_url" label="Url ssls" />
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="certificate.product_name"
                :items="product_name_options"
                item-title="text"
                item-value="value"
                label="Nome do produto *"
                return-object
                single-line
                theme="dark"
              ></v-select>
            </v-col>
            <v-col data="certificate.activation_ssl" cols="12">
              <v-text-field v-model="certificate.activation_ssl" v-value="certificate.activation_ssl" disabled="" label="Data da ativação"/>
            </v-col>
            <v-col data="certificate.expiration_ssl" cols="12">
              <v-text-field v-model="certificate.expiration_ssl" v-value="certificate.expiration_ssl" disabled="" label="Data expiração"/>
            </v-col>
            <v-col data="certificate.issuer" cols="12">
              <v-text-field v-model="certificate.issuer" v-value="certificate.issuer" disabled="" label="Emissora"/>
            </v-col>
            <v-col data="certificate.status_ssl" cols="12">
              <v-text-field v-model="certificate.status_ssl" v-value="certificate.status_ssl" disabled="" label="Status"/>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn class="mr-2" color="error" outlined to="/ssl">
                Cancelar
              </v-btn>
              <v-btn color="success" outlined @click="persistir">
                Salvar
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  layout: 'default',
  name: 'editCertificates',
  data() {
    return {
      certificate: {
        id: null,
        domain: null,
        ssls_url: null,
        activation_ssl: null,
        expiration_ssl: null,
        activation_weekday: null,
        expiration_weekday: null,
        issuer: null,
        status_ssl: null,
        product_name: null
      },
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
          "text": "IXC ACS"
        }
      ]
    }
  },

  mounted() {
    if (this.$route?.params?.id && this.$route.params.id !== 'false' ) {
      this.getCertificate(this.$route.params.id);
    }
  },

  methods: {
    async persistir() {
      try {

        let certificate = {
          domain: this.certificate.domain,
          ssls_url: this.certificate.ssls_url,
          product_name: this.certificate.product_name.value,
        };

        if (!this.certificate.id) {
          let response = await axios.post(`${import.meta.env.VITE_API_URL}/certificates/`, certificate);
          response = response.data

          if(response?.detail?.length ) {
            toast(`Ocorreu um erro ao criar o certificado, verifique os dados e tente novamente`, {
              autoClose: 1000,
              position: 'bottom-right',
              theme: 'dark'
            });
            console.log(response.detail)
          } else {
            toast(`Registro criado com sucesso`, {
              autoClose: 1000,
              position: 'bottom-right',
              theme: 'dark'
            });
            this.$router.push('/ssl')
          }

        } else {
          certificate.id = this.certificate.id
          let response = await axios.put(`${import.meta.env.VITE_API_URL}/certificates/${certificate.id}/`, certificate);
          console.log(response)
          toast(`Registro atualizado com sucesso`, {
            autoClose: 1000,
            position: 'bottom-right',
            theme: 'dark'
          });

          // return this.$router.push('/ssl');
        }
      } catch (error) {
        toast(`Ocorreu um erro no cadastro, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme: 'dark'
        })
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
     
    async getCertificate(id) {
      try {
        let certificate = (await axios.get(`${import.meta.env.VITE_API_URL}/certificates/${id}/`)).data;
        certificate.activation_ssl = this.formatDate(certificate.activation_ssl)
        certificate.expiration_ssl = this.formatDate(certificate.expiration_ssl)
        
        certificate.product_name = this.product_name_options.find(
          option => option.value === certificate.product_name
        );

        switch(certificate.status_ssl) {
          case 'Active':
            certificate.status_ssl = 'Ativo';
          break;
          case 'Expired':
            certificate.status_ssl = 'Expirado';
          break;
          case 'Abandoned': 
            certificate.status_ssl = 'Abandonado'
          break;
          case 'Last day':
            certificate.status_ssl = 'Ultimo dia';
          break;
          case 'Available':
            certificate.status_ssl = 'Disponível'
          break;
          case 'Inconsistent':
            certificate.status_ssl = 'Inconsistente';
          break;
          case 'Inactive':
          default:
            certificate.status_ssl = 'Inativo';
          break;
        }

        this.certificate = certificate
      } catch (error) {
        toast(`Ocorreu um erro ao editar o registro, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme: 'dark'
        });
      }
    },
  },

}
</script>