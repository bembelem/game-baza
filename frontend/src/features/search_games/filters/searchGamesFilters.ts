import { type SelectorValue, type FiltersDefinition, ResetBehavior } from "@/shared/interface/Filters"
import { useFilters } from "@/shared/lib/useFilters"


export interface SearchGamesFilters {
 	sort: SelectorValue<string>,
	genres: SelectorValue<string>[],
	platforms: SelectorValue<string>[],
	developers: SelectorValue<string>[]
	publishers: SelectorValue<string>[],
	stores: SelectorValue<string>[],
	price: SelectorValue<[number, number | undefined] | undefined>
}

type SearchGamesFiltersDefinition = FiltersDefinition<SearchGamesFilters>


const sortValues = [
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

const priceValues: SelectorValue<[number, number | undefined] | undefined>[] = [
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

export const searchGamesFiltersDefinition: SearchGamesFiltersDefinition = {
	sort: {
		values: sortValues,
		defaultValue: sortValues[0],
		resetBehavior: ResetBehavior.ToDefault
	},
	genres: {
		resetBehavior: ResetBehavior.Clear
	},
	platforms: {
		resetBehavior: ResetBehavior.Clear 
	},
	developers: {
		resetBehavior: ResetBehavior.Clear
	},
	publishers: {
		resetBehavior: ResetBehavior.Clear
	},
	stores: {
		resetBehavior: ResetBehavior.Clear
	},
	price: {
		values: priceValues,
		defaultValue: priceValues[0],
		resetBehavior: ResetBehavior.ToDefault
	}
}

export const searchGamesFilters = useFilters<SearchGamesFilters>(searchGamesFiltersDefinition)