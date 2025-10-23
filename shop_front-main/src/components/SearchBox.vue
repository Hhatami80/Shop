<template>
  <div class="search-btn">
    <button @click="submitSearch" class="search-button">
      <i class="fas fa-search"></i>
    </button>
  </div>
  <div class="search-box">
    <input v-model="query" @keyup.enter="submitSearch" type="text" placeholder="جستجوی محصول..." />
    
  </div>
  
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['search'])
const query = ref('')

function submitSearch() {
  emit('search', query.value)
}
</script>

<style scoped>
.search-box {
  direction: rtl;
  font-family: 'Yekan';
  display: flex;
  align-items: center;
  background: white;
  border-radius:0 8px 8px 0;
  overflow: hidden;
  width: 100%;
  height: 40px;
  max-width: 800px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
:deep(input::placeholder) {
  color: #000;
  font-weight: bold;
  font-size: 15px;
}
.search-box input {
  flex: 1;
  font-family: 'Yekan';
  padding: 10px 16px;
  border: none;
  outline: none;
  font-size: 14px;
  height: 100%;
  color: black;
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  height: 100%;
  background-color: white;
  border: none;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
  font-size: 18px;
  border-right: 4px solid #000;
}

.search-button i {
  color: #000;
}
.search-btn{
height: 40px;

}
</style>
