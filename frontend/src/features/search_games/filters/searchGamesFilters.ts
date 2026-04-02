import type { SelectorValue } from "@/shared/interface/Filters"
import { reactive } from "vue"


export interface GamesSelectedFiltersState {
	sort: SelectorValue<string>,
	price: SelectorValue<[number, number] | undefined>
	genres?: SelectorValue<string>[]
	stores?: SelectorValue<string>[]
}


export const searchGamesFilters = reactive<GamesSelectedFiltersState>({
	sort: {
		title: "по популярности", 
		value: "popularity"
	},
	price: {
		title: "все цены",
		value: undefined
	}
})

export const sortValues = [
	{
		title: "по популярности", 
		value: "popularity"
	},
	{
		title: "по рейтингу", 
		value: "rating"
	},
	{
		title: "сначала дешевые", 
		value: "cheap"
	},
	{
		title: "сначала дорогие", 
		value: "expensive"
	},
	{
		title: "по скидке", 
		value: "sale"
	},
	{
		title: "по дате выхода", 
		value: "release_date"
	},
	{
		title: "по дате добавления", 
		value: "addition_date"
	},
	{
		title: "по алфавиту", 
		value: "alphabet"
	}
]

export const priceValues: SelectorValue<[number, number] | undefined>[] = [
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
		value: [6000, 0]
	}
] 