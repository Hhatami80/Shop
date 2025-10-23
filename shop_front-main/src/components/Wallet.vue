<template>
  <div class="wallet-page">
    <!-- کارت بانکی -->
    <div class="wallet-card-wrapper">
      <BankCard
        :card-number="wallet.cardNumber"
        :sheba-number="wallet.shebaNumber"
        :amount="wallet.balance"
        :bank-logo="wallet.bankLogo"
      />
    </div>

    <!-- بخش عملیات -->
    <div class="wallet-actions">
      <h3>مدیریت کیف پول</h3>

      <div class="action-row">
        <input v-model.number="amount" type="number" placeholder="مبلغ (تومان)" />
        <select v-model="method">
          <option value="card">شارژ با کارت</option>
          <option value="iban">شارژ با شبا</option>
        </select>
        <button class="btn-charge" @click="addCredit">
          <fa-icon :icon="['fas', 'plus-circle']" /> شارژ
        </button>
        <button class="btn-withdraw" @click="withdraw">
          <fa-icon :icon="['fas', 'minus-circle']" /> برداشت
        </button>
      </div>
    </div>

    <!-- جدول تراکنش‌ها -->
    <div class="wallet-transactions">
      <h3>تراکنش‌ها</h3>

      <table v-if="wallet.transactions.length">
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
            <td>{{ tx.date }}</td>
            <td :class="tx.type">{{ tx.type === "credit" ? "واریز" : "برداشت" }}</td>
            <td>{{ tx.amount.toLocaleString() }} تومان</td>
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
import { ref, onMounted } from "vue";
import { useWalletStore } from "@/stores/useWalletStore";
import { toast } from "vue3-toastify";
import BankCard from "@/components/BankCard.vue";

const wallet = useWalletStore();
const amount = ref(0);
const method = ref("card");

onMounted(async () => {
  await wallet.fetchBalance();
  await wallet.fetchTransactions();
});

const addCredit = async () => {
  if (amount.value <= 0) return toast.error("مبلغ وارد شده صحیح نیست");
  await wallet.addCredit({ amount: amount.value, method: method.value });
  amount.value = 0;
};

const withdraw = async () => {
  if (amount.value <= 0) return toast.error("مبلغ وارد شده صحیح نیست");
  await wallet.withdraw({ amount: amount.value, method: method.value });
  amount.value = 0;
};
</script>

<style scoped>
.wallet-page {
  max-width: 1000px;
  margin: 50px auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  font-family: "Vazirmatn", sans-serif;
}

.wallet-card-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.wallet-actions {
  background: #fff;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.wallet-actions h3 {
  margin-bottom: 15px;
  color: #333;
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.action-row input,
.action-row select {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
  flex: 1;
  min-width: 150px;
}

.action-row button {
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-charge {
  background: #f9c710;
  color: #1a1a1a;
}

.btn-charge:hover {
  background: #e0b400;
}

.btn-withdraw {
  background: #dc3545;
  color: #fff;
}

.btn-withdraw:hover {
  background: #c82333;
}

.wallet-transactions {
  background: #fff;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.wallet-transactions h3 {
  margin-bottom: 15px;
  color: #333;
}

.wallet-transactions table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 12px;
  overflow: hidden;
}

.wallet-transactions th,
.wallet-transactions td {
  text-align: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.wallet-transactions th {
  background: #f9c710;
  color: #1a1a1a;
  font-weight: 600;
}

.wallet-transactions tr:hover {
  background: #fffbea;
}

.wallet-transactions td.credit {
  color: green;
  font-weight: bold;
}

.wallet-transactions td.debit {
  color: red;
  font-weight: bold;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #777;
}

.empty-state .fa-icon {
  font-size: 2rem;
  color: #f9c710;
  margin-bottom: 10px;
}
</style>
