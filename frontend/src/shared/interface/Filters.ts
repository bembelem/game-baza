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


export interface SelectorValue<T> {
	title: string,
	value: T
}