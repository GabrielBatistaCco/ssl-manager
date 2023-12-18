<template>
  <v-container>
    <v-row style="justify-content: space-between;">
      <v-col cols="12">
        <h1 style="color: #1aa5f">Certificados SSL</h1>
      </v-col>
      <v-col cols="6">
        <v-text-field v-model="search" label="Buscar" />
      </v-col>
      <v-col class="text-end" cols="2">
        <v-icon color="blue"
          class="mdi-plus mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
          title="Adicionar novo domínio"
          @click="persist()">
        </v-icon>
        <v-icon color="blue"
          title="Importar arquivo csv"
          class="mdi-upload mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
          @click="uploadCsv()">
        </v-icon>
        <v-icon color="blue"
          title="Atualizar certificados"
          class="mdi-reload mdi text-blue v-btn--icon v-btn--density-default v-btn--size-large v-btn--variant-elevated ml-2"
          @click="updateCertificates()">
        </v-icon>
      </v-col>
    </v-row>
    <v-data-table :headers="headers" :items="certificates" :search="search" items-per-page-text="Itens por página"
      show-current-page="true" theme="dark">
      <template v-slot:item.actions="{ item }">
        <v-icon small color="yellow" title="Editar" class="mr-2" @click="persist(item)">
          mdi-pencil
        </v-icon>
        <v-icon small color="red" title="Deletar" class="mr-2" @click="destroy(item)">
          mdi-delete
        </v-icon>
        <v-icon v-if="item.ssls_url" small color="blue" title="Acessar certificado" class="mr-2" @click="goto(item.ssls_url)">
          mdi-open-in-new
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
          "value": "",
          "text": "-"
        },
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
    };
  },
  mounted() {
    this.getCertificates();
  },
  methods: {
    async getCertificates() {
      try {
        let certificates_updated = [];
        let certificates = (await axios.get(`${import.meta.env.VITE_API_URL}/certificates/`)).data;
        certificates.forEach(element => {
          let activation_ssl = this.formatDate(element.activation_ssl);
          let expiration_ssl = this.formatDate(element.expiration_ssl);
          element.activation_ssl = activation_ssl ? activation_ssl : '-';
          element.expiration_ssl = expiration_ssl ? expiration_ssl : '-';
          element.issuer = element.issuer && element.issuer != null ? element.issuer : '-';
          element.product_name = this.product_name_options.find(option =>
            option.value === element.product_name
          ).text;

          switch (element.status_ssl) {
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

          certificates_updated.push(element);
        });

        this.certificates = certificates_updated;
      } catch (error) {
        console.log(error)
        toast(`Ocorreu um erro ao carregar a pagina, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme: 'dark'
        });
      }
    },

    formatDate(date) {
      if (!date) return '';
      date = new Date(date);
      if (isNaN(new Date(date).getTime())) return '';
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
            theme: 'dark'
          });
          return this.getCertificates();
        }
      } catch (error) {
        console.log(error)
        toast(`Ocorreu um erro ao deletar o registro id ${certificate.id}, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme: 'dark'
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
        console.log(error)
        toast(`Ocorreu um erro, contate o administrador`, {
          autoClose: 1000,
          position: 'bottom-right',
          theme: 'dark'
        });
      }
    },

    uploadCsv() {
      let input = document.createElement('input');
      input.classList.add('d-none');
      input.type = 'file';
      input.addEventListener('change', async (e) => {
        document.body.removeChild(input);

        let selectedFile = e.target.files[0];

        if (!selectedFile) {
          toast('Nenhum arquivo selecionado.');
          return;
        }

        let formData = new FormData();
        formData.append('file', selectedFile);

        try {
          toast(`Arquivo carregado com sucesso, logo os certificados serão atualizados`, {
              autoClose: 5000,
              position: 'bottom-right',
              theme: 'dark'
          });

          await axios.post(`${import.meta.env.VITE_API_URL}/import_csv/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then(response => {
            switch(response.data.detail) {
              case 'success': 
                toast(`Sucesso ao importar os certificados`, {
                  autoClose: 5000,
                  position: 'bottom-right',
                  theme: 'dark'
                });
              break;
              case 'empty': 
                toast(`Arquivo .csv esta vazio, verifique ou tente novamente.`, {
                  autoClose: 5000,
                  position: 'bottom-right',
                  theme: 'dark'
                });
              break;
              case 'invalid':
                toast(`Arquivo inválido, tente carregar um arquivo .csv válido`, {
                  autoClose: 5000,
                  position: 'bottom-right',
                  theme: 'dark'
                });
              break;
              default:
                toast(`Ocorreu um erro ao realizar a importação`, {
                  autoClose: 5000,
                  position: 'bottom-right',
                  theme: 'dark'
                });
              break;
            }
            this.getCertificates();
          })

        } catch (error) {
          console.error('Erro durante o upload:', error);
        }
      });

      document.body.appendChild(input);
      input.click();
    },

    goto (url) {
      window.open(url, {"target": "_blank"})
    },

    async updateCertificates() {
      try {
        toast(`Iniciando atualização...`, {
            autoClose: 5000,
            position: 'bottom-right',
            theme: 'dark'
        });

        await axios.get(`${import.meta.env.VITE_API_URL}/refresh_certificates/`)
        .then(response => {
          switch(response.data.detail) {
            case 'success': 
              toast(`Sucesso ao atualizar os certificados`, {
                autoClose: 5000,
                position: 'bottom-right',
                theme: 'dark'
              });
            break;
            default:
              toast(`Ocorreu um erro ao realizar a atualização`, {
                autoClose: 5000,
                position: 'bottom-right',
                theme: 'dark'
              });
            break;
          }
          this.getCertificates();
        })

      } catch (error) {
        console.error('Erro durante o upload:', error);
      }
    }
  },
};
</script>