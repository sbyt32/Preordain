// place files you want to import through the `$lib` alias in this folder.
import { readable, writable } from "svelte/store"

function toggleSidebarViewStatus() {
    const { subscribe, set, update } = writable(false)

    return {
        subscribe,
        showSidebar: () => set(true),
        hideSidebar: () => set(false),
        toggleSidebar: () => update((b) => b = !b)

    }
}

export const connectURL = readable("http://127.0.0.1:8000")
export const sidebarViewStatus = toggleSidebarViewStatus();
