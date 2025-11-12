<template>
  <div class="search-container">
    <div class="search-box">
      <input
        v-model="query"
        @keyup.enter="submitSearch"
        type="text"
        placeholder="جستجوی محصول..."
      />
      <button @click="submitSearch" class="search-button">
        <i class="fas fa-search"></i>
      </button>
    </div>
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

.search-container {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 10px;
}

.search-box {
  direction: rtl;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  width: 100%;
  max-width: 800px;
  height: 44px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}


.search-box input {
  flex: 1;
  padding: 10px 14px;
  border: none;
  outline: none;
  font-size: 15px;
  height: 100%;
  color: #000;
  background: transparent;
}

:deep(input::placeholder) {
  color: #000;
  font-weight: 500;
  font-size: 14px;
}


.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  height: 100%;
  background-color: white;
  border: none;
  border-right: 3px solid #000;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.3s ease;
}

.search-button:hover i {
  color: #facc15;
}

.search-button i {
  color: #000;
  transition: color 0.3s ease;
}

@media (max-width: 480px) {
  .search-box {
    height: 38px;
    max-width: 95%;
  }

  .search-box input {
    font-size: 13px;
    padding: 8px 10px;
  }

  .search-button {
    padding: 0 10px;
    font-size: 16px;
    border-right: 2px solid #000;
  }
}

@media (max-width: 768px) {
  .search-box {
    max-width: 600px;
    height: 40px;
  }

  .search-box input {
    font-size: 14px;
  }

  .search-button {
    font-size: 17px;
  }
}

@media (max-width: 1024px) {
  .search-box {
    max-width: 700px;
  }
}
</style>
