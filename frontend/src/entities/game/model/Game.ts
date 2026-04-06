export interface GameBase {
	id: string,
	title: string,
	image_url: string,
	min_price_original: number,
    min_price_discount: number,
    discount_percent: number
}

export interface GamesCatalog {
	total: number,
  	last_id: number,
  	per_page: number,
	has_more: boolean,
	items: GameBase[]
}