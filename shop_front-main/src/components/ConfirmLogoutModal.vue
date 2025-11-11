<template>
  <div class="modal-overlay">
    <div class="modal">
      <h3>آیا مطمئن هستید که می‌خواهید خارج شوید؟</h3>
      <div class="actions">
        <button @click="$emit('confirm')" class="confirm">بله</button>
        <button @click="$emit('cancel')" class="cancel">خیر</button>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal {
  background: #fff;
  padding: 25px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  text-align: center;
  min-width: 300px;
  font-family: 'IRANSansX', sans-serif;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.confirm {
  background-color: #d9534f;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.cancel {
  background-color: #ccc;
  color: black;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.confirm:hover {
  background-color: #c9302c;
}
.cancel:hover {
  background-color: #b3b3b3;
}
</style>
