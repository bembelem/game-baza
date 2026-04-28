import type { SelectorValue } from "../interface/Filters"


export const priceValues: SelectorValue<[number, number | undefined] | undefined>[] = [
	{
		title: "все цены",
		value: undefined
	},
	{
		title: "до 1000₽", 
		value: [0, 1000]
	},
	{
		title: "1000-3000₽", 
		value: [1000, 3000]
	},
	{
		title: "3000-6000₽", 
		value: [3000, 6000]
	},
	{
		title: "от 6000₽", 
		value: [6000, undefined]
	}
] 