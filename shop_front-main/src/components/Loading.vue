<template>
  <transition name="fade-loader">
    <div class="loader-overlay" v-if="modelValue">
      <img class="loader-logo" :src="logo" alt="Loading..." />
    </div>
  </transition>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  logo: String,
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

.fade-loader-enter-active,
.fade-loader-leave-active {
  transition: opacity 0.6s ease;
}

.fade-loader-enter-from,
.fade-loader-leave-to {
  opacity: 0;
}
</style>
