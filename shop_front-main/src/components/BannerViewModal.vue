<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="true" class="modal-backdrop" @click="$emit('close')">
        <div class="modal-panel" @click.stop>
          <div class="modal-header">
            <h3>بنرهای دسته‌بندی</h3>
            <button class="close-btn" @click="$emit('close')" aria-label="بستن">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path
                  d="M18 6L6 18M6 6L18 18"
                  stroke="currentColor"
                  stroke-width="2.5"
                  stroke-linecap="round"
                />
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div v-if="banners.length" class="banners-grid">
              <div v-for="(b, index) in banners" :key="index" class="banner-card">
                <div class="image-wrapper">
                  <img :src="b.image" :alt="b.text || 'بنر ' + (index + 1)" class="banner-image" />
                </div>
                <p v-if="b.text" class="banner-caption">{{ b.text }}</p>
                <small v-else class="no-caption">بدون متن</small>
              </div>
            </div>

            <div v-else class="empty-state">
              <svg
                width="64"
                height="64"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <circle cx="8" cy="8" r="2" />
                <path d="M21 15L16 10L5 21" />
              </svg>
              <p>هیچ بنری برای این دسته‌بندی اضافه نشده است.</p>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-close" @click="$emit('close')">بستن</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  banners: {
    type: Array,
    default: () => [],
  },
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.32s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal-panel,
.modal-leave-to .modal-panel {
  transform: scale(0.92);
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-panel {
  background: #fff;
  border-radius: 20px;
  width: 100%;
  max-width: 780px;
  max-height: 92vh;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.22);
  overflow: hidden;
  direction: rtl;
  font-family: 'IRANSansX', sans-serif;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem 1.8rem 1.2rem;
  background: linear-gradient(135deg, #f9c710, #e6b800);
  color: #111;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.55rem;
  font-weight: 900;
}

.close-btn {
  background: none;
  border: none;
  color: #111;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 1.8rem;
  background: #fdfdfd;
}

.banners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.8rem;
  justify-items: center;
}

.banner-card {
  background: #fff;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  width: 100%;
  max-width: 280px;
}

.banner-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
}

.image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  background: #f0f0f0;
  overflow: hidden;
}

.banner-image {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.banner-card:hover .banner-image {
  transform: scale(1.05);
}

.banner-caption {
  padding: 1rem 0.8rem;
  text-align: center;
  font-weight: 600;
  color: #222;
  font-size: 1rem;
  margin: 0;
  background: #fff;
}

.no-caption {
  padding: 0.8rem;
  text-align: center;
  color: #999;
  font-style: italic;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #888;
}

.empty-state svg {
  color: #ccc;
  margin-bottom: 1rem;
}

.empty-state p {
  margin: 0.5rem 0 0;
  font-size: 1.1rem;
  font-weight: 500;
}

.modal-footer {
  padding: 1.4rem 1.8rem;
  background: #f9fafb;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.btn-close {
  padding: 0.9rem 2.5rem;
  background: #f9c710;
  color: #111;
  border: none;
  border-radius: 14px;
  font-weight: 900;
  font-size: 1.05rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 18px rgba(249, 199, 16, 0.4);
}

.btn-close:hover {
  background: #e6b800;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(249, 199, 16, 0.5);
}
</style>
