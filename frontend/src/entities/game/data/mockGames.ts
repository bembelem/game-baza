import type { GameBase, GameFull, GamesCatalog } from "../model/Game"


export const mockGames: GameBase[] = [
  	{
    	id: "5693a916-b56f-4a9e-bf37-9f9661e0eb32",
    	image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/730/header.jpg?t=1749053861",
    	title: "Counter-Strike 2",
		min_price_original: 0,
		min_price_discount: 0,
		discount_percent: 0
	},
	{
		id: "507f0303-cd79-48b7-88e0-f16a0a59d62e",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/3321460/abd7dbdeaede8b6c9a6d40bf116ff2b883f2dd45/header.jpg?t=1774506236",
		title: "Crimson Desert",
		min_price_original: 4299,
		min_price_discount: 4299,
		discount_percent: 0
	},
	{
		id: "90a6eb29-4ed4-45a1-b743-33397ecd3d48",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/570/header.jpg?t=1769535998",
		title: "Dota 2",
		min_price_original: 0,
		min_price_discount: 0,
		discount_percent: 0
	},
	{
		id: "baa89c69-d6ef-4957-ade6-4837eff8308e",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1808500/e337830aa9314003f23d6630f00304bd815bf673/header_alt_assets_3.jpg?t=1772007651",
		title: "ARC Raiders",
		min_price_original: 3220,
		min_price_discount: 2576,
		discount_percent: 20
	},
	{
		id: "9e284f3e-5f0c-4696-a25e-8727524ae8c2",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/578080/841ea38bc58cabb70aef65365cf50bc2d79329d9/header.jpg?t=1764817633",
		title: "PUBG: BATTLEGROUNDS",
		min_price_original: 0,
		min_price_discount: 0,
		discount_percent: 0
	},
	{
		id: "d68d14fc-1e3c-4144-83a1-1486c79e90b2",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/252490/header.jpg?t=1771871433",
		title: "Rust",
		min_price_original: 1699,
		min_price_discount: 1699,
		discount_percent: 0
	},
	{
		id: "c0096818-63de-457f-ae53-89f8ef7deb6a",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/440/header.jpg?t=1757348372",
		title: "Team Fortress 2",
		min_price_original: 0,
		min_price_discount: 0,
		discount_percent: 0
	},
	{
		id: "5ed49f21-61ae-4e64-8f73-2d3c7c355176",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/305620/header.jpg?t=1768865059",
		title: "The Long Dark",
		min_price_original: 1299,
		min_price_discount: 129,
		discount_percent: 90
	},
	{
		id: "55efe13a-4df1-4cfb-a3de-f42f303f625a",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1304930/5a49938b6562464d06a9b7155bae9c435bb71093/header.jpg?t=1774362779",
		title: "The Outlast Trials",
		min_price_original: 1300,
		min_price_discount: 390,
		discount_percent: 70
	},
	{
		id: "b0b73e3e-3098-430a-8042-d2dd73291c43",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/594650/fe85552acc7c8f01f8118f8a6babc38013ba5e38/header_alt_assets_23.jpg?t=1774427675",
		title: "Hunt: Showdown 1896",
		min_price_original: 1619,
		min_price_discount: 647,
		discount_percent: 60
	},
	{
		id: "72d7e284-00f6-4aaa-989f-b5bced341555",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/227300/9a81dc3126c56637297b654f9dcac057cfd79b77/header.jpg?t=1773641450",
		title: "Euro Truck Simulator 2",
		min_price_original: 1249,
		min_price_discount: 1249,
		discount_percent: 0
	},
	{
		id: "5613434d-ea04-42e4-9513-47848cbec768",
		image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2096610/header.jpg?t=1709652109",
		title: "Crysis 3 Remastered",
		min_price_original: 649,
		min_price_discount: 292,
		discount_percent: 55
	}
]

export const mockGameInfo: GameFull = {
	id: "5693a916-b56f-4a9e-bf37-9f9661e0eb32",
	image_url: "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/730/header.jpg?t=1749053861",
	title: "Counter-Strike 2",
	min_price_original: 0,
	min_price_discount: 0,
	discount_percent: 0,

	description: "Counter-Strike 2 — это тактический командный шутер от первого лица, где две команды (террористы и спецназ) сражаются за выполнение целей или уничтожение противника. Игра является обновлённой версией CS:GO на движке Source 2. Counter-Strike 2 — это тактический командный шутер от первого лица, где две команды (террористы и спецназ) сражаются за выполнение целей или уничтожение противника. Игра является обновлённой версией CS:GO на движке Source 2.",
	release_date: "2023-09-27",
	developer: "Valve",
	publisher: "Valve",
	genres: ["Action", "Shooter", "Multiplayer", "FPS"]
}

export const mockGamesCatalog: GamesCatalog = {
	total: 924,
	last_id: 12,
	per_page: 12,
	has_more: true,
	items: mockGames
}