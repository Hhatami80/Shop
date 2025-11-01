<template>
  <div class="bank-section">
    <h3>حساب‌های بانکی من</h3>

    <div class="bank-inputs">
      <div class="input-card">
        <label>شماره کارت</label>
        <input
          type="text"
          v-model="newBank.cardNumber"
          maxlength="19"
          placeholder="6037 9912 3456 7890"
          @input="onCardInput"
        />
        <div class="bank-detect">
          <img :src="detectedBank.bank_logo || '/logos/default.png'" class="bank-logo" />
          <span>{{ detectedBank.bank_title || "---" }}</span>
        </div>
      </div>

      <div class="input-card">
        <label>شماره حساب</label>
        <input type="text" v-model="newBank.accountNumber" placeholder="123456789012" />
      </div>

      <div class="input-card">
        <label>شماره شبا</label>
        <input
          type="text"
          v-model="newBank.iban"
          placeholder="IR820540102680020817909002"
        />
      </div>
    </div>

    <div class="add-btn-container">
      <button class="btn gold-btn" @click="handleAddBank">➕ افزودن حساب</button>
    </div>

    <table class="bank-table" v-if="store.bankAccounts.length">
      <thead>
        <tr>
          <th>لوگو</th>
          <th>نام بانک</th>
          <th>شماره کارت</th>
          <th>شماره حساب</th>
          <th>شماره شبا</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(account, idx) in store.bankAccounts" :key="account.id">
          <td>
            <img :src="account.bankLogo || '/logos/default.png'" class="bank-logo" />
          </td>
          <td>{{ account.bankName || "نامشخص" }}</td>
          <td>{{ maskCard(account.cardNumber) }}</td>
          <td>{{ account.accountNumber }}</td>
          <td>{{ account.iban }}</td>
          <td>
            <button class="delete-btn" @click="handleDeleteBank(idx)">🗑 حذف</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="empty-message">هنوز حسابی ثبت نکرده‌اید.</p>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import {
  getBankFromCard,
  validateBankCardNumber,
  validateIranianIBAN,
  validateAccountNumber,
} from "@/data/regex/validators";

const store = useUserStore();

const newBank = reactive({
  cardNumber: "",
  accountNumber: "",
  iban: "",
});

const detectedBank = computed(() => {
  const cardClean = newBank.cardNumber.replace(/\s+/g, "");
  return getBankFromCard(cardClean) || {};
});

onMounted(async () => {
  await store.fetchProfile();
  await store.fetchBankAccounts();
});

function maskCard(cardNumber) {
  if (!cardNumber) return "";
  return "**** **** **** " + cardNumber.slice(-4);
}

function onCardInput(e) {
  let digits = e.target.value.replace(/\D/g, "").slice(0, 16);
  newBank.cardNumber = digits.replace(/(.{4})/g, "$1 ").trim();
}

const handleAddBank = async () => {
  const card = newBank.cardNumber.replace(/\s+/g, "");
  const accountNum = newBank.accountNumber.trim();
  const iban = newBank.iban.trim();

  if (!card || !accountNum || !iban) return toast.error("لطفاً همه فیلدها را پر کنید");

  if (!validateBankCardNumber(card)) return toast.error("شماره کارت معتبر نیست");
  if (!validateAccountNumber(accountNum))
    return toast.error("شماره حساب معتبر نیست (حداکثر 12 رقم)");
  let ibanIsValid = validateIranianIBAN(iban);
  if (!ibanIsValid) return toast.error("شماره شبا معتبر نیست");

  const bankInfo = {
    cardNumber: card,
    accountNumber: accountNum,
    iban,
  };

  try {
    const added = await store.addBankAccount(bankInfo);
    added.bankName = detectedBank.value.bank_title || "نامشخص";
    added.bankLogo = detectedBank.value.bank_logo || "/logos/default.png";

    newBank.cardNumber = "";
    newBank.accountNumber = "";
    newBank.iban = "";
  } catch (err) {
    console.error(err.response?.data || err);
    toast.error("خطا در افزودن حساب بانکی");
  }
};

const handleDeleteBank = async (index) => {
  await store.deleteBankAccount(index);
};
</script>

<style scoped>
.bank-section {
  max-width: 950px;
  margin: 0 auto;
  padding: 30px;
  background: #fffef9;
  border-radius: 16px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.06);
}
h3 {
  margin-bottom: 25px;
  font-size: 1.3rem;
  color: #333;
  border-right: 5px solid #f8b900;
  padding-right: 12px;
}
.bank-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
  outline: none;
}
.input-card {
  background: #fff;
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 0 3px 10px rgba(248, 185, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
}
input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 0.92rem;
  outline: none;
}
.bank-detect {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 5px;
}
.bank-logo {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: contain;
  background: #fff8dc;
  padding: 4px;
}
.add-btn-container {
  text-align: center;
  margin-bottom: 35px;
}
.btn.gold-btn {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  border-radius: 12px;
  padding: 12px 26px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.bank-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.bank-table th {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  padding: 12px;
  font-weight: 600;
}
.bank-table td {
  padding: 14px;
  border-bottom: 1px solid #f3f3f3;
}
.delete-btn {
  background: #fff1f1;
  border: none;
  padding: 6px 12px;
  color: #d33;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.empty-message {
  text-align: center;
  padding: 25px;
  color: #888;
}
</style>
