import { createApp } from "vue";
import { createPinia } from "pinia";
import VueSmoothScroll from "vue3-smooth-scroll";
import "./style.css";
import router from "./routes";
import App from "./App.vue";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import HeaderComponent from "./components/HeaderComponent.vue";
import FooterComponent from "./components/FooterComponent.vue";
import SwiperClass, { Pagination } from "swiper";
import VueAwesomeSwiper from "vue-awesome-swiper";
import "swiper/css";
import "swiper/css/pagination";
import "aos/dist/aos.css";

SwiperClass.use([Pagination]);

const app = createApp(App);

const toastOptions = {
  transition: "Vue-Toastification__fade",
  maxToasts: 5,
  newestOnTop: true,
  position: "top-right",
  timeout: 4000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false,
  toastClassName: "custom-theme-toast",
  bodyClassName: "custom-theme-toast-body",
};

app.use(router);
app.use(createPinia());
app.use(VueSmoothScroll);
app.use(VueAwesomeSwiper);
app.use(Toast, toastOptions);

app.component("header-component", HeaderComponent);
app.component("footer-component", FooterComponent);

app.mount("#app");