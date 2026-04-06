import type { User } from "../model/User"
import { useDataStore } from "@/shared/lib/useDataStore"


export const authStore = useDataStore<User>()