import "./assets/main.css";

import WebFont from "webfontloader";
import { createApp } from "vue";
import App from "./App.vue";

createApp(App).mount("#app");

WebFont.load({
    google: {
        families: ["Inter:700,900", "Noto Sans SC:700,900"],
    },
});
