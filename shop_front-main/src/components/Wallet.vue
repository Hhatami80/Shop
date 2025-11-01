<template>
  <div class="wallet-page">
    <div class="wallet-top-row">
      <div class="wallet-card-wrapper" v-if="bank">
        <BankCard
          :card-number="bank.cardNumber"
          :sheba-number="bank.shebaNumber"
          :amount="wallet.balance"
          :bank-logo="bank.bankLogo"
        />
      </div>

      <div class="wallet-actions">
        <h3>مدیریت کیف پول</h3>
        <div class="action-row">
          <input v-model.number="amount" type="number" placeholder="مبلغ (تومان)" />
          <select v-model="method">
            <option value="card">شارژ با کارت</option>
            <option value="iban">شارژ با شبا</option>
          </select>
          <button class="btn-charge" @click="goToPayment">
            <fa-icon :icon="['fas', 'plus-circle']" /> شارژ
          </button>
          <button class="btn-withdraw" @click="withdraw">
            <fa-icon :icon="['fas', 'minus-circle']" /> برداشت
          </button>
        </div>
      </div>
    </div>

    <div class="wallet-transactions">
      <h3>تراکنش‌ها</h3>

      <table v-if="wallet.transactions.length" class="transactions-table">
        <thead>
          <tr>
            <th>تاریخ</th>
            <th>نوع</th>
            <th>مبلغ</th>
            <th>روش</th>
            <th>توضیحات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in wallet.transactions" :key="tx.id">
            <td>{{ formatDate(tx.date) }}</td>
            <td :class="tx.type">{{ tx.type === "credit" ? "واریز" : "برداشت" }}</td>
            <td>{{ formatPrice(tx.amount) }} تومان</td>
            <td>{{ tx.method === "card" ? "کارت" : "شبا" }}</td>
            <td>{{ tx.description }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else class="empty-state">
        <fa-icon :icon="['fas', 'receipt']" />
        <p>تاکنون تراکنشی ثبت نشده است.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useWalletStore } from "@/stores/useWalletStore";
import { useUserStore } from "@/stores/useUserStore";
import { toast } from "vue3-toastify";
import { useRouter } from "vue-router";
import BankCard from "@/components/BankCard.vue";

const wallet = useWalletStore();
const userStore = useUserStore();
const router = useRouter();

const amount = ref(0);
const method = ref("card");

const bank = computed(() =>
  userStore.bankAccounts.length > 0 ? userStore.bankAccounts[0] : null
);

onMounted(async () => {
  await Promise.all([
    wallet.fetchBalance(),
    wallet.fetchTransactions(),
    userStore.fetchBankAccounts(),
  ]);
});

const goToPayment = async () => {
  if (amount.value <= 0) return toast.error("مبلغ وارد شده صحیح نیست");
  wallet.pendingAmount = amount.value;
  router.push({ name: "WalletPayment" });
};

const withdraw = async () => {
  if (amount.value <= 0) return toast.error("مبلغ وارد شده صحیح نیست");
  await wallet.withdraw({ amount: amount.value, method: method.value });
  amount.value = 0;
};

const formatDate = (dateStr) => {
  if (!dateStr) return "";
  return new Intl.DateTimeFormat("fa-IR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(dateStr));
};

const formatPrice = (amount) => Number(amount)?.toLocaleString("fa-IR") || "0";
</script>

<style scoped>
.wallet-page {
  max-width: 1300px;
  margin: 60px auto;
  padding: 48px;
  display: flex;
  flex-direction: column;
  gap: 60px;
  font-family: "Vazirmatn", sans-serif;
  background: linear-gradient(165deg, #f6f7fc, #e6ebf5);
  border-radius: 32px;
  box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.25);
}

.wallet-top-row {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 40px;
  flex-wrap: nowrap;
}

.wallet-card-wrapper {
  flex: 0 0 36%;
  max-width: 420px;
  display: flex;
  align-items: stretch;
}

.wallet-card-wrapper > * {
  width: 400px;
  height: 100%;
  border-radius: 20px;
  background: linear-gradient(145deg, #ffffff, #e8ecf4);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.wallet-actions {
  flex: 1;
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(15px);
  padding: 36px;
  border-radius: 24px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.07);
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.3s ease;
}

.wallet-actions h3 {
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: 28px;
  color: #222;
  border-bottom: 3px solid #f9c710;
  display: inline-block;
  padding-bottom: 8px;
}

.action-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: center;
}

.action-row input,
.action-row select {
  flex: 1 1 160px;
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid #dcdfe3;
  font-size: 1rem;
  background: #fafafa;
  outline: none;
}

.action-row button {
  border: none;
  border-radius: 14px;
  padding: 12px 22px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.btn-charge {
  background: linear-gradient(135deg, #ffe670, #f9c710);
  color: #1a1a1a;
}

.btn-withdraw {
  background: linear-gradient(135deg, #ff5c5c, #dc3545);
  color: #fff;
}

.wallet-transactions {
  background: rgba(255, 255, 255, 0.97);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.07);
}

.wallet-transactions h3 {
  font-size: 1.75rem;
  margin-bottom: 24px;
  border-bottom: 3px solid #f9c710;
  display: inline-block;
  padding-bottom: 8px;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.transactions-table th {
  background: #ffd700;
  color: #222;
  font-weight: 700;
  text-align: center;
  padding: 14px;
  font-size: 1rem;
}

.transactions-table td {
  text-align: center;
  padding: 12px;
  font-size: 0.95rem;
  border-bottom: 1px solid #eee;
  transition: background 0.2s;
}

.transactions-table tbody tr:hover {
  background: #fffde7;
}

.transactions-table td.credit {
  color: #28a745;
  font-weight: bold;
}

.transactions-table td.debit {
  color: #dc3545;
  font-weight: bold;
}

.empty-state {
  padding: 80px 0;
  text-align: center;
}

.empty-state .fa-icon {
  font-size: 3.5rem;
}

@media (max-width: 1000px) {
  .wallet-top-row {
    flex-direction: column;
  }
  .wallet-card-wrapper,
  .wallet-actions {
    flex: 1 1 100%;
    max-width: 100%;
  }
}
</style>
