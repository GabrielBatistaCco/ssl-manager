<template>
    <v-layout v-for="modal in modais">
        <v-dialog v-model="modal.dialog" dark :class="['modal', `modal-size-${modal.size}`]">
            <v-card dark>
                <v-card-title class="text-center header-sticky">
                    {{ modal.title }}
                    <div v-if="modal.showCloseButton" class="btn-close" @click.native="modal.dialog = false">
                        <v-icon color="#fff" class="mdi-close mdi cursor-pointer" title="Fechar"></v-icon>
                    </div>
                </v-card-title>
                <v-card-text v-if="modal.body && !(modal.tableHeaders && modal.tableItems)" v-html="modal.body"></v-card-text>
                <v-data-table 
                    v-if="modal.tableHeaders && modal.tableItems"
                    :headers="modal.tableHeaders"
                    :items="modal.tableItems" 
                    theme="dark"
                    height="700"
                    :fixed-header="true"
                    :items-per-page="itemsPerPage"
                    class="table-modal"
                >
                    <template v-slot:item.table_json = "{ item }">
                        <span v-html="item.table_json"></span>
                    </template>
                    <template v-slot:bottom>
                        <!-- PARA OCULTAR O BOTTOM -->
                    </template>
                </v-data-table>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn v-if="modal.cancelButtonText" :color="modal.type" flat @click.native="modal.dialog = false">{{ modal.cancelButtonText }}</v-btn>
                    <v-btn v-if="modal.confirmButtonText" :color="modal.type" flat @click.native="modal.dialog = false">{{ modal.confirmButtonText }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
export default {
    name: 'Modal',
    props: [
        'modais'
    ],
    data() {
        return{
            itemsPerPage: 0
        }
    },
    methods: {
        defaultModal(modal) {
            modal.title             = modal.title               ? modal.title               : "";
            modal.text              = modal.text                ? modal.text                : "teste";
            modal.confirmButtonText = modal.confirmButtonText   ? modal.confirmButtonText   : false;
            modal.closeButtonText   = modal.closeButtonText     ? modal.closeButtonText     : false;
            modal.cancelButtonText  = modal.cancelButtonText    ? modal.cancelButtonText    : false;
            modal.showCloseButton   = modal.showCloseButton     ? modal.showCloseButton     : true;
            modal.customClass       = modal.customClass         ? modal.customClass         : "";
            modal.size              = modal.size                ? modal.size                : "md";
            modal.type              = modal.type                ? modal.type                : "success";
            modal.dialog            = modal.dialog === false    ? modal.dialog              : true;
            modal.body              = modal.body                ? modal.body                : `
                <div class="d-flex justify-center">
                    <i class="v-icon mdi-check-bold mdi text-success text-center" style="font-size: 100px;"></i>
                </div>
            `;
            return modal;
        },
    },
    beforeUpdate() {
        this.$props.modais.forEach(e => this.defaultModal(e))
    },
    beforeUnmount() {
        this.$props.modais = []
    }
}
</script>

<style >
.modal .v-overlay__content{
    position: relative;
}

.modal .v-card {
    background-color: #222020;
}

.modal .header-sticky {
    position: sticky;
    top: 0;
    background-color: #222020;
    color: #ffffff;
}

.modal .header-sticky .btn-close {
    position: absolute;
    top: 10px;
    right: 15px;
}

.modal.modal-size-sm {
    max-width: 400px;
    width: 80vw;
}

.modal.modal-size-md {
    max-width: 700px;
    width: 80vw;
}

.modal.modal-size-lg {
    max-width: 1100px;
    width: 80vw;
}

.modal.modal-size-xl {
    max-width: 1600px;
    width: 80vw;
}

.cursor-pointer {
    cursor: pointer;
}
</style>
