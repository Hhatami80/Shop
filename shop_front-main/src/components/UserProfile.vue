<template>
  <div class="profile-card">
    <h3>پروفایل کاربری</h3>

  
    <div class="profile-tabs">
      <router-link
        to="/user/profile/info"
        class="tab-btn"
        :class="{ active: $route.path.endsWith('/info') }"
      >
        مشخصات فردی
      </router-link>
      <router-link
        to="/user/profile/addresses"
        class="tab-btn"
        :class="{ active: $route.path.endsWith('/addresses') }"
      >
        آدرس‌ها
      </router-link>
      <router-link
        to="/user/profile/bank"
        class="tab-btn"
        :class="{ active: $route.path.endsWith('/bank') }"
      >
        حساب بانکی
      </router-link>
    </div>

  
    <div class="tab-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.profile-card {
  background: linear-gradient(180deg, #ffffff 0%, #fdfaf3 100%);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
}

.profile-tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 24px;
  border-radius: 25px;
  border: none;
  background: #f3f3f3;
  color: #555;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.tab-btn.active {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  box-shadow: 0 4px 10px rgba(249, 199, 16, 0.4);
}

.tab-content {
  margin-top: 20px;
}
</style>
