import type {  
	GenresFilter, 
	PlatformsFilter, 
	PublishersFilter, 
	StoresFilter 
} from "../model/Filter"


export const genresMock: GenresFilter = {
	genres: [
		{ id: 1, name: "Экшен" },
		{ id: 2, name: "Ролевая игра (RPG)" },
		{ id: 3, name: "Стратегия" },
		{ id: 4, name: "Шутер" },
		{ id: 5, name: "Приключения" },
		{ id: 6, name: "Симулятор" },
		{ id: 7, name: "Головоломка" },
		{ id: 8, name: "Гонки" },
		{ id: 9, name: "Спорт" },
		{ id: 10, name: "Хоррор" }
	]
}

export const platformsMock: PlatformsFilter = {
	platforms: [
		{ id: 1, name: "PC", url: "https://store.steampowered.com" },
		{ id: 2, name: "PlayStation 5", url: "https://www.playstation.com/ps5/" },
		{ id: 3, name: "PlayStation 4", url: "https://www.playstation.com/ps4/" },
		{ id: 4, name: "Xbox Series X|S", url: "https://www.xbox.com/xbox-series-x" },
		{ id: 5, name: "Xbox One", url: "https://www.xbox.com/xbox-one" },
		{ id: 6, name: "Nintendo Switch", url: "https://www.nintendo.com/switch/" },
		{ id: 7, name: "iOS", url: "https://www.apple.com/ios/app-store/" },
		{ id: 8, name: "Android", url: "https://play.google.com/store" }
	]
}

export const publishersMock: PublishersFilter = {
	publishers: [
		{ id: 1, name: "Electronic Arts" },
		{ id: 2, name: "Ubisoft" },
		{ id: 3, name: "Activision" },
		{ id: 4, name: "Bethesda Softworks" },
		{ id: 5, name: "Square Enix" },
		{ id: 6, name: "Capcom" },
		{ id: 7, name: "Bandai Namco" },
		{ id: 8, name: "CD Projekt" },
		{ id: 9, name: "Valve" },
		{ id: 10, name: "Rockstar Games" }
	]
}

export const storesMock: StoresFilter = {
	stores: [
		{ id: 1, name: "Steam", url: "https://store.steampowered.com" },
		{ id: 2, name: "Epic Games Store", url: "https://store.epicgames.com" },
		{ id: 3, name: "GOG", url: "https://www.gog.com" },
		{ id: 4, name: "PlayStation Store", url: "https://store.playstation.com" },
		{ id: 5, name: "Microsoft Store", url: "https://www.microsoft.com/store" },
		{ id: 6, name: "Nintendo eShop", url: "https://www.nintendo.com/store/" },
		{ id: 7, name: "App Store", url: "https://apps.apple.com" },
		{ id: 8, name: "Google Play", url: "https://play.google.com/store" }
	]
}