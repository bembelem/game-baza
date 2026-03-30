import App from "@/app/app/App.vue"
import { createApp } from "vue"
import { router } from "./app/router/router"

const app = createApp(App)

app.use(router)

app.mount('#app')