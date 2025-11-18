<template>
  <div class="wallet-page">
    <div v-if="!bank" class="bank-warning">
       برای استفاده از کیف پول، لطفاً حساب بانکی خود را در بخش حساب بانکی وارد کنید.
      <button class="go-bank-btn" @click="goToBankSection">رفتن به حساب بانکی</button>
    </div>

    <div class="wallet-top-row">
      <div class="wallet-card-wrapper" v-if="bank">
        <BankCard
          :card-number="bank.cardNumber"
          :sheba-number="bank.iban"
          :amount="wallet.balance"
          :bank-logo="bank.bankLogo"
        />
      </div>

      <div class="wallet-actions">
        <h3>مدیریت کیف پول</h3>
        <div class="action-row">
          <input v-model.number="amount" type="number" placeholder="مبلغ (تومان)" />
          <button class="btn-charge" @click="goToPayment">
            <fa-icon :icon="['fas', 'plus-circle']" /> شارژ
          </button>
          <!-- <button class="btn-withdraw" @click="withdraw">
            <fa-icon :icon="['fas', 'minus-circle']" /> برداشت
          </button> -->
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
          <tr v-for="tx in paginatedTransactions" :key="tx.id">
            <td>{{ formatDate(tx.date) }}</td>
            <td :class="tx.type">{{ tx.type === 'credit' ? 'واریز' : 'برداشت' }}</td>
            <td>{{ formatPrice(tx.amount) }} تومان</td>
            <td>{{ tx.method === 'card' ? 'کارت' : 'شبا' }}</td>
            <td>{{ tx.description }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else class="empty-state">
        <fa-icon :icon="['fas', 'receipt']" />
        <p>تاکنون تراکنشی ثبت نشده است.</p>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">
          <fa-icon :icon="['fas', 'chevron-left']" />
        </button>
        <span>صفحه {{ currentPage }} از {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">
          <fa-icon :icon="['fas', 'chevron-right']" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useWalletStore } from '@/stores/useWalletStore'
import { useUserStore } from '@/stores/useUserStore'
import { toast } from 'vue3-toastify'
import { useRouter } from 'vue-router'
import BankCard from '@/components/BankCard.vue'

const wallet = useWalletStore()
const userStore = useUserStore()
const router = useRouter()

const amount = ref()

const bank = computed(() => (userStore.bankAccounts.length > 0 ? userStore.bankAccounts[0] : null))
const showBankMessage = computed(() => !bank.value)

onMounted(async () => {
  await Promise.all([
    wallet.fetchBalance(),
    wallet.fetchTransactions(),
    userStore.fetchBankAccounts(),
  ])
})

const currentPage = ref(1)
const pageSize = ref(5)
const totalPages = computed(() => Math.ceil(wallet.transactions.length / pageSize.value))

const paginatedTransactions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return wallet.transactions.slice(start, start + pageSize.value)
})

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const goToPayment = async () => {
  if (amount.value < 100) return toast.error('حداقل مبلغ قابل شارژ 100 تومان میباشد.')
  wallet.pendingAmount = amount.value
  router.push({ name: 'WalletPayment' })
}

const withdraw = async () => {
  if (!bank.value) return toast.error('برای برداشت وجه ابتدا حساب بانکی ثبت کنید.')
  if (amount.value <= 0) return toast.error('مبلغ وارد شده صحیح نیست')
  await wallet.withdraw({ amount: amount.value, method: 'card' })
  amount.value = 0
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(dateStr))
}
const formatPrice = (amount) => Number(amount)?.toLocaleString('fa-IR') || '0'
const goToBankSection = () => {
  router.push('/user/profile/bank')
}
</script>

<style scoped>
.wallet-page {
  max-width: 1300px;
  margin: 60px auto;
  padding: 48px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  background: linear-gradient(165deg, #f6f7fc, #e6ebf5);
  border-radius: 32px;
  box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.25);
  
}


.bank-warning {
  background: #fff4e5;
  border: 1px solid #ffd699;
  color: #8b5e3c;
  padding: 16px 20px;
  border-radius: 14px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  
  font-weight: 500;
  font-size: 0.95rem;
  animation: fadeSlide 0.4s ease;
}

.go-bank-btn {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 10px 18px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}
.go-bank-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
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
  transition: transform 0.3s ease;
}
.wallet-card-wrapper > * {
  width: 100%;
  height: 100%;
  border-radius: 20px;
  background: linear-gradient(145deg, #ffffff, #e8ecf4);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.wallet-card-wrapper:hover > * {
  transform: translateY(-5px);
  box-shadow: 0 18px 35px rgba(0, 0, 0, 0.12);
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
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 28px;
  color: #222;
  border-bottom: 3px solid #f9c710;
  display: inline-block;
  padding-bottom: 8px;
}

.action-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.action-row input {
  flex: 0 0 140px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid #dcdfe3;
  font-size: 0.95rem;
  background: #fafafa;
  outline: none;
  transition: border 0.2s, box-shadow 0.2s;
}
.action-row input:focus {
  border-color: #f9c710;
  box-shadow: 0 0 6px rgba(249, 199, 16, 0.4);
}


.action-row button {
  flex: 0 0 auto;
  padding: 10px 18px;
  font-size: 0.95rem;
  border-radius: 12px;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.25s ease;
}

.btn-charge {
  background: linear-gradient(135deg, #ffe670, #f9c710);
  color: #1a1a1a;
}
.btn-charge:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(249, 199, 16, 0.4);
}

.btn-withdraw {
  background: linear-gradient(135deg, #ff5c5c, #dc3545);
  color: #fff;
}
.btn-withdraw:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(220, 53, 69, 0.35);
}


.wallet-transactions {
  background: rgba(255, 255, 255, 0.97);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.07);
  transition: all 0.3s ease;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 14px;
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
  transform: scale(1.01);
  transition: all 0.2s;
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
  animation: fadeScaleIn 0.4s ease;
}
.empty-state .fa-icon {
  font-size: 3.5rem;
  color: #f9c710;
  animation: bounce 1.2s infinite;
}
.empty-state p {
  font-size: 1.1rem;
  margin-top: 14px;
  color: #555;
}


.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}
.pagination button {
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  background: #ffd700;
  color: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.pagination button:hover {
  background: #e5c100;
}
.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.pagination span {
  font-weight: bold;
}


@keyframes fadeScaleIn {
  0% {
    opacity: 0;
    transform: scale(0.75);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes fadeSlide {
  0% { opacity: 0; transform: translateY(-10px); }
  100% { opacity: 1; transform: translateY(0); }
}


@media (max-width: 1000px) {
  .wallet-top-row {
    flex-direction: column;
    gap: 30px;
  }
  .wallet-card-wrapper,
  .wallet-actions {
    flex: 1 1 100%;
    max-width: 100%;
  }
}

</style>
