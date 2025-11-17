<template>
  <div class="main-banner">
    <div class="left-section">
      <div v-for="(item, idx) in staticItems" :key="idx" class="static-box">
        <div class="side-icon">
          <img :src="item.icon" alt="" />
        </div>
        <div class="info">
          <h4>{{ item.title }}</h4>
          <p>{{ item.subtitle }}</p>
        </div>
        <div class="icon-btn" @click="goTo(item.route)">
          <i class="fas fa-chevron-left"></i>
          <i class="fas fa-chevron-left"></i>
          <i class="fas fa-chevron-left"></i>
        </div>
      </div>
    </div>

    <div class="right-section" v-if="!loading && banner">
      <img :src="banner.image" alt="banner" class="banner-img" />
      <div class="banner-content">
        <h2>{{ banner.title }}</h2>
        <p>{{ banner.subtitle }}</p>
        <button class="shop-btn">فروشگاه</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useFeatureSectionStore } from '@/stores/FeatureSectionStore'
import { useRouter } from 'vue-router'
import cat1 from '@/assets/image/icons/cat1.png'
import cat2 from '@/assets/image/icons/cat2.png'
import cat3 from '@/assets/image/icons/cat3.png'

const router = useRouter()
const store = useFeatureSectionStore()

const banner = computed(() => {
  if (!store.featureSection || !store.featureSection.banner) return null
  return store.featureSection.banner[0]
})

const loading = computed(() => store.loading)
const goTo = (route) => {
  router.push(route)
}

const staticItems = [
  {
    title: 'پیشنهادهای ویژه',
    subtitle: 'و امتیازات ویژه',
    icon: cat1,
    route: '/special-offers',
  },
  {
    title: 'ارسال سریع و رایگان',
    subtitle: 'تمامی نقاط کشور',
    icon: cat2,
    route: '/fast-shipping',
  },
  {
    title: 'سفارشی‌سازی',
    subtitle: 'حک پیام روی محصول',
    icon: cat3,
    route: '/custom-products',
  },
]

onMounted(() => {
  store.getFeatureSection()
})
</script>

<style scoped>
.main-banner {
  direction: rtl;
  display: flex;
  flex-direction: row-reverse;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  margin: 0 3px;
  min-height: 400px;
}
.left-section {
  background: #ffe7b3;
  width: 40%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
  gap: 12px;
}

.static-box {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 12px 20px;
  border-bottom: 1px solid #ddd;
  gap: 12px;
  flex: 1;
  transition: all 0.3s;
  border-radius: 10px;
  background: #fff4d6;
}

.side-icon img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  flex-shrink: 0;
}

.info {
  flex: 1;
  margin: 0;
  text-align: right;
}

.icon-btn {
  cursor: pointer;
  background: #ffb800;
  padding: 8px;
  border-radius: 8px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-btn i {
  font-size: 12px;
  margin-left: 2px;
}

.right-section {
  background: #002833;
  color: white;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  width: 60%;
  display: flex;
  flex-direction: column;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.banner-content {
  position: absolute;
  right: 10%;
  top: 50%;
  transform: translateY(-50%);
  text-align: right;
  color: white;
  max-width: 80%;
  z-index: 1;
}

.banner-content h2 {
  font-size: 28px;
  margin-bottom: 8px;
}

.banner-content p {
  font-size: 16px;
  margin-bottom: 12px;
}

.shop-btn {
  margin-top: 12px;
  background: #f9c710;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  font-weight: bold;
  color: #222;
  transition: 0.3s;
}
.shop-btn:hover {
  background: #e5b809;
}


@media (max-width: 1024px) {
  .main-banner {
    min-height: 350px;
  }
}

@media (max-width: 768px) {
  .main-banner {
    flex-direction: column-reverse;
    min-height: auto;
  }

  .left-section,
  .right-section {
    width: 100%;
    padding: 12px;
  }

  .right-section {
    height: 300px;
  }

  .banner-img {
    height: 100%;
  }

  .banner-content {
    right: 5%;
    bottom: 10%;
    top: auto;
    transform: none;
    text-align: center;
    max-width: 90%;
  }

  .static-box {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 10px;
    gap: 8px;
  }

  .side-icon img {
    width: 40px;
    height: 40px;
    margin: 0;
  }

  .icon-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .main-banner {
    border-radius: 8px;
  }

  .right-section {
    height: 220px;
    position: relative;
  }
  .right-section img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .banner-content h2 {
    font-size: 18px;
  }

  .banner-content p {
    font-size: 12px;
  }

  .shop-btn {
    padding: 6px;
  }

  .side-icon img {
    width: 35px;
    height: 35px;
  }
  .icon-btn{
    width: 40px;
  }

  .static-box {
    gap: 6px;
    padding: 8px;
  }
}
</style>
