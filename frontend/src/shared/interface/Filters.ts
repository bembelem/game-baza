import type { Ref } from "vue"
import type { ToArray } from "./Helpers"


export enum ResetBehavior {
	None = "none",
	ToDefault = "toDefault",
	Clear = "clear"
}

export interface MonoFilterDefinition<T> {
	values?: T[],
	defaultValue?: T,
	resetBehavior: ResetBehavior
}

export interface MultiFilterDefinition<T> {
	values?: T[],
	defaultValue?: T[],
	resetBehavior: ResetBehavior
}

export type FiltersDefinition<T> = {
	[K in keyof T]: 
		T[K] extends Array<unknown>
		? MultiFilterDefinition<T[K][number]>
		: MonoFilterDefinition<T[K]>
}

export type AvailableFiltersOptions<T> = {
	[K in keyof T]?: Ref<ToArray<T[K]> | null>
}

export type InjectedFiltersOptions<T> = {
	[K in keyof T]?: Ref<ToArray<T[K]>>
}


export interface SelectorValue<T> {
	title: string,
	value: T
}