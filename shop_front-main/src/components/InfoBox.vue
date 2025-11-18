<template>
  <div class="info-box">
    <div class="icon">
      <i :class="iconClass"></i>
    </div>
    <div class="content">
      <p class="label">{{ label }}</p>
      <p class="value">{{ value }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: { type: String, required: true },
    value: { type: [String, Number], required: true },
    iconClass: { type: String, default: 'fas fa-info' },
  },
}
</script>

<style scoped>
.info-box {
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(12px);
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1 1 220px;
  border-top: 5px solid #f1c40f; 
  transition: transform 0.3s, box-shadow 0.3s;
}
.info-box:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}
.icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000; 
  font-size: 1.8rem;
  flex-shrink: 0;
  transition: transform 0.3s, background 0.3s;
}
.info-box:hover .icon {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.35);
}
.content {
  display: flex;
  flex-direction: column;
}
.label {
  font-size: 0.95rem;
  color: #7f6a3e;
  font-weight: 500;
  margin-bottom: 5px;
}
.value {
  font-size: 1.6rem;
  font-weight: bold;
  color: #ffd700;
  white-space: pre-line;
}
@media (max-width: 1024px) {
  .cards {
    flex-wrap: wrap;
  }
}
@media (max-width: 768px) {
  .cards {
    flex-direction: column;
  }
}
</style>
