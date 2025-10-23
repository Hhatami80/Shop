مراحل نصب و اجرا
1.     کلون کردن پروژه:
git clone https://github.com/username/frontend-project.git
cd frontend-project
 
2.     نصب وابستگی‌ها:
npm install
 
3.     اجرای پروژه در حالت توسعه
npm run dev
 
4.     ساخت نسخه‌ی نهایی (Production):
npm run build
 
5.     اتصال به بک‌اند
برای اتصال به بک‌اند DRF باید آدرس API در فایل تنظیمات فرانت‌اند مثلا ( (.envمشخص شود.
نمونه .env
VITE_API_URL=http://127.0.0.1:8000/api
و در کد Vue مثلا با Axios
import axios from 'axios';
 
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});
 
export default api;
 
6.     ساخت نهایی:
npm run build
