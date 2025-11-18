<template>
  <div class="loader-overlay" v-if="isVisible">
    <img class="loader-logo" :src="logo" alt="Loading..." />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  logo: String, 
})

const isVisible = ref(true)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = false
  }, 2000) 
})
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  z-index: 9999;
}

.loader-logo {
  width: 120px;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
    transform: scale(0.9);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0.6;
    transform: scale(0.9);
  }
}
</style>
