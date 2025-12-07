<template>
  <div class="search-wrapper">
    <div class="search-box">
      <input
        v-model="query"
        @input="onInput"
        @focus="showResults = true"
        @blur="onBlur"
        type="text"
        placeholder="جستجوی محصول..."
      />
      <button @click="submitSearch" class="search-button">
        <i class="fas fa-search"></i>
      </button>
      
      <div v-if="isLoading" class="spinner"></div>
    </div>

  
    <div v-if="showResults && results.length" class="search-results">
      <div
        v-for="product in results"
        :key="product.id"
        class="search-result-card"
        @mousedown.prevent="$router.push(`/product/${product.id}`)"
      >
        <img :src="product.image" alt="product" />
        <div class="info">
          <p class="title">{{ product.title }}</p>
          <p class="price">{{ formatPrice(product.price) }} تومان</p>
        </div>
      </div>
    </div>

    <div v-if="showResults && !results.length && query && !isLoading" class="no-results">
      محصولی یافت نشد
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { productService } from '@/services/ProductService'
import debounce from 'lodash/debounce'

const query = ref('')
const results = ref([])
const showResults = ref(false)
const router = useRouter()

const isLoading = ref(false)

function goToProduct(productId) {
  router.push(`/product/${productId}`)
}

function formatPrice(price) {
  if (!price) return '0'
  return price.toLocaleString('fa-IR')
}


async function submitSearch() {
  if (!query.value) return
  await searchProducts(query.value)
}


const searchProducts = debounce(async (text) => {
  if (!text) {
    results.value = []
    isLoading.value = false
    return
  }
  isLoading.value = true
  try {
    const response = await productService.searchProducts(query.value)
    results.value = response.data
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}, 300)


function onInput() {
  searchProducts(query.value)
}


function onBlur() {
  setTimeout(() => (showResults.value = false), 200)
}
</script>

<style scoped>
.search-wrapper {
  position: relative;
  width: 100%;
  max-width: 700px;
  margin: auto;
  direction: rtl;
}

.search-box {
  display: flex;
  width: 100%;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  height: 44px;
}

.search-box input {
  flex: 1;
  padding: 10px 14px;
  border: none;
  outline: none;
  font-size: 15px;
}

.search-button {
  width: 50px;
  border: none;
  background: white;
  cursor: pointer;
  font-size: 18px;
  border-right: 2px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button i {
  transition: color 0.3s;
}

.search-button:hover i {
  color: #facc15;
}

.search-results {
  position: absolute;
  top: 130px;
  width: 100%;
  max-height: 400px;
  overflow-y: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  z-index: 2000;
}

.search-result-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  cursor: pointer;
  transition: background 0.2s;
}

.search-result-card:hover {
  background: #f9f9f9;
}

.search-result-card img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
}

.search-result-card .info .title {
  font-size: 14px;
  font-weight: 600;
}

.search-result-card .info .price {
  font-size: 13px;
  color: #facc15;
}

.no-results {
  position: absolute;
  top: 130px;
  width: 100%;
  background: white;
  padding: 3px;
  text-align: center;
  color: #888;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}
.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #facc15;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
}

@keyframes spin {
  0% { transform: translateY(-50%) rotate(0deg); }
  100% { transform: translateY(-50%) rotate(360deg); }
}

@media (max-width: 768px) {
  .search-wrapper {
    max-width: 95%;
  }

  .search-box {
    height: 40px;
  }

  .search-box input {
    font-size: 14px;
    padding: 8px 10px;
  }

  .search-button {
    width: 45px;
    font-size: 16px;
  }

  .search-result-card img {
    width: 40px;
    height: 40px;
  }

  .search-result-card .info .title {
    font-size: 13px;
  }

  .search-result-card .info .price {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .search-box {
    height: 38px;
  }

  .search-box input {
    font-size: 13px;
    padding: 6px 8px;
  }

  .search-button {
    width: 40px;
    font-size: 15px;
  }

  .search-result-card img {
    width: 35px;
    height: 35px;
  }

  .search-result-card .info .title {
    font-size: 12px;
  }

  .search-result-card .info .price {
    font-size: 11px;
  }
}
</style>
