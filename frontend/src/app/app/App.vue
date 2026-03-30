<script setup lang="ts">
import AppHeader from "@/widgets/header/ui/AppHeader.vue"
import { RouterView } from "vue-router"
import "../styles/fonts.css"
import "../styles/main.css"
import "../styles/reset.css"
</script>

<template>
	<AppHeader/>
	<RouterView/>
</template>