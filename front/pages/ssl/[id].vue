<template>
  <v-container>
    <v-row no-gutters class="pb-10 justify-center">
      <v-col cols="12" lg="10" xl="8">
        <v-row class="justify-space-between">
          <v-col cols="12" lg="8">
            <h1 v-if="!certificate.id" class="pb-lg-5 px-3">Cadastro de certificados</h1>
            <h1 v-if="certificate.id" class="pb-lg-5 px-3">Editando certificado {{ certificate.id }}</h1>
          </v-col>
          <v-col cols="12" lg="auto" class="pb-7 text-right pb-lg-0">
            <v-menu v-if="certificate.id" location="bottom" theme="dark">
              <template v-slot:activator="{ props }">
                <v-icon
                  class="mdi-shield-search mdi text-yellow v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
                  title="Auditoria"
                  v-bind="props"
                ></v-icon>
              </template>
              <v-list >
                <v-list-item @click="showLogs('record')">
                  <v-list-item-title>Auditoria do registro</v-list-item-title>
                </v-list-item>
                <v-list-item @click="showLogs('detail')">
                  <v-list-item-title>Auditoria detalhada</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-icon class="mdi-close mdi text-error v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2" title="Cancelar" @click="goBack"></v-icon>
            <v-icon v-if="permitEdit" title="Salvar" id="save-edit" @click="persistir"
              class="mdi-check mdi text-green v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2 mr-3">
            </v-icon>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12" lg="10" xl="8">
        <v-form v-model="valid">
          <v-row no-gutters>
            <v-col class="px-3" cols="12" lg="6">
              <v-text-field v-model="certificate.domain" v-value="certificate.domain" :disabled="!permitEdit" label="Domínio" />
              <v-text-field v-model="certificate.ssls_url" v-value="certificate.ssls_url" :disabled="!permitEdit" label="Url ssls" />
              <v-text-field v-model="certificate.email" v-value="certificate.email" :disabled="!permitEdit" label="E-mail notificação" />
              <v-select v-model="certificate.product_name"  :disabled="!permitEdit" item-title="text"  item-value="value" label="Nome do produto *"
                :items="Object.keys(product_name_options).map(chave => product_name_options[chave])" 
                return-object
                single-line
                theme="dark">
              </v-select>
            </v-col>
            <v-col class="px-3" cols="12" lg="6">
              <v-text-field v-model="certificate.activation_ssl" v-value="certificate.activation_ssl" disabled="" label="Data da ativação"/>
              <v-text-field v-model="certificate.expiration_ssl" v-value="certificate.expiration_ssl" disabled="" label="Data expiração"/>
              <v-text-field v-model="certificate.issuer" v-value="certificate.issuer" disabled="" label="Emissora"/>
              <v-text-field v-model="certificate.status_ssl" v-value="certificate.status_ssl" disabled="" label="Status"/>
            </v-col>
            <v-col class="px-3 h-100" cols="12" lg="12">
              <v-textarea v-model="certificate.notes" class="resize-vertical" :disabled="!permitEdit" placeholder="Digite aqui"></v-textarea>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
  <modal :modais="modais"></modal>
</template>

<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import modal from '~/components/modal.vue';
export default {
  layout: 'default',
  name: 'editCertificates',
  components: {
    modal   
  },
  data() {
    return {
      modais:[],
      permitEdit: false,
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
        product_name: null,
        notes: null,
        email: null
      },
      product_name_options: { },
      status_ssl_options: { }
    }
  },
  async beforeMount() {
    let status_ssl_options = localStorage.getItem('status_ssl_options')
    status_ssl_options = JSON.parse(status_ssl_options)
    this.status_ssl_options = status_ssl_options;
    
    let product_name_options = localStorage.getItem('product_name_options')
    product_name_options = JSON.parse(product_name_options)
    this.product_name_options = product_name_options;

    //  se vier id esta buscando a edição de um certificado
    if (this.$route?.params?.id && this.$route.params.id !== 'false' ) {
      this.getCertificate(this.$route.params.id);
    } else {
      this.permitEdit = true;
    }
  },
  beforeUnmount() {
    this.unlock()
  },
  methods: {
    async persistir() {
      document.querySelector('#save-edit').style.pointerEvents = "none"
      
      try {
        function doneResponse (detail) {
          switch(detail) {
            case 'success': 
              toast.success(`Sucesso ao salvar o registro.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
              return true;
            break;
            case 'cert_error': 
              toast.error(`Erro ao verificar dados do certificado.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'product_empty': 
              toast.warning(`O campo Nome do produto é obrigatório`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'cert_empty': 
              toast.warning(`Pelo menos um Domínio ou Url ssls deve ser preenchido`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'domain_exists': 
              toast.warning(`Esse Domínio já esta cadastrado`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'invalid_url': 
              toast.warning(`Verifique a Url ssls informada, formato inválido`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'url_exists': 
              toast.warning(`Essa Url ssls já esta cadastrada`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'invalid_email': 
              toast.warning(`Verifique se o e-mail esta correto`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            default:
              toast.error(`Ocorreu um erro ao salvar o certificado.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
          }
          return false
        }

        let certificate = {
          domain: this.certificate.domain && this.certificate.domain.length ? this.certificate.domain : null,
          ssls_url: this.certificate.ssls_url && this.certificate.ssls_url.length ? this.certificate.ssls_url : null,
          product_name: this.certificate?.product_name?.value,
          notes: this.certificate.notes,
          email: this.certificate.email && this.certificate.email.length ? this.certificate.email : null
        };

        if (!this.certificate.id) {
          let response = await axios.post(`${ import.meta.env.VITE_API_URL }/certificates/`, certificate);
          response = response.data

          if(typeof response.detail == "object") {
            response.detail = response.detail[0]
          }
          
          if(doneResponse(response.detail)) {
            let cert_id = response.data.id
            this.$router.push(`/ssl/${ cert_id }`)
          }
          document.querySelector('#save-edit').style.pointerEvents = "all"

        } else {
          certificate.id = this.certificate.id

          if( this.permitEdit ) {
            let response = await axios.put(`${ import.meta.env.VITE_API_URL }/certificates/${ certificate.id }/`, certificate);
            response = response.data
            
            if(typeof response.detail == "object") {
              response.detail = response.detail[0]
            }
            
            if(doneResponse(response.detail)) {
              this.getCertificate(response.data.id)
            }
            document.querySelector('#save-edit').style.pointerEvents = "all"

          } else {
            toast.error(`Não foi possivel salvar, já existe um usuário editando esse certificado!`, {
              autoClose: 4000,
              position: 'bottom-right',
              theme: 'dark'
            } );
          }
        }
      } catch (error) {
        console.log(error)
        toast.error(`Ocorreu um erro no cadastro, contate o administrador`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } )
        document.querySelector('#save-edit').style.pointerEvents = "all"
      }
    },

    formatDate(date, time = false) {
      if(!date) return  '';
      date = new Date(date); 
      if(isNaN(new Date(date).getTime())) return '';
      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      if(time) {
        let h = date.getHours()
        let m = date.getMinutes()
        let s = date.getSeconds()
        time = `${ h }:${ m }:${ (s+"").length >= 2  ? s : '0'+ s }`
      } else {
        time = '';
      } 
      let dateFormtat = `${ day < 10 ? '0' : '' }${ day }/${ month < 10 ? '0' : '' }${ month }/${ year } ${ time }`;
      return dateFormtat;
    },
    unlock() {
      if(this.permitEdit) {
        axios.put(`${ import.meta.env.VITE_API_URL }/certificates/${ this.permitEdit }/unlock/`);
        this.permitEdit = false
      }
    },
    goBack () {
      this.unlock()
      this.$router.push('/ssl')
    },
    
    async getCertificate(id) {
      try {
        let certificate = (await axios.get(`${ import.meta.env.VITE_API_URL }/certificates/${ id }/`)).data;
        // verifica se o certificado não esta bloqueado, ou seja, sendo editado por outro usuário
        switch(certificate.detail) {
          case 'locked':
            // se estiver ele desativa a edição do certificado e avisa o usuário
            this.permitEdit = false
            toast.warning(`Já existe um usuário editando esse certificado!`, {
              autoClose: false,
              position: 'bottom-right',
              theme: 'dark' 
            } );
            certificate = certificate.data
          break;
          default:
            // se estiver livre, libera a edição para o usuario e agenda o desbloqueio
            this.permitEdit = id

            window.addEventListener('beforeunload', (event) => {
              event.preventDefault()
              this.unlock()
            } );
            
            window.addEventListener('unload', (event) => {
              event.preventDefault()
              this.unlock()
            } );

          break
        }
        // formata a data
        certificate.activation_ssl = this.formatDate(certificate.activation_ssl)
        certificate.expiration_ssl = this.formatDate(certificate.expiration_ssl)
        
        // ajusta o status para o padrão
        certificate.product_name = 
            this.product_name_options[certificate.product_name] 
              ? this.product_name_options[certificate.product_name] 
                : undefined;

        certificate.status_ssl = 
          this.status_ssl_options[certificate.status_ssl] 
            ? this.status_ssl_options[certificate.status_ssl].text 
              : "-";

        certificate.email = certificate.email ? certificate.email : null
        this.certificate = certificate
      } catch (error) {
        console.log(error)
        toast.error(`Ocorreu um erro ao salvar o registro, contate o administrador`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } );
      }
    },

    async showLogs(option, id = this.certificate.id) {
      try {
        
        let audit = { };
        let auditLogsHeaders =  [];
        let titleModal = '';
        
        switch(option) {
          case 'record':
            titleModal = 'Auditoria de registro'
            audit = (await axios.get(`${ import.meta.env.VITE_API_URL }/audit/${ id }/record_logs/`)).data;
            auditLogsHeaders = [
              { title: "Ação", key: "action" },
              { title: "Registro", key: "record_id" },
              { title: "Data", key: "timestamp" },
              { title: "Dados", key: "table_json" },
              { title: "Usuário", key: "user" },
            ]
          break;
          case 'detail': 
            titleModal = 'Auditoria detalhada'
            audit = (await axios.get(`${ import.meta.env.VITE_API_URL }/audit/${ id }/detailed_logs/`)).data;
            auditLogsHeaders = [
              { title: "Ação", key: "action" },
              { title: "Registro", key: "record_id" },
              { title: "Data", key: "timestamp" },
              { title: "Dados", key: "table_json" },
              { title: "Usuário", key: "user"}
            ]
          break;
        }

        if( audit.audit_logs ) {
          audit = audit.audit_logs
          let auditLogsItems = []
  
          audit.forEach( e => {
            e.timestamp = this.formatDate(e.timestamp, true)
            switch(e.action.toLowerCase()) {
              case 'insert':
                e.action = 'Inseriu';
              break;
              case 'update':
                e.action = 'Editou';
              break;
              case 'delete':
                e.action = 'Excluiu';
              break;
            }
            let html = '';
            Object.keys(e.cert_data).forEach(key => {
              html += `
                <tr>
                  <td class="px-2 py-1">${ key }</td>
                  <td class="px-2 py-1"> ${ e.cert_data[key] ? e.cert_data[key] : '' }</td>
                </tr>`
            } )

            e.table_json = `<table class="table-dados">${ html }</table>`;

            auditLogsItems.push(e);
          } )
  
          this.modais.push( {
            "title": titleModal,
            "confirmButtonText": "OK",
            "size": "xl",
            "type": "info",
            "body": false,
            "tableItems": auditLogsItems,
            "tableHeaders": auditLogsHeaders
          } )
        }

      } catch (error) {
        console.log(error)
        toast.error(`Ocorreu um erro ao auditar registro, contate o administrador`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } );
      }
    }
  },
}
</script>

<style scoped>
.mdi-shield-search {
  background-color: #ffffff;
}
.resize-vertical {
  resize: vertical;
}
</style>
