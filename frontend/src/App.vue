<script>
import Navbar from './component/Navbar.vue'
import Footer from './component/Footer.vue'

export default {
    data() {
        return {}
    },
    components: {
        Navbar,
        Footer
    }
}
</script>


<template>
  <Navbar />
  <router-view />
  <Footer />  
</template>

<style scoped></style>
