<template>
  <div class="pagination-wrapper" v-if="totalPages > 1">
    <!-- Prev -->
    <button
      class="pagination-btn"
      :disabled="page <= 1"
      @click="changePage(page - 1)"
    >
      قبلی
    </button>

    <!-- Page Numbers -->
    <ul class="pagination-list">
      <li
        v-for="p in pages"
        :key="p"
        :class="{ active: p === page }"
        @click="changePage(p)"
      >
        {{ p }}
      </li>
    </ul>

    <!-- Next -->
    <button
      class="pagination-btn"
      :disabled="page >= totalPages"
      @click="changePage(page + 1)"
    >
      بعدی
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  maxPages: { type: Number, default: 5 }
})

const emit = defineEmits(["page-change"])

const pages = computed(() => {
  const total = props.totalPages
  const current = props.page
  const max = props.maxPages

  const half = Math.floor(max / 2)
  let start = Math.max(1, current - half)
  let end = Math.min(total, current + half)

  if (end - start + 1 < max) {
    if (start === 1) end = Math.min(total, start + max - 1)
    else if (end === total) start = Math.max(1, end - max + 1)
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

function changePage(p) {
  if (p >= 1 && p <= props.totalPages) {
    emit("page-change", p)
  }
}
</script>

<style scoped>
.pagination-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 1rem;
}

.pagination-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background: #f0f0f0;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.pagination-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.pagination-list {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 6px;
}

.pagination-list li {
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  background: #f9f9f9;
  transition: background 0.3s, transform 0.2s;
}

.pagination-list li.active {
  background: gold;
  color: black;
  font-weight: bold;
  transform: scale(1.1);
}

.pagination-list li:hover:not(.active) {
  background: #eee;
}
</style>
