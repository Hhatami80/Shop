<template>
  <div class="game-section">
    
    <div class="game-header">
      <h2>بازی ها</h2>
      <p>پانتومیم</p>
    </div>

    
    <div class="cards-container">
        <div class="card upload-card">
        <div class="upload-box">
          <span class="plus">+</span>
          <p>بارگذاری تصویر</p>
        </div>
      </div>
      
      <div class="card">
        <p>کلمات کلیدی: جشن و پایکوبی و ......</p>
        <p>داستان: .....</p>
      </div>

     
      
    </div>
  </div>
</template>

<style scoped>
.game-section {
  background: #111; 
  color: #fff;
  padding: 40px;
  text-align: center;
  direction: rtl;
}

.game-header h2 {
  margin: 0;
  font-size: 20px;
}

.game-header p {
  margin: 5px 0 20px;
  font-size: 16px;
}

.cards-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 60px; 
  flex-wrap: wrap;
}

.card {
  background: #fff;
  color: #000;
  width: 300px;
  height: 250px;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.upload-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.plus {
  font-size: 40px;
  line-height: 1;
  margin-bottom: 10px;
}
</style>
