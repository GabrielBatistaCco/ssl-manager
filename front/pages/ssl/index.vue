<template>
  <v-container>
    <v-row class="justify-between">
      <v-col cols="12">
        <h1>Certificados SSL</h1>
      </v-col>
      <v-col cols="2">
        <v-select v-model="search.key" item-title="title" label="Nome do produto *" item-value="key" return-object single-line theme="dark"
          :items="getItemsHeader">
        </v-select>
      </v-col>
      <v-col cols="4">
        <v-text-field v-model="search.value" label="Buscar" />
      </v-col>
      <v-col class="text-end" cols="6">
        <v-icon color="blue" title="Adicionar novo domínio" @click="persist()"
          class="mdi-plus mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
        >
        </v-icon>
        <v-icon color="blue" title="Importar arquivo csv" @click="uploadCsv()"
          class="mdi-upload mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
        >
        </v-icon>
        <v-icon color="blue"
          title="Atualizar certificados"
          class="mdi-reload mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
          @click="updateCertificates()">
        </v-icon>
      </v-col>
    </v-row>
    <v-data-table :headers="headers" :items="certificates_show" :search="search.value" items-per-page-text="Itens por página"
      show-current-page="true"
      theme="dark"
      id="table-centered"
      @update:options="filterItems">
      <template v-slot:item.actions="{ item  }">
        <div class="text-end">
          <v-icon small color="yellow" title="Editar" class="mr-2 mdi mdi-pencil" @click="persist(item)"></v-icon>
          <v-icon small color="red" title="Deletar" class="mr-2 mdi mdi-delete" @click="destroy(item)"></v-icon>
          <a v-if="item.product_id" :href="'https://www.ssls.com/user/bundles/view/' + item.product_id" target="_blank" rel="noopener noreferrer">
            <v-icon small color="blue" title="Acessar certificado" class="mr-2 mdi mdi-open-in-new"></v-icon>
          </a>
          <v-menu location="right">
            <template v-slot:activator="{ props }">
              <v-icon class="mdi-shield-search mdi text-yellow mr-2" title="Salvar" v-bind="props"></v-icon>
            </template>
            <v-list >
              <v-list-item @click="showLogs('record', item.id)">
                <v-list-item-title>Auditoria do registro</v-list-item-title>
              </v-list-item>
              <v-list-item @click="showLogs('detail', item.id)">
                <v-list-item-title>Auditoria detalhada</v-list-item-title>
              </v-list-item>
            </v-list>    
          </v-menu>
        </div>
      </template>
      <template v-slot:item.status_ssl="{ item }">
        <span v-html="renderStatus(item)"></span>
      </template>
    </v-data-table>
  </v-container>
  <modal :modais="modais"></modal>
</template>

<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import modal from '~/components/modal.vue';

export default {
  layout: "default",
  name: "defaultCertificatesPage",
  components: {
    modal
  },
  data() {
    return {
      certificates_show: [],
      certificates: [],
      modais: [],
      search: {
        value: "",
        key: { title: "Selecione", key: "" }
      },
      headers: [
        { title: "ID", key: "id" },
        { title: "ID SSLS", key: "product_id" },
        { title: "Domínio", key: "domain" },
        // { title: "Ativação", key: "activation_ssl" },
        { title: "Validade", key: "expiration_ssl" },
        { title: "Emissor", key: "issuer" },
        { title: "Produto", key: "product_name" },
        { title: "Status", key: "status_ssl" },
        { title: " ", key: "actions" },
      ],
      product_name_options: { },
      status_ssl_options: { }
    };
  },

  computed: {
    getItemsHeader () {
      return this.headers.filter( e => e.key !== 'id' && e.key !== 'actions' )
    }
  },
  mounted() {
    let status_ssl_options = localStorage.getItem('status_ssl_options')
    status_ssl_options = JSON.parse(status_ssl_options)
    this.status_ssl_options = status_ssl_options;
    
    let product_name_options = localStorage.getItem('product_name_options')
    product_name_options = JSON.parse(product_name_options)
    this.product_name_options = product_name_options;

    this.getCertificates();
  },
  methods: {
    async getCertificates() {
      try {
        // variavel para guardar os certificados que foram "tratados"
        let certificates_updated = [];
        let certificates = (await axios.get(`${ import.meta.env.VITE_API_URL }/certificates/`)).data;
        // passa por todos
        certificates.forEach( element => {
          // trata a data para um formato mais amigavel ao usuário
          let activation_ssl = this.formatDate(element.activation_ssl);
          let expiration_ssl = this.formatDate(element.expiration_ssl);
          // adiciona o - em dados vazios
          element.activation_ssl = activation_ssl ? activation_ssl : '-';
          element.expiration_ssl = expiration_ssl ? expiration_ssl : '-';
          element.issuer = element.issuer && element.issuer != null ? element.issuer : '-';

          element.product_name =
            this.product_name_options[element.product_name]
              ? this.product_name_options[element.product_name].text
                : "-";

          // pra separar da busca foram criados dois status no front
          if(this.status_ssl_options[element.status_ssl]) {
            element.status = this.status_ssl_options[element.status_ssl];
          } else {
            // desconhecido
            element.status = this.status_ssl_options["unknown"];
          }
          
          element.status_ssl = element.status.text;

          certificates_updated.push(element);
        } );

        // atualiza as globais 
        this.certificates_show = certificates_updated;
        this.certificates = certificates_updated;
      } catch (error) {
        console.log(error)
        toast.error(`Ocorreu um erro ao carregar a pagina, contate o administrador`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } );
      }
    },
    renderStatus(item) {
      // função responsável por renderizar o status do certificado na data table, ela é necessária para a bolinha colorida
      const status = item.status
      if( status.text ) {
        return `
          <div>
            <span style="
              background-color: ${ status?.color || "#DD2C00" };
              width: 10px;
              height: 10px;
              margin-right: 5px;
              display: inline-block;
              border-radius: 100%;
              ">
            </span>
            ${ status.text }
          <div>
        `;
      } else {
        return `<div class="text-center">
            -
          </div>`
      }
    },
    async filterItems () {
      // função extra para busca por campos individuais, ex.: somente status
      let key = this.search.key.key
      let value = this.search.value
      let certificates_show = [];

      // se não tem filtro por um dos campos key = campos do certificado ex.: dominio
      if( !key ) return false;

      const normalize = (str) => {
          return str
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '');
        };

      value = normalize(value.toLowerCase());

      this.certificates.forEach((e) => {
        // busca
        if (normalize(String(e[key]).toLowerCase()).includes(value)) {
          certificates_show.push(e);
        }
      } );
      // atualiza
      this.certificates_show = certificates_show
    },

    formatDate(date, time = false) {
      // formata a data para o formato br, com opção de time
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
    async destroy(certificate) {
      try {
        if (confirm(`Deseja deletar ${ certificate.domain }?`)) {
          await axios.delete(`${ import.meta.env.VITE_API_URL }/certificates/${ certificate.id }/`);
          toast.success(`Registro deletado com sucesso`, {
            autoClose: 4000,
            position: 'bottom-right',
            theme: 'dark'
          } );
          return this.getCertificates();
        }
      } catch (error) {
        toast.error(`Ocorreu um erro ao deletar o registro id ${ certificate.id }, contate o administrador`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } );
      }
    },
    async persist(certificate) {
      try {
        if (certificate) {
          return this.$router.push( {
            name: "ssl-id",
            params: { id: certificate.id },
          } );
        }

        return this.$router.push( {
          name: "ssl-id",
          params: { id: false },
        } );

      } catch (error) {
        console.log(error)
        toast.error(`Ocorreu um erro, contate o administrador`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } );
      }
    },
    uploadCsv() {
      let input = document.createElement('input');
      input.classList.add('d-none');
      input.type = 'file';
      input.accept = '.csv';
      input.addEventListener('change', async (e) => {
        document.body.removeChild(input);

        let selectedFile = e.target.files[0];

        if (!selectedFile) {
          toast.warning('Nenhum arquivo selecionado.');
          return;
        }

        let formData = new FormData();
        formData.append('file', selectedFile);

        try {
          toast.success(`Arquivo carregado com sucesso, logo os certificados serão atualizados`, {
              autoClose: 4000,
              position: 'bottom-right',
              theme: 'dark'
          } );

          await axios.post(`${ import.meta.env.VITE_API_URL }/import_csv/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          } )
          .then(response => {
            switch(response.data.detail) {
              case 'success': 
                toast.success(`Arquivo .csv importado com sucesso`, {
                  autoClose: 4000,
                  position: 'bottom-right',
                  theme: 'dark'
                } );
              break;
              case 'already_running':
                toast.warning(`Já tem um arquivo sendo processado, aguarde e tente novamente.`, {
                  autoClose: 4000,
                  position: 'bottom-right',
                  theme: 'dark'
                } );
              break;
              case 'empty': 
                toast.warning(`Arquivo .csv esta vazio, verifique ou tente novamente.`, {
                  autoClose: 4000,
                  position: 'bottom-right',
                  theme: 'dark'
                } );
              break;
              case 'invalid':
                toast.warning(`Arquivo inválido, tente carregar um arquivo .csv válido`, {
                  autoClose: 4000,
                  position: 'bottom-right',
                  theme: 'dark'
                } );
              break;
              case 'failed_refresh':
              toast.error(`Falha ao verificar status dos certificados durante a importação.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
              default:
                toast.error(`Ocorreu um erro ao realizar a importação.`, {
                  autoClose: 4000,
                  position: 'bottom-right',
                  theme: 'dark'
                } );
              break;
            }
            this.getCertificates();
          } )

        } catch (error) {
          console.error(error);
          toast.error(`Ocorreu um erro ao importar os certificados, contate o administrador.`, {
            autoClose: 4000,
            position: 'bottom-right',
            theme: 'dark'
          } );
        }
      } );

      document.body.appendChild(input);
      input.click();
    },
    async updateCertificates() {
      try {
        toast.success(`Iniciando atualização...`, {
            autoClose: 4000,
            position: 'bottom-right',
            theme: 'dark'
        } );

        await axios.get(`${ import.meta.env.VITE_API_URL }/refresh_certificates/`)
        .then(response => {
          switch(response.data.detail) {
            case 'success': 
              toast.success(`Certificados atualizados com sucesso.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'locked':
              toast.warning(`Já tem uma atualização em execução, aguarde e tente novamente.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            case 'no_certificates':
              toast.warning(`Não existem certificados para serem atualizados.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
            default:
              toast.error(`Ocorreu um erro ao realizar a atualização.`, {
                autoClose: 4000,
                position: 'bottom-right',
                theme: 'dark'
              } );
            break;
          }
          this.getCertificates();
        } )

      } catch (error) {
        console.error(error);
        toast.error(`Ocorreu um erro ao atualizar os certificados`, {
          autoClose: 4000,
          position: 'bottom-right',
          theme: 'dark'
        } );
      }
    },
    async showLogs(option, id) {
      try {
        
        let audit = { };
        let auditLogsHeaders = [];
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
};
</script>


<style >
table thead th div {
  width: fit-content;
  margin: 0 auto;
  position: relative;
}

table thead th div i.v-icon {
  position: absolute !important;
  right: -21px;
}

#table-centered table tbody tr td {
  text-align: center;
}

#table-centered table tbody tr td:nth-child(8),
#table-centered table tbody tr td:nth-child(3) {
  text-align: left;
}

.table-modal table tbody tr td:not(:nth-child(4)) {
  text-align: center;
}

.table-modal table.table-dados tbody tr td {
  text-align: left;
}
</style>
