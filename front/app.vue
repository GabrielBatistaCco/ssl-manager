<template>
  <div>
    <NuxtLayout class="layouts">
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script>
import axios from 'axios'
async function loadItemsStorage() {
  let status_ssl_options = (await axios.get(`/status_ssl_options.json`)).data;
  status_ssl_options = JSON.stringify(status_ssl_options)
  localStorage.setItem('status_ssl_options', status_ssl_options)
  
  let product_name_options = (await axios.get(`/product_name_options.json`)).data;
  product_name_options = JSON.stringify(product_name_options)
  localStorage.setItem('product_name_options', product_name_options)

  // let certificates = (await axios.get(`${ import.meta.env.VITE_API_URL }/certificates/`)).data
  // certificates = certificates.slice()
  // certificates = JSON.stringify(certificates)
  // localStorage.setItem('first_certificates', certificates);
}

loadItemsStorage()

</script>