import type { 
	FiltersDefinition, 
	AvailableFiltersOptions, 
	InjectedFiltersOptions 
} from "../interface/Filters"
import type { ToArray } from "../interface/Helpers"
import { reactive } from "vue"
import equal from "fast-deep-equal"


export function useFiltersOptions<T>(
	filtersDefinition: FiltersDefinition<T>,
	availableFiltersOptions?: AvailableFiltersOptions<T>,
) {
	const injectedFiltersOptions = reactive({}) as InjectedFiltersOptions<T>

	function getFilterOptions<K extends keyof T>(name: K) {
		if (filtersDefinition[name].values) {
			return filtersDefinition[name].values as ToArray<T[K]>
		}
	
		const availableOptions = availableFiltersOptions?.[name]?.value ?? []
		const injectedOptions = injectedFiltersOptions[name] ?? []
	
		const combined = [...availableOptions, ...injectedOptions]
	
		return combined.filter((item, index) => 
			[...availableOptions, ...injectedOptions].findIndex((i) => equal(i, item)) == index
		) as ToArray<T[K]>
	}

	function injectFilterOption<K extends keyof T>(name: K, value: T[K]) {
		// known TS limitation with generic index access
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const options = injectedFiltersOptions as any

		if (!options[name]) {
			options[name] = []
		}
		
		if (Array.isArray(value)) {
			value.forEach((item) => options[name].push(item))
		} else {
			options[name].push(value)
		}
	}

	function resetInjectedFilters() {
		(Object.keys(injectedFiltersOptions) as Array<keyof T>).forEach((key) => {
			delete injectedFiltersOptions[key]
		})
	}

	return {
		getFilterOptions,
		injectFilterOption,
		resetInjectedFilters
	}
}