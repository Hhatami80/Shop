<template>
  <div class="footer-manager">
    <h2>مدیریت فوتر</h2>

    <section class="section-box">
      <h3>تماس با ما</h3>
      <input v-model="footerStore.contact.phone" placeholder="تلفن" />
      <input v-model="footerStore.contact.email" placeholder="ایمیل" />
      <input v-model="footerStore.contact.address" placeholder="آدرس" />
    </section>

    <section class="section-box">
      <h3>پیوندهای مفید</h3>
      <div v-for="(link, index) in footerStore.links" :key="index" class="item">
        <input v-model="link.title" placeholder="متن پیوند" />
        <button @click="removeItem('links', index)">حذف</button>
      </div>
      <button @click="addItem('links')">+ افزودن پیوند</button>
    </section>

    <section class="section-box">
      <h3>سرویس‌ها</h3>
      <div v-for="(service, index) in footerStore.services" :key="index" class="item">
        <input v-model="service.title" placeholder="نام سرویس" />
        <button @click="removeItem('services', index)">حذف</button>
      </div>
      <button @click="addItem('services')">+ افزودن سرویس</button>
    </section>

    <section class="section-box">
      <h3>آدرس تصاویر نمادها</h3>
      <div v-for="(badge, index) in footerStore.badges" :key="index" class="item">
        <img
          v-if="badge.image && badge.image.startsWith('http')"
          :src="badge.image"
          alt="نماد"
          class="badge-preview"
        />
        <input type="file" @change="onFileChange($event, index)" />
        <button @click="footerStore.removeBadge(index)">حذف</button>
      </div>
      <button @click="footerStore.addBadge">+ افزودن تصویر</button>
    </section>

    <button @click="saveFooter" class="save-button">ذخیره تغییرات</button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFooterStore } from '@/stores/useFooterStore'
import { toast } from 'vue3-toastify'

const footerStore = useFooterStore()

onMounted(() => {
  footerStore.fetchFooter()
})

const saveFooter = async () => {
  const success = await footerStore.saveFooter()
  if (success) {
    toast.success('اطلاعات با موفقیت ذخیره شد.')
  } else {
    toast.error('خطا در ذخیره اطلاعات.')
  }
}

const onFileChange = async (event, index) => {
  const file = event.target.files[0]
  if (!file) return
  try {
    await footerStore.uploadBadgeFile(file, index)
  } catch {
    toast.error('خطا در آپلود تصویر')
  }
}

const addItem = (section) => {
  footerStore[section].push({ title: '' })
}

const removeItem = (section, index) => {
  footerStore[section].splice(index, 1)
}
</script>



<style scoped>
.footer-manager {
  --primary-gold: #ffd700;
  --gold-hover: #E6C200;
  --text-dark: #34495e;
  --text-light: #7f8c8d;
  --bg-section: #f9f9f9;
  --border-light: #e9ecef;
  --shadow-light: rgba(0, 0, 0, 0.08);
  --danger-color: #dc3545; 
  --danger-hover: #c82333; 

  background: #fff;
  padding: 40px;
  border-radius: 16px;
  max-width: 850px;
  margin: 40px auto;
  direction: rtl;
  font-family: 'Vazirmatn', sans-serif;
  color: var(--text-dark);
  box-shadow: 0 10px 30px var(--shadow-light);
  border: 1px solid var(--border-light);
}

h2 {
  font-size: 2.2rem;
  margin-bottom: 35px;
  border-bottom: 4px solid var(--primary-gold);
  padding-bottom: 15px;
  color: var(--text-dark);
  font-weight: 900;
  text-align: right;
}

.section-box {
  margin-bottom: 35px;
  padding: 25px;
  border: 1px solid var(--border-light);
  border-radius: 12px;
  background-color: var(--bg-section);
  transition: box-shadow 0.3s ease;
}

.section-box:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.section-box h3 {
  margin-bottom: 20px;
  font-size: 1.6rem;
  color: var(--text-dark);
  font-weight: 700;
  border-bottom: 2px solid var(--primary-gold);
  padding-bottom: 8px;
  display: inline-block;
}

.section-box:first-of-type input {
    width: 95%;
    margin-bottom: 15px;
}

input {
  padding: 14px 18px;
  /* width: 90%; */
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
  color: var(--text-dark);
  font-size: 16px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus {
  outline: none;
  border-color: var(--primary-gold);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.4);
}

.item {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 12px;
  padding: 5px 0;
  background-color: #fff;
  border-radius: 8px;
}

.item input {
  flex-grow: 1;
  margin-bottom: 0;
}
.item input[type='file'] {
    padding: 10px 0;
    border: none;
}

.section-box > button {
  padding: 12px 25px;
  background: var(--primary-gold);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  color: var(--text-dark);
  font-weight: 700;
  transition: 0.3s ease;
  margin-top: 15px;
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.5);
  display: inline-block;
  font-size: 16px;
}

.section-box > button:hover {
  background-color: var(--gold-hover);
  box-shadow: 0 8px 20px rgba(255, 215, 0, 0.7);
  transform: translateY(-2px);
}

.item button {
  background-color: var(--danger-color);
  color: #fff;
  border: 2px solid var(--danger-color); 
  padding: 10px 15px;
  font-weight: 600;
  flex-shrink: 0;
  box-shadow: 0 3px 8px rgba(220, 53, 69, 0.4); 
  font-size: 14px;
  border-radius: 8px; 
  transition: all 0.3s ease;
}

.item button:hover {
  background-color: var(--danger-hover);
  border-color: var(--danger-hover);
  box-shadow: 0 5px 12px rgba(200, 35, 51, 0.6);
  transform: translateY(-1px); 
}

.save-button {
  background-color: var(--text-dark);
  color: #fff;
  font-weight: 800;
  width: 100%;
  margin-top: 50px;
  font-size: 1.2rem;
  padding: 18px;
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 25px rgba(52, 73, 94, 0.4);
  transition: background-color 0.3s, box-shadow 0.3s, transform 0.3s;
}

.save-button:hover {
  background-color: #2c3e50;
  box-shadow: 0 12px 30px rgba(52, 73, 94, 0.6);
  transform: translateY(-2px);
}

.badge-preview {
  width: 55px;
  height: 55px;
  object-fit: contain;
  border-radius: 8px;
  margin-left: 15px;
  border: 2px solid var(--primary-gold);
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}
</style>