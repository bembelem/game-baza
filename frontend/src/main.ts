import App from "@/app/app/App.vue"
import { createApp } from "vue"
import { router } from "./app/router/router"
import "./app/styles/reset.css"
import "./app/styles/fonts.css"
import "./app/styles/tokens.css"
import "./app/styles/global.css"


const app = createApp(App)

app.use(router)

app.mount('#app')