import { ref } from "vue"
import { ResetBehavior } from "../interface/Filters"
import type { FiltersDefinition } from "../interface/Filters"


function getInitFiltersState<T>(filtersDefinition: FiltersDefinition<T>) {
	const initFiltersState = {} as Partial<T> 

	(Object.keys(filtersDefinition) as Array<keyof T>).forEach((filterName) => {
		if (filtersDefinition[filterName].defaultValue != undefined) {
			initFiltersState[filterName] = filtersDefinition[filterName].defaultValue as T[keyof T]
		}
	})

	return initFiltersState
}


export function useFilters<T>(filtersDefinition: FiltersDefinition<T>) {
	const filters = ref<Partial<T>>(getInitFiltersState(filtersDefinition))

	function updateFilters<K extends keyof T>(name: K, value: T[K]) {
		filters.value[name] = value
	}

	function resetFilters() {
		(Object.keys(filtersDefinition) as Array<keyof T>).forEach((filterName) => {
			const definition = filtersDefinition[filterName]
			switch (filtersDefinition[filterName].resetBehavior) {
				case ResetBehavior.None:
					break
				case ResetBehavior.ToDefault:
					filters.value[filterName] = definition.defaultValue
					break
				case ResetBehavior.Clear: 
					delete filters.value[filterName]
			}
		})
	}

	return {
		filters,
		updateFilters,
		resetFilters
	}
}