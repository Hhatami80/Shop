<template>
  <div
    @mousedown="onPress($event)"
    @mouseup="onRelease"
    @mouseleave="onRelease"
    ref="card"
    :style="{
      transform: cardTransform,
      background: cardBackground,
    }"
    :class="['card-container', { locked }]"
  >
    <!-- Locked status -->
    <template v-if="locked">
      <div class="locked-backdrop"></div>
      <Lock class="icon large locked-icon" />
    </template>

    <!-- Ripple effect -->
    <div
      class="ripple"
      v-for="ripple in ripples"
      :key="ripple.id"
      :style="{
        ...ripple.style,
        background: rippleBackgroundColor,
      }"
    ></div>

    <!-- $ effect -->
    <div class="dollar" v-for="dollar in dollars" :key="dollar.id" :style="dollar.style">
      $
    </div>

    <div class="card-content">
      <!-- Card wave -->
      <!-- <img alt="shape" src="~/assets/image/banks/CardWave.png" class="card-shape" /> -->

      <!-- Card header -->
      <div
        class="card-header"
        v-animate-on-scroll="{
          animation: 'fade-down',
          duration: 1,
          distance: 10,
          delay: 0.2,
          once: true,
        }"
      >
        <!-- bank provider -->
        <span class="card-provider" v-if="!hideProvider">{{
          bankInfo?.bank_title || "کیف پول "
        }}</span>
        <span class="card-provider" v-else> •••••• </span>

        <!-- Bank logo -->
        <img
          class="card-logo"
          :src="bankLogo || bankInfo?.bank_logo || defaultCardLogo"
        />
      </div>

      <!-- Card number -->
      <div
        class="card-body"
        v-animate-on-scroll="{
          animation: 'zoom-in',
          duration: 1,
          distance: 10,
          delay: 0.2,
          once: true,
        }"
      >
        <div class="card-number">
          <span v-if="!hideCard">{{ formatCardNumber(cardNumber) }}</span>
          <span class="mask" v-else> •••• •••• •••• •••• </span>
        </div>
        <div class="sheba_number">
          <span v-if="!hideSheba">{{ shebaNumber }}</span>
          <span class="mask" v-else>IR••••••••••••••••••••••••</span>
        </div>
      </div>

      <div
        class="card-footer"
        v-animate-on-scroll="{
          animation: 'fade-up',
          duration: 1,
          distance: 10,
          delay: 0.2,
          once: true,
        }"
      >
        <p class="card-amount" v-if="!hideAmount && amount">
          {{ rialToToman(Number(amount))?.toLocaleString() ?? 0 }} ریال
        </p>
        <p class="card-amount mask" v-else>•••••••••• ریال</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Lock } from "lucide-vue-next";
import { ref, computed } from "vue";
// import defaultCardLogo from "~/assets/image/logos/logo.png";
import { bankCards } from "@/data/bank-cards/bankCards";
import type { BankCard } from "@/data/bank-cards/bankCards";
import { formatCardNumber, rialToToman } from "@/utils/banking";

interface Ripple {
  id: string;
  style: {
    top: string;
    left: string;
  };
}

interface Dollar {
  id: string;
  style: {
    top: string;
    left: string;
  };
}

const props = defineProps<{
  cardNumber?: string;
  shebaNumber?: string;
  author?: string;
  bankLogo?: string;
  amount?: string;
  hideAmount?: boolean;
  hideCard?: boolean;
  hideSheba?: boolean;
  hideProvider?: boolean;
  locked?: boolean;
}>();

const getBankInfo = (cardNumber?: string): BankCard | null => {
  if (!cardNumber || typeof cardNumber !== "string") return null;
  const prefix = parseInt(cardNumber.slice(0, 6), 10);
  return bankCards.find((bank: BankCard) => bank.card_no === prefix) || null;
};

const bankInfo = computed<BankCard | null>(() => {
  if (props.cardNumber) {
    return getBankInfo(props.cardNumber);
  }
  return null;
});

const bankColor = computed(() => {
  return bankInfo.value?.color?.slice(0, 7) || "#191414";
});

const cardBackground = computed(() => {
  const base = bankColor.value;
  return `linear-gradient(
        45deg, 
        ${base}e6, 
        ${base}cc, 
        ${base}99, 
        ${base}66
    )`;
});

const rippleBackgroundColor = computed(() => {
  const c = bankColor.value || "rgba(25, 20, 20, 0.5)";
  if (c.startsWith("#")) {
    return `radial-gradient(
            circle, 
            ${c}cc 0%, 
            ${c}99 70%, 
            transparent 100%
        )`;
  } else {
    const baseRgb = c
      .replace(/rgba?\(([^)]+)\)/, "$1")
      .split(",")
      .slice(0, 3)
      .map((x) => x.trim())
      .join(",");
    return `radial-gradient(
            circle, 
            rgba(${baseRgb}, 0.8) 0%, 
            rgba(${baseRgb}, 0.6) 70%, 
            transparent 100%
        )`;
  }
});

const ripples = ref<Ripple[]>([]);
const dollars = ref<Dollar[]>([]);
const cardTransform = ref<string>("");
const pressed = ref<boolean>(false);

const getRelativePosition = (
  event: MouseEvent,
  offset: { x?: number; y?: number } = { x: 0, y: 0 }
) => {
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
  return {
    x: event.clientX - rect.left - (offset.x || 0),
    y: event.clientY - rect.top - (offset.y || 0),
  };
};

const createRipple = (event: MouseEvent) => {
  const { x, y } = getRelativePosition(event, { x: 50, y: 50 });
  const newRipple: Ripple = {
    id: `${Date.now()}-${Math.random()}`,
    style: {
      top: `${y}px`,
      left: `${x}px`,
    },
  };
  ripples.value.push(newRipple);
  if (ripples.value.length > 10) ripples.value.shift();
  setTimeout(() => {
    ripples.value = ripples.value.filter((r) => r.id !== newRipple.id);
  }, 500);
};

const createDollar = (event: MouseEvent) => {
  const { x, y } = getRelativePosition(event);
  const newDollar: Dollar = {
    id: `${Date.now()}-${Math.random()}`,
    style: {
      top: `${y}px`,
      left: `${x}px`,
    },
  };
  dollars.value.push(newDollar);
  if (dollars.value.length > 10) dollars.value.shift();
  setTimeout(() => {
    dollars.value = dollars.value.filter((d) => d.id !== newDollar.id);
  }, 800);
};

const onPress = (event: MouseEvent) => {
  if (props.locked) return;

  createDollar(event);
  createRipple(event);
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width - 0.5) * 3;
  const y = ((event.clientY - rect.top) / rect.height - 0.5) * -3;
  cardTransform.value = `perspective(500px) rotateX(${y}deg) rotateY(${x}deg) scale(0.99)`;
  pressed.value = true;
};

const onRelease = () => {
  cardTransform.value = "";
  pressed.value = false;
};
</script>

<style scoped>
.card-container {
  user-select: none;
  position: relative;
  border-radius: 10px;
  cursor: pointer;
  overflow: hidden;
  width: 360px;
  height: 190px;
  margin: auto;
  transition: 0.4s;
  will-change: transform;
  transform: var(--transform, none);
  background: none;
  box-shadow: rgba(0, 0, 0, 0.07) 0px 1px 2px, rgba(0, 0, 0, 0.07) 0px 2px 4px,
    rgba(0, 0, 0, 0.07) 0px 4px 8px, rgba(0, 0, 0, 0.07) 0px 8px 16px,
    rgba(0, 0, 0, 0.07) 0px 16px 32px, rgba(0, 0, 0, 0.07) 0px 32px 64px;
}

.card-container:active {
  transition: none;
}

.card-container.locked {
  pointer-events: none;
}

.locked-backdrop {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 3;
  background-color: #00000020;
  backdrop-filter: blur(5px);
}
.locked-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 4;
  filter: drop-shadow(0 0 3px rgba(0, 0, 0, 0.8));
  stroke: #bbbbbb;
}

.ripple {
  position: absolute;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  transform: scale(0);
  animation: ripple-effect 0.6s ease-out;
  pointer-events: none;
}

.dollar {
  position: absolute;
  font-size: 24px;
  font-weight: bold;
  color: rgba(190, 190, 190, 0.719);
  transform: scale(1);
  animation: dollar-effect 0.8s ease-out forwards;
  pointer-events: none;
  z-index: 2;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.card-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.9);
  padding: 10px 15px;
  box-sizing: border-box;
}

.card-header .card-provider {
  font-size: 16px;
  font-weight: bold;
  color: white;
}

.card-header .card-logo {
  width: 35px;
  height: 35px;
  filter: drop-shadow(0 0 3px rgba(0, 0, 0, 0.9));
}

.card-shape {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 8px;
  position: relative;
  padding: 10px 0;
  color: white;
}

.card-number,
.sheba_number {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  direction: ltr;
}

.sheba_number span {
  font-size: 15px;
  color: rgb(228, 228, 228);
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.9);
  font-family: system-ui, sans-serif !important;
}

.card-number span {
  font-size: 25px;
  font-weight: bold;
  direction: ltr;
  color: white;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.9);
  font-family: system-ui, sans-serif !important;
}

.card-number .mask,
.sheba_number .mask {
  letter-spacing: 2px;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 100%;
  position: absolute;
  height: 50px;
  bottom: 0;
  left: 0;
  padding: 0px 20px;
}

.card-amount {
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.9);
}

.card-amount .mask {
  letter-spacing: 2px;
}

@keyframes dollar-effect {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5) translateY(-20px);
    opacity: 0.7;
  }
  100% {
    transform: scale(2) translateY(-50px);
    opacity: 0;
  }
}

@keyframes ripple-effect {
  to {
    transform: scale(5);
    opacity: 0;
  }
}

@keyframes rotate-gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
