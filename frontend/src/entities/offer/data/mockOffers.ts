import type { Offer } from "../model/Offer"


export const mockOffers: Offer[] = [
	{
		store: "Steam",
		price_original: 2999,
		price_discount: 1499,
		store_game_link: "https://store.steampowered.com/app/123456"
	},
	{
		store: "Epic Games",
		price_original: 2799,
		price_discount: 1399,
		store_game_link: "https://store.epicgames.com/p/game-name"
	},
	{
		store: "GOG",
		price_original: 2599,
		price_discount: 1299,
		store_game_link: "https://www.gog.com/game/game_name"
	},
	{
		store: "PlayStation Store",
		price_original: 3499,
		price_discount: 1999,
		store_game_link: "https://store.playstation.com/product/123456"
	},
	{
		store: "Xbox Store",
		price_original: 3399,
		price_discount: 1899,
		store_game_link: "https://www.xbox.com/games/store/game-name"
	}
]