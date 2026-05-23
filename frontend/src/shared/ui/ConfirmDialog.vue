<script lang="ts" setup>
import SubmitButton from "./SubmitButton.vue"

const props = withDefaults(defineProps<{
	title: string
	message: string
	isConfirming?: boolean
	confirmLabel?: string
	cancelLabel?: string
}>(), {
	confirmLabel: "Подтвердить",
	cancelLabel: "Отмена"
})

const emit = defineEmits<{
	confirm: []
	cancel: []
}>()
</script>

<template>
	<div class="overlay">
		<div class="dialog">
			<p class="title">{{ props.title }}</p>
			<p class="message">{{ props.message }}</p>

			<div class="footer">
				<button
				class="decision_button decision_button--cancel"
				type="button"
				@click="emit('cancel')">
					{{ props.cancelLabel }}
				</button>

				<SubmitButton
				:label="props.confirmLabel"
				type="button"
				:is-submitting="props.isConfirming"
				@click="emit('confirm')"/>
			</div>
		</div>
	</div>
</template>

<style scoped>
.overlay {
	position: fixed;
	inset: 0;
	background-color: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 100;
}

.dialog {
	background-color: var(--c_bg__surface);
	border: var(--border__md) solid var(--c_border__default);
	padding: var(--space__lg);
	display: flex;
	flex-direction: column;
	gap: var(--space__sm);
	width: 50%;
}

.title {
	font-size: var(--fs__lg);
}

.message {
	font-size: var(--fs__xs);
	color: var(--c_text__muted);
}

.footer {
	display: flex;
	gap: var(--space__sm);
}

.decision_button {
	padding: var(--space__xs);
	width: 100%;
	background-color: transparent;
}

.decision_button--cancel {
	border: var(--border__md) solid var(--c_border__default);
	color: var(--c_text__primary);
}

@media (max-width: 1024px) {
	.dialog {
		width: 75%;
	}
}
@media (max-width: 600px) {
	.dialog {
		width: 100%;
		margin: 0 var(--p_layout);
	}
}
</style>