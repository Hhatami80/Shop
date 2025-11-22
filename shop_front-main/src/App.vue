<template>
  <Header v-if="!isAdminRoute && !isUserPanel && !isCategoryRoute && !isProductRoute && !isLoginRoute && !isRegisterRoute" />
  
  <router-view></router-view>

  <Footer class="footer" v-if="!isAdminRoute && !isLoginRoute && !isRegisterRoute && !isUserPanel" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed , ref, onMounted } from 'vue'
import Header from './layouts/Header.vue'
import Footer from './layouts/Footer.vue'


const route = useRoute()
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const isUserPanel = computed(() => route.path.startsWith('/user'))
const isCategoryRoute = computed(() => route.path.startsWith('/categories'))
const isProductRoute = computed(() => route.path.startsWith('/product'))
const isLoginRoute = computed(() => route.path.startsWith('/login'))
const isRegisterRoute = computed(() => route.path.startsWith('/register'))




</script>
<style>


html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  /* overflow-x: hidden; */
  scrollbar-width: none;
  background-color: #000;
}
.footer{
  margin-top: 3rem;
}
.my-swal-popup {
  border-radius: 20px !important;
  padding: 35px 40px !important;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  box-shadow: 0 15px 40px rgba(50, 130, 184, 0.3);
  color: #1a1a1a;
  text-align: center;
}

.my-swal-popup .swal2-title {
  font-weight: 900 !important;
  font-size: 26px !important;
  color: #e63946 !important;
  margin-bottom: 12px !important;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.my-swal-popup .swal2-actions {
  display: flex !important;
  justify-content: center;
  gap: 12px;
}
.my-swal-popup .swal2-html-container {
  font-size: 17px !important;
  color: #333 !important;
  margin-bottom: 25px !important;
  line-height: 1.5;
}

.my-swal-confirm {
  background: linear-gradient(135deg, #e63946, #ff6b6b) !important;
  border: none !important;
  color: white !important;
  font-weight: 700 !important;
  font-size: 17px !important;
  padding: 14px 34px !important;
  border-radius: 40px !important;
  margin-right: 12px !important;
  box-shadow: 0 8px 20px rgba(230, 57, 70, 0.4) !important;
  transition: all 0.3s ease-in-out !important;
  text-transform: uppercase;
}

.my-swal-confirm:hover {
  background: linear-gradient(135deg, #ff6b6b, #e63946) !important;
  box-shadow: 0 10px 30px rgba(230, 57, 70, 0.6) !important;
  transform: scale(1.1);
}

.my-swal-cancel {
  background: #adb5bd !important;
  color: #222 !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  padding: 14px 34px !important;
  border-radius: 40px !important;
  border: none !important;
  box-shadow: 0 6px 18px rgba(100, 100, 100, 0.15) !important;
  transition: all 0.3s ease-in-out !important;
  text-transform: uppercase;
  margin-left: 12px !important;
}

.my-swal-cancel:hover {
  background: #868e96 !important;
  box-shadow: 0 8px 24px rgba(100, 100, 100, 0.25) !important;
  transform: scale(1.05);
}
</style>