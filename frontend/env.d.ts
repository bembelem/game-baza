/// <reference types="vite/client" />

declare module '*.svg?component' {
  	import { Component } from 'vue'
  	const component: Component
  	export default component
}
