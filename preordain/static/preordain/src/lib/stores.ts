import { writable, type Writable } from "svelte/store";

// export const displaySidebar: Writable<boolean> = writable(false)
function toggleSidebarViewStatus() {
    const { subscribe, set, update } = writable(false)

    return {
        subscribe,
        showSidebar: () => set(true),
        hideSidebar: () => set(false),
        toggleSidebar: () => update((b) => b = !b)

    }
}

export const sidebarViewStatus = toggleSidebarViewStatus();
