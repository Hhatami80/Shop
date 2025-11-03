<template>
  <div class="checkout-page">
    <h2 class="title">مرور سفارش</h2>

    <div v-if="cartItems && cartItems.length" class="checkout-container">
      <div class="cart-items">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.product.image" alt="product image" class="product-image" />
          <div class="item-details">
            <h3>{{ item.product.title }}</h3>
            <p>تعداد: {{ item.quantity }}</p>
            <p>
              قیمت واحد:
              {{ (item.product.final_price || item.product.price).toLocaleString() }}
              تومان
            </p>
            <p>
              قیمت کل:
              {{
                (
                  item.quantity * (item.product.final_price || item.product.price)
                ).toLocaleString()
              }}
              تومان
            </p>
          </div>
        </div>
      </div>

      <div class="cart-summary">
        <div class="total-section">
          <strong>مجموع سبد خرید:</strong> {{ total.toLocaleString() }} تومان
        </div>

        <div class="payment-method">
          <h3>انتخاب روش پرداخت</h3>
          <label>
            <input type="radio" value="online" v-model="paymentMethod" />
            پرداخت آنلاین
          </label>
          <label>
            <input type="radio" value="cod" v-model="paymentMethod" />
            پرداخت در محل
          </label>
          <label>
            <input type="radio" value="wallet" v-model="paymentMethod" />
            پرداخت با کیف پول
          </label>

          <p v-if="paymentMethod === 'wallet'" class="wallet-info">
            موجودی کیف پول شما: {{ wallet.balance.toLocaleString() }} تومان
          </p>

          <button class="btn gold-btn" @click="proceedToPayment" :disabled="loading">
            ادامه پرداخت
          </button>
        </div>
      </div>
    </div>

    <p v-else class="empty">سبد خرید شما خالی است.</p>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCartStore } from "@/stores/useCartStore";
import { useOrderStore } from "@/stores/useOrderStore";
import { useWalletStore } from "@/stores/useWalletStore";
import { toast } from "vue3-toastify";

const cartStore = useCartStore();
const orderStore = useOrderStore();
const wallet = useWalletStore();
const router = useRouter();

const cartItems = computed(() => cartStore.items || []);
const total = computed(() =>
  cartItems.value.reduce(
    (acc, i) => acc + i.quantity * (i.product.final_price || i.product.price),
    0
  )
);

const paymentMethod = ref("online");
const loading = ref(false);

onMounted(async () => {
  if (!cartItems.value.length) await cartStore.fetchCart();
  await wallet.fetchBalance();
});

const proceedToPayment = async () => {
  if (!cartItems.value.length) {
    toast.error("سبد خرید شما خالی است");
    return;
  }
  orderStore.paymentMethod = paymentMethod.value;
  loading.value = true;

  try {
    if (paymentMethod.value === "wallet") {
      if (total.value > wallet.balance) {
        toast.error("موجودی کیف پول کافی نیست ");
        return;
      }
      const payload = {
        payment_method: "wallet",
        items: cartItems.value.map((i) => ({
          product_id: i.product.id,
          quantity: i.quantity,
        })),
      };

      const res = await orderStore.submitOrder(payload);
      if (res?.orderId) {
        toast.success("پرداخت با کیف پول با موفقیت انجام شد ");
        await wallet.fetchBalance();
        router.push("user/orders");
      }
    } else if (paymentMethod.value === "online") {
      router.push({ name: "payment-gateway" });
    } else {
      router.push({ name: "payment", query: { method: "cod" } });
    }
  } catch (err) {
    console.error(err);
    toast.error("خطا در ثبت سفارش");
  } finally {
    loading.value = false;
  }
};
</script>
<style scoped>
.checkout-page {
  max-width: 100vw;
  margin: 50px auto;
  padding: 30px 25px;
  font-family: "Yekan", sans-serif;
  background: #f6f7f9;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}
.wallet-info {
  font-size: 0.95rem;
  color: #555;
  margin-top: 5px;
  font-weight: 500;
}
.title {
  direction: rtl;
}
f h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 35px;
  border-right: 8px solid #f8b900;
  padding-right: 14px;
}

.checkout-container {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  flex-direction: row-reverse;
}

.cart-items {
  direction: rtl;
  flex: 2.5;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #fff;
  padding: 15px 20px;
  border-radius: 16px;
  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.cart-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.product-image {
  width: 120px;
  height: 120px;
  object-fit: contain;
  border-radius: 12px;
  border: 1px solid #eee;
  background: #fafafa;
  flex-shrink: 0;
}

.item-details {
  flex: 1;
  font-family: "Yekan", sans-serif;

  display: flex;
  flex-direction: column;
  gap: 6px;
}

.item-details h3 {
  margin: 0;
  font-size: 1.15rem;
  color: #222;
}

.item-details p {
  margin: 0;
  font-size: 1rem;
  color: #555;
}

.cart-summary {
  flex: 1;
  background: #fffbe6;
  border-radius: 16px;
  padding: 25px 20px;
  position: sticky;
  top: 20px;
  height: fit-content;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.total-section {
  text-align: right;
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 15px;
}

.payment-method {
  font-family: "Yekan";
  direction: rtl;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.payment-method h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.payment-method label {
  display: flex;
  font-family: "Yekan";

  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

.btn.gold-btn {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  border: none;
  border-radius: 14px;
  padding: 12px 28px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 15px;
  transition: all 0.3s;
}

.btn.gold-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(248, 185, 0, 0.5);
}

.empty {
  text-align: center;
  padding: 80px 20px;
  font-size: 1.3rem;
  color: #777;
  background: #fff;
  border-radius: 16px;
  border: 2px dashed #f8b900;
}

@media (max-width: 900px) {
  .checkout-container {
    flex-direction: column-reverse;
  }

  .cart-summary {
    position: static;
    top: auto;
  }

  .cart-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .product-image {
    width: 140px;
    height: 140px;
  }

  .item-details {
    gap: 8px;
  }
}
</style>
