<template>
  <div>
    <header v-if="!onlySticky" class="header-main">
      <button ref="menuBtn" class="menu-btn" @click="toggleMenu">☰</button>
      <img
        v-if="headerStore.site_logo"
        :src="headerStore.site_logo"
        alt="لوگو"
        class="logo"
      />
      <img v-else src="" alt="لوگو" class="logo" />
    </header>

    <StickyHeader
      :visible="showStickyHeader || onlySticky"
      :compact="compactSticky"
      @toggle-menu="toggleMenu"
    />
    <transition name="slide-fade">
      <div
        v-if="drawerOpen"
        class="menu-box"
        :style="menuStyle"
        @click.self="drawerOpen = false"
      >
        <button class="close-btn" @click="drawerOpen = false">×</button>
        <ul>
          <li v-for="item in headerStore.menuItems" :key="item.id">
            <template v-if="item.url?.startsWith?.('#')">
              <a href="#" @click.prevent="scrollToSection(item.url)">
                {{ item.title }}
              </a>
            </template>
            <template v-else>
              <router-link :to="item.url">{{ item.title }}</router-link>
            </template>
          </li>
        </ul>
      </div>
    </transition>
    <div v-if="!onlySticky" class="search-wrapper">
      <SearchBox />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from "vue";
import { useHeaderStore } from "@/stores/useHeaderStore";
import SearchBox from "@/components/SearchBox.vue";
import StickyHeader from "@/components/StickyHeader.vue";

const props = defineProps({
  onlySticky: { type: Boolean, default: false },
  compactSticky: { type: Boolean, default: false },
});

const drawerOpen = ref(false);
const showStickyHeader = ref(false);
const headerStore = useHeaderStore();
const menuBtn = ref(null);
const menuStyle = ref({
  position: "fixed",
  top: "0px",
  left: "100%", 
});

onMounted(() => {
  headerStore.fetchHeader();
  headerStore.fetchlogo();
  window.addEventListener("scroll", handleScroll);
});
onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

function handleScroll() {
  showStickyHeader.value = window.scrollY > 200;
}
function scrollToSection(selector) {
  const el = document.querySelector(selector);
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
    drawerOpen.value = false;
  }
}

async function toggleMenu() {
  drawerOpen.value = !drawerOpen.value;
  if (drawerOpen.value) {
    await nextTick();
    const rect = menuBtn.value?.getBoundingClientRect();
    if (rect) {
      const menuWidth = 230;
      const topOffset = 10;

      if (rect.right + menuWidth > window.innerWidth) {
        menuStyle.value = {
          position: "fixed",
          top: `${rect.bottom + topOffset}px`,
          left: `${rect.left - menuWidth}px`,
        };
      } else {
        menuStyle.value = {
          position: "fixed",
          top: `${rect.bottom + topOffset}px`,
          left: `${rect.right + 10}px`,
        };
      }
    }
  }
}
</script>

<style scoped>
.header-main {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: white;
  border-bottom: 1px solid gold;
  position: relative;
  direction: rtl;
  transition: all 0.3s ease;
}

.logo {
  height: 300px;
  max-width: 90%;
  object-fit: contain;
}

.menu-btn {
  position: absolute;
  right: 20px;
  top: 50px;
  font-size: 30px;
  background: none;
  border: none;
  cursor: pointer;
}

.search-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
  height: 100px;
}

.menu-box {
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 15px 20px 20px;
  z-index: 2000;
  min-width: 220px;
}

.menu-box ul {
  direction: rtl;
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-box ul li {
  margin-bottom: 12px;
}

.menu-box ul li a {
  text-decoration: none;
  font-weight: 600;
  color: #333;
  transition: color 0.3s;
}

.menu-box ul li a:hover {
  color: gold;
}

.close-btn {
  position: absolute;
  top: 8px;
  left: 8px;
  font-size: 22px;
  background: none;
  border: none;
  cursor: pointer;
}

.close-btn:hover {
  color: red;
}


.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}


.slide-fade-enter-from {
  transform: translateX(100%);
  opacity: 0;
}


.slide-fade-enter-to {
  transform: translateX(0);
  opacity: 1;
}


.slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}



@media (max-width: 1024px) {
  .header-main {
    height: 220px;
    padding: 15px;
  }
  .logo {
    height: 180px;
  }
  .menu-btn {
    font-size: 26px;
    top: 40px;
  }
  .search-wrapper {
    margin-top: 30px;
    height: 80px;
  }
}

@media (max-width: 768px) {
  .header-main {
    height: auto;
    flex-direction: column;
    justify-content: flex-start;
    padding: 10px 15px;
    text-align: center;
  }
  .logo {
    height: 120px;
    margin: 10px auto;
  }
  .menu-btn {
    top: 10px;
    right: 10px;
  }
  .search-wrapper {
    margin-top: 15px;
    height: auto;
    padding: 10px;
  }
  .menu-box {
    min-width: 90%;
    top: 60px !important;
    left: 5% !important;
  }
}

@media (max-width: 480px) {
  .header-main {
    padding: 5px 10px;
  }
  .logo {
    height: 100px;
  }
  .menu-btn {
    font-size: 24px;
    top: 5px;
    right: 5px;
  }
  .search-wrapper {
    margin-top: 10px;
    height: auto;
  }
  .menu-box {
    min-width: 95%;
    padding: 10px 15px;
  }
}

</style>
