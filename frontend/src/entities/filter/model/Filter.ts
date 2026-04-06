export interface FilterValue {
	id: number,
	name: string,
	url?: string
}

export interface GenresFilter {
	genres: FilterValue[]
}

export interface PlatformsFilter {
	platforms: FilterValue[]
}

export interface PublishersFilter {
	publishers: FilterValue[]
}

export interface StoresFilter {
	stores: FilterValue[]
}