<template>
  <footer
    class="footer"
    v-if="footerStore.links.length || footerStore.services.length || footerStore.badges.length"
  >
    <div class="footer-column section1">
      <h4>تماس با ما</h4>
      <ul class="contact-list">
        <li>
          <i class="fas fa-phone"></i>
          <span>تلفن: {{ footerStore.contact?.phone }}</span>
        </li>
        <li>
          <i class="fas fa-envelope"></i>
          <span>ایمیل: {{ footerStore.contact?.email }}</span>
        </li>
        <li>
          <i class="fas fa-map-marker-alt"></i>
          <span>آدرس: {{ footerStore.contact?.address }}</span>
        </li>
      </ul>

      <div class="social-icons">
        <a href="#" class="social-icon" title="تلگرام">
          <i class="fab fa-telegram-plane"></i>
        </a>
        <a href="#" class="social-icon" title="اینستاگرام">
          <i class="fab fa-instagram"></i>
        </a>
        <a href="#" class="social-icon" title="واتساپ">
          <i class="fab fa-whatsapp"></i>
        </a>
      </div>
    </div>

    <div class="footer-column">
      <h4>پیوندهای مفید</h4>
      <ul>
        <li v-for="(link, index) in footerStore.links" :key="index">
          <a href="#">{{ link.title }}</a>
        </li>
      </ul>
    </div>

    <div class="footer-column">
      <h4>سرویس‌های ما</h4>
      <ul>
        <li v-for="(service, index) in footerStore.services" :key="index">
          <a href="#">{{ service.title }}</a>
        </li>
      </ul>
    </div>

    <div class="footer-column section2">
      <h4>نمادها</h4>
      <div class="image-container">
        <img
          v-for="(badge, index) in footerStore.badges"
          :key="index"
          :src="badge.image"
          alt="badge"
        />
      </div>
    </div>
  </footer>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFooterStore } from '@/stores/useFooterStore'

const footerStore = useFooterStore()

onMounted(() => {
  footerStore.fetchFooter()
})
</script>

<style scoped>
.footer {
  background-color: #000;
  color: #f5f5f5;
  display: flex;
  justify-content: space-between;
  padding: 50px 40px;
  border-radius: 8px;
  font-family: 'Yekan', sans-serif;
  direction: rtl;
  gap: 40px;
  position: relative;
  flex-wrap: wrap;
}


.footer-column {
  flex: 1 1 220px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}


.footer-column h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #fff;
}


.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column ul li {
  font-size: 14px;
  margin-bottom: 8px;
}

.footer-column ul li a {
  color: #ccc;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-column ul li a:hover {
  color: #ffc107;
}


.contact-list li {
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-list i {
  color: #ffc107;
  font-size: 16px;
}


.social-icons {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 15px;
}

.social-icon {
  background-color: #222;
  color: #ffc107;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  transition: background 0.3s ease, transform 0.3s ease;
}

.social-icon:hover {
  background-color: #ffc107;
  color: #000;
  transform: scale(1.1);
}


.image-container {
  display: flex;
  gap: 15px;
  background-color: #111;
  padding: 15px;
  border-radius: 8px;
}

.image-container img {
  width: 80px;
  height: auto;
  border-radius: 6px;
  object-fit: contain;
}


@media (max-width: 768px) {
  .footer {
    flex-direction: column;
    align-items: center;
    padding: 30px 20px;
  }

  .footer-column {
    align-items: center;
    text-align: center;
  }

  .social-icons {
    position: static;
    transform: none;
    margin-bottom: 20px;
  }

  .image-container {
    justify-content: center;
  }
}

</style>
