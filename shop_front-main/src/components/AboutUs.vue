<template>
  <section v-if="!loading && !error" class="about-us">
    <div class="content">
      <h2>{{ title }}</h2>
      <p>{{ text }}</p>
      <button>بیشتر بدانید</button>
    </div>
    <div class="image">
      <img :src="imageurl" alt="About Us" />
    </div>
  </section>

  <p v-else-if="loading">در حال بارگذاری...</p>
  <p v-else>{{ error }}</p>
</template>

<script setup>
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useAboutUsStore } from "@/stores/useAboutUsStore";

const aboutStore = useAboutUsStore();
const { title, text, imageurl, loading, error } = storeToRefs(aboutStore);

onMounted(() => {
  aboutStore.fetchAbout();
});
</script>

<style scoped>
.about-us {
  font-family: "Yekan";
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  padding: 3rem 6rem;
  background-color: #ffffff;
  border-radius: 12px;
  direction: rtl;
  flex-wrap: wrap;
  color: #111111;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.05);
}

.content {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
  text-align: right;
  margin-right: auto;
  margin-left: auto;
}

.image {
  flex: 1;
  min-width: 250px;
  text-align: center;
  margin-left: -40px;
}

.image img {
  max-width: 90%;
  max-height: 400px;
  border-radius: 12px;
  object-fit: cover;
  margin: 0 auto;
  display: block;
}

.content h2 {
  color: #f9c710;
  margin-bottom: 1rem;
  font-size: 2rem;
}
.content p {
  line-height: 1.6;
  color: #222222;
  margin-bottom: 1.5rem;
}
.content button {
  background-color: #f9c710;
  border: none;
  color: #111;
  padding: 0.7rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.content button:hover {
  background-color: #f9c710;
}

.loading {
  padding: 2rem;
  text-align: center;
  font-size: 1.2rem;
  color: #777;
  background-color: #fff;
}
.fallback {
  background-color: #f9f7f1;
  color: #333333;
}
@media (max-width: 768px) {
  .about-us {
    flex-direction: column-reverse;
    text-align: center;
  }
  .content button {
    width: 100%;
  }
  .image {
    margin-bottom: 1.5rem;
  }
}
</style>
