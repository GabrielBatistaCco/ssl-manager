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
              <v-text-field v-model="certificate.id" v-value="certificate.id" disabled="" placeholder="ID" label="ID" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="certificate.domain" v-value="certificate.domain" placeholder="Domínio"
                label="Domínio" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="certificate.ssls_url" v-value="certificate.ssls_url" placeholder="Url ssls"
                label="Url ssls" />
            </v-col>
            <v-col v-if="certificate.activation_ssl" cols="12">
              <v-text-field v-model="certificate.activation_ssl" v-value="certificate.activation_ssl" disabled="" placeholder="Data da ativação"
                label="Data da ativação"/>
            </v-col>
            <v-col v-if="certificate.expiration_ssl" cols="12">
              <v-text-field v-model="certificate.expiration_ssl" v-value="certificate.expiration_ssl" disabled="" placeholder="Data expiração"
                label="Data expiração"/>
            </v-col>
            <v-col v-if="certificate.issuer" cols="12">
              <v-text-field v-model="certificate.issuer" v-value="certificate.issuer" disabled="" placeholder="Emissora"
                label="Emissora"/>
            </v-col>
            <v-col v-if="certificate.status_ssl" cols="12">
              <v-text-field v-model="certificate.status_ssl" v-value="certificate.status_ssl" disabled="" placeholder="Status"
                label="Status"/>
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
        status_ssl: null
      }
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
        };

        if (!this.certificate.id) {
          let response = await axios.post('http://localhost:8000/certificates/', certificate);
          
          response = response.data.domain
          toast(`Registro criado com sucesso`, {
            autoClose: 1000,
            position: 'bottom-right',
            theme: 'dark'
          });

          this.$router.push('/ssl')

        } else {
          certificate.id = this.certificate.id
          await axios.put(`http://localhost:8000/certificates/${certificate.id}/`, certificate);

          toast(`Registro atualizado com sucesso`, {
            autoClose: 1000,
            position: 'bottom-right',
            theme: 'dark'
          });

          return this.$router.push('/ssl');
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
      date = new Date(date); 
      if(isNaN(new Date(date).getTime())) {
          return '';
      }
      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      let dateFormtat = `${day < 10 ? '0' : ''}${day}/${month < 10 ? '0' : ''}${month}/${year}`;

      return dateFormtat;
    },
     
    async getCertificate(id) {
      console.log(id)
      try {
        let certificate = await axios.get(`http://localhost:8000/certificates/${id}/`);
        // tratando a data
        certificate.data.activation_ssl = this.formatDate(certificate.data.activation_ssl)
        certificate.data.expiration_ssl = this.formatDate(certificate.data.expiration_ssl)

        certificate.data.expiration_ssl = this.formatDate(certificate.data.expiration_ssl)
        
        this.certificate = certificate.data
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