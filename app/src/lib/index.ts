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

// If Developing, should use the localhost aka 127.0.0.1 endpoint. If it's deployed, likely through Docker, should use the latter.
// export const connectURL = readable(import.meta.env.DEV ?  "http://127.0.0.1:8000": "http://api:8000")
export const connectURL = readable("http://127.0.0.1:8000")

export const sidebarViewStatus = toggleSidebarViewStatus();
