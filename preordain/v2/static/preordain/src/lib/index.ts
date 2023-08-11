// place files you want to import through the `$lib` alias in this folder.
import { readable } from "svelte/store"
export const connectURL = readable("http://127.0.0.1:8000/")
