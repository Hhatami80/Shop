<template>
  <div class="info-box" @click="navigate" role="button" tabindex="0" @keydown.enter="navigate">
    <div class="icon-wrapper">
      <i :class="iconClass"></i>
    </div>
    <div class="content">
      <p class="label">{{ label }}</p>
      <p class="value">{{ value }}</p>
      <slot></slot>
    </div>
    <div class="shine"></div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { defineProps } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  iconClass: { type: String, default: 'fas fa-chart-line' },
  route: { type: String, default: null }
})

const router = useRouter()

const navigate = () => {
  if (props.route) {
    router.push(props.route)
  }
}
</script>

<style scoped>
.info-box {
  position: relative;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 24px;
  padding: 2rem 1.5rem;
  text-align: center;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.08),
    0 4px 15px rgba(249, 199, 16, 0.1);
  border: 1px solid rgba(249, 199, 16, 0.2);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.info-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #f9c710, #ffd700, #f9c710);
  border-radius: 24px 24px 0 0;
}


.shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 70%
  );
  transform: translateX(-100%) translateY(-100%) rotate(30deg);
  transition: transform 0.6s;
  pointer-events: none;
  opacity: 0;
}

.info-box:hover .shine {
  transform: translateX(100%) translateY(100%) rotate(30deg);
  opacity: 1;
}


.info-box:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 
    0 25px 60px rgba(0, 0, 0, 0.15),
    0 15px 35px rgba(249, 199, 16, 0.25);
  border-color: #f9c710;
}


.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f9c710, #e6b800);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 25px rgba(249, 199, 16, 0.4);
  transition: all 0.4s ease;
}

.info-box:hover .icon-wrapper {
  transform: scale(1.15) rotate(8deg);
  box-shadow: 0 15px 35px rgba(249, 199, 16, 0.5);
}

.icon-wrapper i {
  font-size: 2.2rem;
  color: #111;
}


.label {
  font-size: 1.05rem;
  color: #555;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.5px;
}

.value {
  font-size: 2.4rem;
  font-weight: 900;
  color: #1a1a1a;
  margin: 0.5rem 0 0;
  line-height: 1.2;
}

::v-deep(.extra) {
  font-size: 0.95rem;
  color: #10b981;
  font-weight: 600;
  margin-top: 0.5rem;
}

@media (max-width: 1024px) {
  .info-box {
    padding: 1.8rem 1.2rem;
    min-height: 160px;
  }
  .value {
    font-size: 2.1rem;
  }
}

@media (max-width: 768px) {
  .info-box {
    padding: 1.5rem 1rem;
    min-height: 140px;
  }
  .icon-wrapper {
    width: 70px;
    height: 70px;
  }
  .icon-wrapper i {
    font-size: 1.9rem;
  }
  .value {
    font-size: 1.9rem;
  }
}
</style>