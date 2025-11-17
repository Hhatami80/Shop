<template>
  <div class="info-box" :style="{ backgroundColor: bgColor, color: textColor }">
    <div class="icon" :style="{ color: iconColor }">
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
  name: "InfoBox",
  props: {
    label: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number],
      required: true,
    },
    iconClass: {
      type: String,
      default: "fas fa-info-circle",
    },
    bgColor: {
      type: String,
      default: "#ffffff", 
    },
    textColor: {
      type: String,
      default: "#333333", 
    },
    iconColor: {
      type: String,
      default: "#3498db", 
    },
  },
};
</script>

<style>
.info-box {
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.info-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.icon {
  font-size: 36px;
  margin-right: 15px;
}

.content .label {
  font-size: 14px;
  font-weight: 500;
  opacity: 0.7;
}

.content .value {
  font-size: 20px;
  font-weight: bold;
  margin-top: 3px;
}
</style>
