<template>
  <div class="header-manager">
    <h2>مدیریت هدر</h2>

    <section class="section-box">
      <h3>لوگو</h3>

      <input type="file" @change="onFileChange" accept="image/*" />

      <div v-if="headerStore.site_logo" class="logo-preview">
        <img :src="headerStore.site_logo" alt="لوگو" />
        <!-- <button class="remove-logo" @click="removeLogo">حذف لوگو</button> -->
      </div>
    </section>

    <section class="section-box">
      <h3>منوها</h3>

      <draggable
        v-model="headerStore.menuItems"
        item-key="id"
        handle=".drag-handle"
        animation="200"
        class="draggable-list"
      >
        <template #item="{ element, index }">
          <div class="item">
            <span class="drag-handle">⠿</span>
            <input type="text" v-model="element.title" placeholder="متن منو" />
            <input type="text" v-model="element.url" placeholder="لینک" />
            <button @click="headerStore.removeMenuItem(index)">حذف</button>
          </div>
        </template>
      </draggable>

      <button @click="headerStore.addMenuItem">+ افزودن منو</button>
    </section>

    <button class="save-button" @click="headerStore.saveHeader">ذخیره تغییرات</button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useHeaderStore } from '@/stores/useHeaderStore'
import draggable from 'vuedraggable'

const headerStore = useHeaderStore()

onMounted(() => {
  headerStore.fetchHeader()
})

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
   headerStore.site_logo = URL.createObjectURL(file)
  headerStore.uploadLogo(file)
}

const removeLogo = () => {
  headerStore.setLogoUrl('')
}
</script>

<style scoped>
.header-manager {
  --primary-gold: #ffd700;
  --gold-hover: #E6C200;
  --text-dark: #34495e;
  --text-light: #7f8c8d;
  --bg-form: #fcfcfc;
  --border-light: #e9ecef;
  --shadow-light: rgba(0, 0, 0, 0.08);

  max-width: 700px;
  margin: 40px auto;
  background: var(--card-bg, #fff);
  color: var(--text-dark);
  padding: 30px;
  border-radius: 12px;
  font-family: 'Vazirmatn', sans-serif;
  direction: rtl;
  box-shadow: 0 8px 30px var(--shadow-light);
  border: 1px solid var(--border-light);
}

h2 {
  color: var(--text-dark);
  border-bottom: 3px solid var(--primary-gold);
  padding-bottom: 15px;
  margin-bottom: 30px;
  font-weight: 800;
  font-size: 2rem;
  text-align: right;
}

h3 {
  color: var(--text-dark);
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.section-box {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  background-color: var(--bg-form);
}

.item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.drag-handle {
  cursor: grab;
  color: var(--primary-gold);
  font-size: 24px;
  user-select: none;
  transition: transform 0.2s;
}
.drag-handle:active {
  cursor: grabbing;
  transform: scale(1.1);
}

input[type='text'] {
  flex-grow: 1;
  padding: 10px 15px;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  color: var(--text-dark);
  font-size: 15px;
  transition: border-color 0.3s, box-shadow 0.3s;
}
input:focus {
  outline: none;
  border-color: var(--primary-gold);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.4);
}
input[type='text']:focus {
  border-color: var(--primary-gold);
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
  background-color: #fff;
}

input[type='text']::placeholder {
  color: var(--text-light);
}

input[type='file'] {
  margin-top: 8px;
  padding: 10px 0;
  color: var(--text-light);
  font-size: 14px;
}

.logo-preview {
  margin-top: 15px;
  position: relative;
  display: inline-block;
}

.logo-preview img {
  max-width: 150px;
  height: auto;
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--primary-gold); 
  transition: transform 0.3s;
}
.logo-preview img:hover {
    transform: scale(1.03);
}

button {
  background-color: #fff;
  border: 2px solid var(--primary-gold);
  border-radius: 8px;
  color: var(--primary-gold);
  font-weight: 600;
  padding: 10px 18px;
  cursor: pointer;
  transition: 0.3s;
  font-size: 15px;
}
.item button {
  border: none;
  background-color: #dc3545;
  color: #fff;
  padding: 8px 12px;
  font-weight: 500;
  font-size: 14px;
}
.item button:hover {
  background-color: #c82333;
  box-shadow: none;
}

.section-box > button:hover {
  background-color: var(--primary-gold);
  color: var(--text-dark);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}
.save-button {
  width: 100%;
  font-weight: 800;
  font-size: 18px;
  background-color: var(--primary-gold);
  color: var(--text-dark);
  padding: 15px;
  border-radius: 10px;
  border: none;
  margin-top: 30px;
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.5);
}

.save-button:hover {
  background-color: var(--gold-hover);
  box-shadow: 0 8px 20px rgba(230, 194, 0, 0.7);
  transform: translateY(-2px);
}
</style>